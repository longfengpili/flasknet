#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__all__ = ['db', 'login_manger']

from flask import Flask, url_for, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from flask_login import LoginManager

#用户认证
login_manger = LoginManager()

#配置用户认证信息
login_manger.init_app(app)
#认证加密程度
login_manger.session_protection = 'strong'
#登陆认证的处理视图
login_manger.login_view = 'admin.login'
#登陆提示信息
login_manger.login_message = u'请输入密码'
login_manger.login_message_category = 'info'


from word_setting import models
from word_setting import views
