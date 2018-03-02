#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for,make_response
from .models import Admin,alarm_setting
from word_setting import db,login_manger
import datetime
import config as cf
import logging
from logging import config
import re

config.fileConfig('loadlog.conf')
load_log = logging.getLogger('loading')

from flask_login import login_required, logout_user, login_user,current_user



admin = Blueprint('admin',__name__)


@login_manger.user_loader
def load_user(userid):
    return Admin.query.get(userid)


@admin.route("/set_cookie")
def set_cookie(username):
    """设置cookie"""
    #先创建响应对象
    username = request.form.get('username')
    admin = Admin.query.filter_by(username=username).first()

    if admin and request.form.get('password') == admin.password:
        resp = make_response("set cookie OK")
        # 通过max_age控制cookie有效期, 单位:秒
        resp.set_cookie("username", username, max_age=30000)
        print(resp,username)
        return resp
    else:
        return render_template('admin/login.html')


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
    if request.cookies.get('username'):
        return redirect(url_for('admin.show'))
    elif request.method == 'POST':
        username = request.form.get('username')
        admin = Admin.query.filter_by(username=username).first()
        print(admin)
        if not admin: 
            flash('该用户不存在')
        elif request.form.get('password') != admin.password:  
            flash('密码错误')  
        else:
            login_user(admin)  
            #next_url = request.args.get('next') 
            return redirect(url_for('admin.show'))
    return render_template('admin/login.html')

@admin.route("/logout")
@login_required
def logout():
    username = current_user.username
    print(username)
    logout_user()
    delete_cookie(username)
    return redirect(url_for('admin.show'))


@admin.route('/add/',methods=['POST','GET'])
@login_required
def add():
    if request.method == 'POST':
        p_admin = request.form.get('username',None)
        p_email = request.form.get('email',None)
        p_password = request.form.get('password',None)

        if not p_admin or not p_email or not p_password:
            return 'input error'

        newobj = Admin(username=p_admin, email=p_email, password=p_password)
        db.session.add(newobj)
        db.session.commit()
        admins = Admin.query.all()
        return render_template('admin/add.html',admins=admins)
    admins = Admin.query.all()
    return render_template('admin/add.html',admins=admins)

@admin.route('/show')
@login_required
def show():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
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
