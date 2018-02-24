#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from app import app
from .admin import admin
from .user import user

app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')