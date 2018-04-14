#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__ = 'longfengpili'

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
import base64
import re
import time
import random

#导入配置
import sys
sys.path.append('..')
import flasknet_setting as cs
c_from_addr = cs.mail_address
c_password = base64.b64decode(cs.mail_password.encode('utf-8')).decode('utf-8')


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(to_addr, security_code,subject='【word实时监控】验证码'):
    from_addr = c_from_addr
    password = c_password
    to_addr = to_addr
    smtp_server = "smtp.office365.com:587"

    #创建一个带附件的实例
    msg = MIMEMultipart()
    msg['From'] = _format_addr('【word实时监控】<{}>'.format(from_addr))
    #主题
    msg['Subject'] = Header(subject, 'utf-8').encode()

    #msgAlternative = MIMEMultipart('alternative')
    #msg.attach(msgAlternative)

    html = """
    <p>您正在申请修改密码，验证码：</p>
    <p style="color:red"><strong>{}</strong></p>
    <p><a target="_blank" href="http://sighttp.qq.com/authd?IDKEY=8978c26b91afac72d92579b2e91f6c51700ed40eb07de5a7"><img border="0" src="http://wpa.qq.com/imgd?IDKEY=8978c26b91afac72d92579b2e91f6c51700ed40eb07de5a7&pic=51" alt="点击这里给我发消息" title="点击这里给我发消息"><strong>点击左侧QQ联系我！</strong></a></p>
    """.format(security_code)

    #正文
    msg.attach(MIMEText(html, 'html', 'utf-8'))

    server = smtplib.SMTP()
    with server:
        #服务器连接
        server.connect(smtp_server)

        #返回服务器特性
        #server.set_debuglevel(1)

        server.ehlo()
        #进行TLS安全传输
        server.starttls()
        server.login(from_addr, password)

        # 邮件发送
        
        msg['To'] = _format_addr('监控人员 <{}>'.format(to_addr))
        server.sendmail(from_addr, to_addr, msg.as_string())
        time.sleep(random.uniform(0,5))
        # server.quit()



if __name__ == '__main__':
    send_mail('398745129@qq.com','333333')


