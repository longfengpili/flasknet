#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from word_setting import db  # db是在app/__init__.py生成的关联后的SQLAlchemy实例
#from word_setting import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(320), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute/ password 不是一个可读属性。')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(320), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username,email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute/ password 不是一个可读属性。')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

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
    alarm_line = db.Column(db.Numeric(10, 2))
    alarm_type = db.Column(db.Integer)
    alarm_min_line = db.Column(db.Integer)
    alarm_level = db.Column(db.Integer)
    alarm_iap = db.Column(db.Integer)
    data_ts = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<app_platform {}-{}>'.format(self.app_name, self.platform)
