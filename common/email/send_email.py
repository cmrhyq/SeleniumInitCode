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
import logging
import os
import smtplib
import sys
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
from email.mime.image import MIMEImage
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header

from common.logging_log import MyLogger
from common.read_config import ReadConfig

conf = ReadConfig()
# 日志设置
log = MyLogger(tag='ballLog', colorful=True, save_pth="../logs", existing_counts=7)


def format_email(send_email):
    """
    格式化邮件
    :param send_email: 邮件
    :return:
    """
    new_email = ""
    if "," in send_email:
        for rows in send_email.split(","):
            new_email = new_email + (rows.split("@")[0] + "<%s>" % rows + ",")
        send_email = new_email[0:-1]
    else:
        send_email = send_email.split("@")[0] + "<%s>" % send_email
    return send_email


def set_image(mm, image_path):
    """
    设置图片
    :param mm: 图片
    :param image_path: 图片路径
    :return:
    """
    image_name = image_path.split("/")[len(image_path.split("/")) - 1]
    log.info("开始添加名为%s的图片" % image_name)
    # 二进制读取图片
    image_data = open('image_path', 'rb')
    # 设置读取获取的二进制数据
    message_image = MIMEImage(image_data.read())
    # 关闭刚才打开的文件
    image_data.close()
    # 添加图片文件到邮件信息当中去
    mm.attach(message_image)


def set_file(mm, file_path):
    """
    设置文件
    :param mm: 附件
    :param file_path: 文件路径
    :return:
    """
    for rows in file_path.split(","):
        file_name = rows.split("/")[len(rows.split("/")) - 1]
        log.info("开始添加名为%s的附件" % file_name)
        # 构造附件
        attach = MIMEText(open(rows, 'rb').read(), 'base64', 'utf-8')
        # 设置附件信息
        attach["Content-Disposition"] = 'attachment; filename="%s"' % file_name
        # 添加附件到邮件信息当中去
        mm.attach(attach)


def send(mail_receivers=None, attachments=None, email_theme=None, email_content=None):
    """
    发送邮件
    :param mail_receivers: 收件人，可设置多个收件人：abc@yahoo.com.a,cba@yahoo.com
    :param attachments: 附件
    :param email_theme: 主题
    :param email_content: 内容
    :return:
    """
    # 创建SMTP对象
    stp = smtplib.SMTP()
    try:
        if conf.mail_host is None or conf.mail_sender is None or conf.mail_license is None or mail_receivers is None:
            log.error("邮箱配置错误！邮箱参数为 None")
            sys.exit()

        log.info("开始发送邮件")

        mm = MIMEMultipart('related')

        # 主题
        theme = """%s""" % email_theme
        # 设置发送者，格式：sender_name<******@163.com>
        mm["From"] = format_email(conf.mail_sender)
        mm["To"] = format_email(mail_receivers)
        mm["Subject"] = Header(theme, "utf-8")
        log.info("电子邮件接收者有: %s" % format_email(mail_receivers))

        # 正文
        content = """%s""" % email_content
        send_text = MIMEText(content, "plain", "utf-8")
        mm.attach(send_text)

        # 附件
        if attachments is not None:
            set_file(mm, attachments)
        # 设置发件人邮箱的域名和端口，端口地址为25
        stp.connect(conf.mail_host, 25)
        # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
        # stp.set_debuglevel(1)
        # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
        stp.login(conf.mail_sender, conf.mail_license)
        # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
        stp.sendmail(conf.mail_sender, mail_receivers, mm.as_string())
        # 关闭SMTP对象
        stp.quit()
        log.info("邮件发送结束")
    except Exception as e:
        log.error(e)
    finally:
        stp.quit()
