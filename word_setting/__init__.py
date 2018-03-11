#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__all__ = ['db', 'login_manager']

from flask import Flask, url_for, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from flask_login import LoginManager

#用户认证
login_manager = LoginManager()

#配置用户认证信息
login_manager.init_app(app)
#认证加密程度
login_manager.session_protection = 'strong'
#登陆认证的处理视图
login_manager.login_view = 'admin.login'
#登陆提示信息
login_manager.login_message = u'请登录'
login_manager.login_message_category = 'info'


from word_setting import models
from word_setting import views
