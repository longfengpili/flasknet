#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from word_setting import app
from .admin import admin


app.register_blueprint(admin,url_prefix='/admin')
