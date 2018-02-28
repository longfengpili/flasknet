#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from word_setting import db  #db是在app/__init__.py生成的关联后的SQLAlchemy实例
from word_setting import login_manger

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<Admin {}>'.format(self.username)


class alarm_setting(db.Model):
    __tablename__ = 'alarm_setting'
    app_name = db.Column(db.String(20))
    platform = db.Column(db.String(20))
    current = db.Column(db.Integer)
    max_line = db.Column(db.Integer)
    times = db.Column(db.Integer)
    total_times = db.Column(db.Integer)
    last_mail_time = db.Column(db.DateTime)
    alarm_line = db.Column(db.Numeric(10,2))
    alarm_type = db.Column(db.Integer)
    alarm_min_line = db.Column(db.Integer)
    alarm_level = db.Column(db.Integer)
    alarm_iap = db.Column(db.Integer)
    data_ts = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<app_platform {}-{}>'.format(self.app_name,self.platform)
