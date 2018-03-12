#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from .models import User,alarm_setting
from word_setting import db, login_manager, app, login_required, logout_user, login_user, current_user
import datetime
import config as cf
import logging
from logging import config
import re

config.fileConfig('loadlog.conf')
load_log = logging.getLogger('loading')

user = Blueprint('user',__name__)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@user.route("/get_cookie")
def get_cookie():
    """获取cookie"""
    cookie = request.cookies.get('username')
    return "cookie username=%s" % cookie

@user.route('/index')
def index():
    return render_template('user/index.html')

@user.route('/logout/')
@login_required
def logout():
    username = current_user.username
    load_log.info(username)
    response = make_response(redirect(url_for('admin.login')))
    response.delete_cookie('username')
    load_log.info(response)
    logout_user()
    return response

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
