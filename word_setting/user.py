#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from .models import User,alarm_setting
from word_setting import db,login_manger_user,app
import datetime
import config as cf
import logging
from logging import config
import re

config.fileConfig('loadlog.conf')
load_log = logging.getLogger('loading')

from flask_login import login_required, logout_user, login_user, current_user

user = Blueprint('user',__name__)


@login_manger_user.user_loader
def load_user(userid):
    return User.query.get(userid)


@user.route("/get_cookie")
def get_cookie():
    """获取cookie"""
    cookie = request.cookies.get('username')
    return "cookie username=%s" % cookie


@user.route("/delete_cookie")
def delete_cookie(username):
    """删除cookie"""
    resp = make_response("delete cookie ok")
    resp.delete_cookie(username)
    return resp


@user.route('/index')
def index():
    return render_template('user/index.html')


@user.route('/login/', methods=['POST', 'GET'])
def login():
    if request.cookies.get('username'):
        username = request.cookies.get('username')
        user = User.query.filter_by(username=username).first()
        login_user(user)
        next_url = request.args.get('next')
        response = make_response(redirect(next_url or url_for('user.show')))
        return response
    elif request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('该用户不存在')
        elif request.form.get('password') != user.password:
            flash('密码错误')
        else:
            login_user(user)
            next_url = request.args.get('next')
            response = make_response(
                redirect(next_url or url_for('user.show')))
            response.set_cookie("username", username, max_age=30)
            return response
    return render_template('user/login.html')


@user.route("/logout/")
@login_required
def logout():
    username = current_user.username
    print(username)
    logout_user()
    delete_cookie(username)
    return redirect(url_for('user.login'))


# @user.route('/add/',methods=['GET','POST'])
# def add():
#     if request.method == 'POST':
#         p_user = request.form.get('username',None)
#         p_email = request.form.get('email',None)
#         p_password = request.form.get('password',None)

#         if not p_user or not p_email or not p_password:
#             return 'input error'

#         newobj = User(username=p_user, email=p_email, password=p_password)
#         db.session.add(newobj)
#         db.session.commit()
#         users = User.query.all()
#         return render_template('user/add.html',users=users)
#     users = User.query.all()
#     return render_template('user/add.html',users=users)

@user.route('/show')
@login_required
def show():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    ip = request.remote_addr
    User_Agent = request.headers.get('User-Agent')
    load_log.info('请求IP【{}】,请求头{}'.format(ip,User_Agent))
    browser_name = re.match('.*(Firefox).*',User_Agent)
    if ip in cf.iplist and browser_name is not None:
        setting = db.session.query(alarm_setting).filter(alarm_setting.data_ts >= today).order_by(db.desc(alarm_setting.last_mail_time)).order_by(db.desc(alarm_setting.total_times)).order_by(db.desc(alarm_setting.times)).order_by(db.desc(alarm_setting.current)).order_by(alarm_setting.app_name).order_by(alarm_setting.platform)
        return render_template('user/show.html',settings=setting,date = today)
    else:
        return render_template('user/index.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('user/not_found.html'), 404
