#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask import Blueprint, render_template, redirect,request
from .models import User,alarm_setting
from word_setting import db
import datetime

today = datetime.datetime.now().strftime('%Y-%m-%d')

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
    print(today)
    setting = db.session.query(alarm_setting).filter(alarm_setting.data_ts >= today).order_by(db.desc(alarm_setting.last_mail_time))
    return render_template('user/show.html',settings=setting,date = today)