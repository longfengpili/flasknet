#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
sys.path.append("..")
import flasknet_setting as fs

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@localhost:3306/test?charset=utf8'.format(fs.mysqlname,fs.mysqlpasswd)
SQLALCHEMY_TRACK_MODIFICATIONS = True