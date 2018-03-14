#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for,make_response
from .models import Admin,alarm_setting,User
from word_setting import db,login_manager,app,login_required, logout_user, login_user, current_user
import datetime,time
import config as cf
import logging
from logging import config
import re


config.fileConfig('loadlog.conf')
load_log = logging.getLogger('loading')

from functools import wraps

def admin_login_required(func):
    @wraps(func)
    def admin_login_judge(*args,**rw):
        username = current_user.username
        load_log.info(username)
        if Admin.query.filter_by(username=username).first():
            load_log.info(Admin.query.filter_by(username=username).first())
            f = func()
            return f
        else:
            load_log.info('admin.not_found')
            return render_template('admin/not_found.html')
    return admin_login_judge


admin = Blueprint('admin',__name__)

@login_manager.user_loader
def load_user(userid):
    if Admin.query.get(userid):
        load_log.info(Admin.query.get(userid))
        return Admin.query.get(userid)
    elif User.query.get(userid):
        load_log.info(User.query.get(userid))
        return User.query.get(userid)


@admin.route("/get_cookie")
def get_cookie():
    """获取cookie"""
    cookie = request.cookies.get('username')
    return "cookie username=%s" % cookie


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
        load_log.info(username)
        if Admin.query.filter_by(username = username).first():
            admin = Admin.query.filter_by(username = username).first()
            load_log.info(admin)
            login_user(admin)
            load_log.info(current_user)
            next_url = request.args.get('next')
            response = make_response(redirect(next_url or url_for('admin.show')))
            return response
        elif User.query.filter_by(username=username).first():
            user = User.query.filter_by(username=username).first()
            load_log.info(user)
            login_user(user)
            next_url = request.args.get('next')
            response = make_response(redirect(next_url or url_for('user.show')))
            return response
    elif request.method == 'POST':
        username = request.form.get('username')
        load_log.info(username)
        if Admin.query.filter_by(username = username).first():
            admin = Admin.query.filter_by(username=username).first()
            load_log.info(admin)
            if not admin: 
                flash('该用户不存在')
            elif request.form.get('password') != admin.password:  
                flash('密码错误')  
            else:
                login_user(admin)
                load_log.info(admin)
                load_log.info(current_user)
                next_url = request.args.get('next') 
                load_log.info(next_url)
                response = make_response(redirect(next_url or url_for('admin.show')))
                response.set_cookie("username", username, max_age=30)
                return response
        elif User.query.filter_by(username=username).first():
            user = User.query.filter_by(username=username).first()
            load_log.info(user)
            if not user: 
                flash('该用户不存在')
            elif request.form.get('password') != user.password:  
                flash('密码错误')  
            else:
                login_user(user)
                response = make_response(redirect(url_for('user.show')))
                response.set_cookie("username", username, max_age=30)
                return response
        else:
            load_log.info('wrong')

    return render_template('admin/login.html')

@admin.route('/logout/')
@login_required
@admin_login_required
def logout():
    username = current_user.username
    print(username)
    logout_user()
    response = make_response(redirect(url_for('admin.login')))
    response.delete_cookie('username')
    return response


@admin.route('/add/',methods=['POST','GET'])
@login_required
@admin_login_required
def add():
    if request.method == 'POST':
        p_admin = request.form.get('username',None)
        p_email = request.form.get('email',None)
        p_password = request.form.get('password',None)
        p_role = request.form.get('role',None)

        if not p_admin or not p_email or not p_password:
            return 'input error'
        
        if p_role == 'admin':
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
    print(today)
    ip = request.remote_addr
    User_Agent = request.headers.get('User-Agent')
    load_log.info('请求IP【{}】,请求头{}'.format(ip, User_Agent))
    browser_name = re.match('.*(Firefox).*', User_Agent)
    if ip in cf.iplist and browser_name:
        setting = db.session.query(alarm_setting).filter(alarm_setting.data_ts >= today).order_by(db.desc(alarm_setting.last_mail_time)).order_by(db.desc(
            alarm_setting.total_times)).order_by(db.desc(alarm_setting.times)).order_by(db.desc(alarm_setting.current)).order_by(alarm_setting.app_name).order_by(alarm_setting.platform)
        return render_template('admin/show.html', settings=setting, date=today)
    else:
        return render_template('admin/index.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('admin/not_found.html'), 404


