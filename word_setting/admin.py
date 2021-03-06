#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for,make_response,send_file
from .models import Admin,alarm_setting,User
from word_setting import db,login_manager,app,login_required, logout_user, login_user, current_user
import datetime,time
import config as cf
import logging
from logging import config
import re
import os
import random
from flasknet.send_mail import send_mail


config.fileConfig('loadlog.conf')
load_log = logging.getLogger('loading')

from functools import wraps

def admin_login_required(func):
    @wraps(func)
    def admin_login_judge(*args,**rw):
        username = current_user.username
        if Admin.query.filter_by(username=username).first():
            f = func(*args, **rw)
            return f
        else:
            return render_template('admin/not_found.html')
    return admin_login_judge


admin = Blueprint('admin',__name__)

@login_manager.user_loader
def load_user(userid):
    if Admin.query.get(userid):
        return Admin.query.get(userid)
    elif User.query.get(userid):
        return User.query.get(userid)


@admin.route("/get_cookie")
def get_cookie():
    """获取cookie"""
    cookie = request.cookies.get('username')
    return "cookie username={}".format(cookie)


@admin.route("/delete_cookie")
def delete_cookie(username):
    """删除cookie"""
    resp = make_response("delete cookie ok")
    resp.delete_cookie(username)
    return resp

@admin.route('/index')
def index():
    return render_template('admin/index.html')


@admin.route('/login/', methods=['POST', 'GET'])
def login():
    load_log.info(request.cookies.get('username'))
    if request.cookies.get('username'):
        username = request.cookies.get('username')
        if Admin.query.filter_by(username = username).first():
            admin = Admin.query.filter_by(username = username).first()
            login_user(admin)
            next_url = request.args.get('next')
            response = make_response(redirect(next_url or url_for('admin.show')))
            return response
        elif User.query.filter_by(username=username).first():
            user = User.query.filter_by(username=username).first()
            login_user(user)
            next_url = request.args.get('next')
            response = make_response(redirect(next_url or url_for('user.show')))
            return response
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # load_log.info('{},{}'.format(username, password))
        if Admin.query.filter_by(username = username).first():
            admin = Admin.query.filter_by(username=username).first()
            # load_log.info('{}'.format(admin.password_hash))
            if not admin: 
                flash('该用户不存在')
            elif admin.verify_password(password) is False:
                flash('密码错误')  
            else:
                login_user(admin)
                next_url = request.args.get('next') 
                response = make_response(redirect(next_url or url_for('admin.show')))
                response.set_cookie("username", username, max_age=600)
                return response
        elif User.query.filter_by(username=username).first():
            user = User.query.filter_by(username=username).first()
            load_log.info(user)
            if not user: 
                flash('该用户不存在')
            elif user.verify_password(password) is False:
                flash('密码错误')
            else:
                login_user(user)
                response = make_response(redirect(url_for('user.show')))
                response.set_cookie("username", username, max_age=600)
                return response
        else:
            flash('该用户不存在')

    return render_template('admin/login.html')

@admin.route('/logout/')
@login_required
@admin_login_required
def logout():
    username = current_user.username
    logout_user()
    response = make_response(redirect(url_for('admin.login')))
    response.delete_cookie('username')
    return response


@admin.route('/add',methods=['POST','GET'])
@login_required
@admin_login_required
def add():
    if request.method == 'POST':
        p_admin = request.form.get('username',None)
        p_email = request.form.get('email',None)
        p_password = request.form.get('password',None)
        p_role = request.form.get('role',None)
        user = User.query.filter_by(username=p_admin).first()
        admin = Admin.query.filter_by(username=p_admin).first()

        if not p_admin or not p_email or not p_password:
            return 'input error'
        
        elif admin:
            flash('{}用户已经存在'.format(admin))
            return redirect(url_for('admin.add'))
        elif user:
            flash('{}用户已经存在'.format(user))
            return redirect(url_for('admin.add'))

        elif p_role == 'admin':
            newobj = Admin(username=p_admin, email=p_email, password=p_password)
            db.session.add(newobj)
            db.session.commit()
            admins = Admin.query.all()
            return redirect(url_for('admin.add'))
            #return render_template('admin/add.html',admins=admins)
        elif p_role == 'user':
            newobj = User(username=p_admin, email=p_email,password=p_password)
            db.session.add(newobj)
            db.session.commit()
            users = User.query.all()
            return redirect(url_for('admin.add'))
            #return render_template('user/add.html', users=users)
    admins = Admin.query.all()
    users = User.query.all()
    return render_template('admin/add.html',admins=admins,users=users)

@admin.route('/show')
@login_required
@admin_login_required
def show():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    ip = request.remote_addr
    # User_Agent = request.headers.get('User-Agent')
    load_log.info('请求IP【{}】,登录用户{}'.format(ip, current_user))
    # browser_name = re.match('.*(Firefox).*', User_Agent)
    if ip in cf.iplist:
        setting = db.session.query(alarm_setting).filter(alarm_setting.data_ts >= today).order_by(db.desc(alarm_setting.last_mail_time)).order_by(db.desc(
            alarm_setting.total_times)).order_by(db.desc(alarm_setting.times)).order_by(db.desc(alarm_setting.current)).order_by(alarm_setting.app_name).order_by(alarm_setting.platform)
        return render_template('admin/show.html', settings=setting, date=today)
    else:
        return render_template('admin/index.html')

