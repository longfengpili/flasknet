#!/bin/bash
#helloworld.sh

ps -ef | grep flask_run.py | awk '{print $2}'|xargs kill -9

nohup python3 /usr/longfengpili/loggly/flasknet/flask_run.py >myhup & 
