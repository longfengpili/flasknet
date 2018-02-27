#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask import Blueprint, render_template, redirect,request
from .models import User,alarm_setting
from word_setting import db
import datetime
import config as cf
import logging
from logging import config
import re

config.fileConfig('loadlog.conf')
load_log = logging.getLogger('loading')



user = Blueprint('user',__name__)

@user.route('/index')
def index():
    return render_template('user/index.html')

@user.route('/add/',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        p_user = request.form.get('username',None)
        p_email = request.form.get('email',None)
        p_password = request.form.get('password',None)

        if not p_user or not p_email or not p_password:
            return 'input error'

        newobj = User(username=p_user, email=p_email, password=p_password)
        db.session.add(newobj)
        db.session.commit()
        users = User.query.all()
        return render_template('user/add.html',users=users)
    users = User.query.all()
    return render_template('user/add.html',users=users)

@user.route('/show')
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
