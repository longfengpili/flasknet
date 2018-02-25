#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__all__ = ['db']

from flask import Flask, url_for, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
from word_setting import models
from word_setting import views