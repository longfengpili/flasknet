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
import word_setting as cs
c_from_addr = cs.mail_address
c_password = base64.b64decode(cs.mail_password.encode('utf-8')).decode('utf-8')
c_to_addr = cs.to_address

#导入图片地址
import os
pwd = os.getcwd()
father_path = os.path.dirname(pwd)
worddb_path = father_path+r'/worddb'



def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(app_name, platform, subject='【Attention】数据异常',note='test'):
    from_addr = c_from_addr
    password = c_password
    to_addr = c_to_addr
    smtp_server = "smtp.office365.com:587"

    #创建一个带附件的实例
    msg = MIMEMultipart()
    msg['From'] = _format_addr('Attention <{}>'.format(from_addr))
    #主题
    msg['Subject'] = Header(subject, 'utf-8').encode()

    #msgAlternative = MIMEMultipart('alternative')
    #msg.attach(msgAlternative)

    html = """
    <p>{}</p>
    <p>近一天数据波动详见下图：</p>
    <p><img src="cid:image1"></p>
    <p><a target="_blank" href="http://sighttp.qq.com/authd?IDKEY=8978c26b91afac72d92579b2e91f6c51700ed40eb07de5a7"><img border="0" src="http://wpa.qq.com/imgd?IDKEY=8978c26b91afac72d92579b2e91f6c51700ed40eb07de5a7&pic=51" alt="点击这里给我发消息" title="点击这里给我发消息"><strong>点击左侧QQ联系我！</strong></a></p>
    """.format(note)

    #正文
    msg.attach(MIMEText(html, 'html', 'utf-8'))

    # 指定图片为当前目录
    pic_add = r'{}/{}({}).png'.format(worddb_path,app_name,platform)
    with open(pic_add, 'rb') as fp:
        msgImage = MIMEImage(fp.read())
        fp.close()
    
    # 定义图片 ID，在 HTML 文本中引用
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)
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
        for to_addr_one in to_addr:
            msg['To'] = _format_addr('监控人员 <{}>'.format(to_addr_one))
            server.sendmail(from_addr, to_addr_one, msg.as_string())
            time.sleep(random.uniform(0,5))
        word_alarm.info('sendmail success!{},{},{},{}'.format(to_addr,app_name,platform,note))

        # server.quit()



if __name__ == '__main__':
    send_mail('word_production','ios','test','test')


