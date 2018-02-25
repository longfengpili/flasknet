#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
sys.path.append("..")
import flasknet_setting as fs

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:3306/word?charset=utf8'.format(fs.mysqlname,fs.mysqlpasswd,fs.mysqlip)
SQLALCHEMY_TRACK_MODIFICATIONS = True
iplist = fs.iplist