@admin.route('/delete/<username>')
@login_required
@admin_login_required
def delete(username):
    user = User.query.filter_by(username=username).first()
    admin = Admin.query.filter_by(username=username).first()
    if username in cf.adminlist:
        u = Admin.query.filter_by(username=username).first()
        flash('不能删除{}'.format(u))
    elif admin == current_user:
        flash('不能删除当前登录帐号')
    elif admin:
        db.session.delete(admin)
        db.session.commit()
    elif user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin.add'))


@admin.route('/wordimages/<filename>')
@login_required
@admin_login_required
def download(filename):
    load_log.info(filename)
    response = make_response()
    response.headers['Content-Type'] = 'application/png'
    response.headers['X-Accel-Redirect'] = '/admin/images/{}'.format(filename)
    return response


@admin.route('/modifypassword', methods=['POST', 'GET'])
@login_required
@admin_login_required
def modifypassword():
    if request.method == 'POST':
        username = request.form.get('username', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        newPassword = request.form.get('newpassword', None)

        if User.query.filter_by(username=username).first():
            user = User.query.filter_by(username=username).first()
            if email != user.email:
                flash('email错误')
            elif user.verify_password(password) is False:
                flash('密码错误')
            else:
                user.password_hash = user.password_hash_update(newPassword)
                db.session.add(user)
                db.session.commit()
                flash('密码修改成功')

        elif Admin.query.filter_by(username=username).first():
            admin = Admin.query.filter_by(username=username).first()
            if email != admin.email:
                flash('email错误')
            elif admin.verify_password(password) is False:
                flash('密码错误')
            else:
                # load_log.info(admin.password_hash)
                admin.password_hash = admin.password_hash_update(newPassword)
                db.session.add(admin)
                db.session.commit()
                flash('密码修改成功')
                # load_log.info(admin.password_hash)

        else:
            flash('用户名不存在')
    return render_template('admin/modifypassword.html')


@admin.route('/findpassword/<int:step>', methods=['POST', 'GET'])
def find_password(step):
    refer = request.headers.get('Referer', None)
    message = int(request.args.get('message', 0))
    username_form = request.args.get('username', None)

    if request.method == 'POST':
        username = request.form.get('username', None)
        email = request.form.get('email', None)
        username = request.form.get('username', None)
        security_code = request.form.get('securitycode', None)
        newpassword = request.form.get('newpassword', None)

        user = User.query.filter_by(username=username).first()
        admin = Admin.query.filter_by(username=username).first()

        if step == 1:
            if not username or not email:
                flash('请输入完整信息')
            elif admin and admin.email == email:
                i = random.randint(20, len(admin.password_hash)-8)
                security_code = admin.password_hash[i:i+6]
                send_mail(email,security_code)
                flash('请登录邮箱查看验证码并输入修改密码')
                return redirect(url_for('admin.find_password', step=2, message=i,username=username))
            elif user and user.email == email:
                i = random.randint(20, len(user.password_hash)-8)
                security_code = user.password_hash[i:i+6]
                send_mail(email, security_code)
                flash('请登录邮箱查看验证码并输入修改密码')
                return redirect(url_for('admin.find_password', step=2, message=i, username=username))
            else:
                flash('请输入正确信息')
        elif step == 2:
            if not username or not security_code or not newpassword:
                flash('请输入完整信息')
                return redirect(url_for('admin.find_password', step=2, message=message, username=username_form))
            elif admin:
                security_code_real = admin.password_hash[message:message+6]
                if security_code == security_code_real:
                    admin.password_hash = admin.password_hash_update(newpassword)
                    db.session.add(admin)
                    db.session.commit()
                    flash('完成修改密码，请登录！')
                    return redirect(url_for('admin.login'))
                else:
                    flash('请输入正确的验证码')
                    return redirect(url_for('admin.find_password', step=2, message=message, username=username_form))
            elif user:
                security_code_real = user.password_hash[message:message+6]
                if security_code == security_code_real:
                    user.password_hash = user.password_hash_update(newpassword)
                    db.session.add(user)
                    db.session.commit()
                    flash('完成修改密码，请登录！')
                    return redirect(url_for('admin.login'))
                else:
                    flash('请输入正确的验证码')
                    return redirect(url_for('admin.find_password', step=2, message=message, username=username_form))
            else:
                return redirect(url_for('admin.find_password', step=2, message=message, username=username_form))
                flash('请输入正确信息')
        else:
            return redirect(url_for('admin.find_password', step=1))
    elif step > 2:
        return redirect(url_for('admin.find_password', step=1))
    elif step == 2 and not refer:
        flash('请重新提交申请，获取验证码！')
        return redirect(url_for('admin.find_password', step=1))

    return render_template('admin/findpassword_{}.html'.format(step), username=username_form)

    
@app.errorhandler(404)
def not_found_error(error):
    return render_template('admin/not_found.html'), 404


