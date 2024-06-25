#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File send_email.py
@Contact cmrhyq@163.com
@License (C)Copyright 2022-2025, AlanHuang
@Modify Time 2024/6/25 23:28
@Author Alan Huang
@Version 0.0.1
@Description None
"""
"""
@File          main.py
@Contact       cmrhyq@163.com
@License       (C)Copyright 2022-2025, AlanHuang
@Modify Time   2022/10/26 下午11:21
@Author        Alan Huang
@Version       0.0.1
@Description   None
"""
import logging
import os
import smtplib
import email
import sys
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
from email.mime.image import MIMEImage
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime

from common.printLog import PrintLogger
from common.readXml import ParamCfg


def format_email(send_email):
    new_email = ""
    if "," in send_email:
        for rows in send_email.split(","):
            new_email = new_email + (rows.split("@")[0] + "<%s>" % rows + ",")
        send_email = new_email[0:-1]
    else:
        send_email = send_email.split("@")[0] + "<%s>" % send_email
    return send_email


def set_image(mm, image_path):
    image_name = image_path.split("/")[len(image_path.split("/")) - 1]
    logs.info("Start adding image named %s" % image_name)
    # 二进制读取图片
    image_data = open('image_path', 'rb')
    # 设置读取获取的二进制数据
    message_image = MIMEImage(image_data.read())
    # 关闭刚才打开的文件
    image_data.close()
    # 添加图片文件到邮件信息当中去
    mm.attach(message_image)


def set_file(mm, file_path):
    for rows in file_path.split(","):
        file_name = rows.split("/")[len(rows.split("/")) - 1]
        logs.info("Start adding attachments named %s" % file_name)
        # 构造附件
        attach = MIMEText(open(rows, 'rb').read(), 'base64', 'utf-8')
        # 设置附件信息
        attach["Content-Disposition"] = 'attachment; filename="%s"' % file_name
        # 添加附件到邮件信息当中去
        mm.attach(attach)


def send(config_file, mail_host=None, mail_sender=None, mail_receivers=None,
         mail_license=None, attachments=None, email_theme=None, email_content=None):
    start_time = datetime.now()
    if not os.path.isfile(config_file):
        print("Config file not exist! fileName:%s" % config_file)
        logging.error("Config file not exist! fileName:%s" % config_file)
        sys.exit()
    elif mail_host is None or mail_sender is None or mail_license is None or mail_receivers is None:
        print("Email configuration error! Email parameter is None")
        logging.error("Email configuration error! Email parameter is None")
        sys.exit()

    global logs
    params = ParamCfg(config_file)
    log_file = os.sep.join([params.logPath, params.logName])
    logs = PrintLogger(log_file, int(params.logSize), params.logLevel)
    logs.info("=-=-=-=-=-=-= Action send mail")

    mm = MIMEMultipart('related')

    # 主题
    theme = """%s""" % email_theme
    # 设置发送者，格式：sender_name<******@163.com>
    mm["From"] = format_email(mail_sender)
    mm["To"] = format_email(mail_receivers)
    mm["Subject"] = Header(theme, "utf-8")
    logs.info("Email receivers have %s" % format_email(mail_receivers))

    # 正文
    content = """%s""" % email_content
    send_text = MIMEText(content, "plain", "utf-8")
    mm.attach(send_text)

    # 附件
    if attachments is not None:
        set_file(mm, attachments)

    # 创建SMTP对象
    stp = smtplib.SMTP()
    # 设置发件人邮箱的域名和端口，端口地址为25
    stp.connect(mail_host, 25)
    # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
    # stp.set_debuglevel(1)
    # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
    stp.login(mail_sender, mail_license)
    # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
    stp.sendmail(mail_sender, mail_receivers, mm.as_string())
    # 关闭SMTP对象
    stp.quit()
    logs.info("Takes a total of %s seconds" % (datetime.now() - start_time).microseconds)
    logs.info("=-=-=-=-=-=-= End send mail")
