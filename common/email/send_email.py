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
log = MyLogger(tag='ballLog', colorful=True, save_pth="../../logs", existing_counts=7)


class SendEmail(object):
    """
    :param receivers: 收件人，可设置多个收件人：abc@yahoo.com.a,cba@yahoo.com
    :param theme: 主题
    :param content: 内容
    """

    def __init__(self, receivers: str, theme: str, content: str):
        super().__init__()
        self.mm = MIMEMultipart('related')
        # 创建SMTP对象
        self.stp = smtplib.SMTP()
        self.mail_receivers = receivers
        self.email_theme = theme
        self.email_content = content

    def format_email(self, send_email):
        """
        格式化邮件
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

    def set_file(self, file_path):
        """
        设置文件
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
            self.mm.attach(attach)

    def send(self):
        """
        发送邮件
        :return:
        """
        try:
            if conf.mail_host is None or conf.mail_sender is None or conf.mail_license is None or self.mail_receivers is None:
                log.error("邮箱配置错误！邮箱参数为 None")
                sys.exit()

            log.info("开始发送邮件")

            # 主题
            theme = """%s""" % self.email_theme
            # 设置发送者，格式：sender_name<******@163.com>
            self.mm["From"] = self.format_email(conf.mail_sender)
            self.mm["To"] = self.format_email(self.mail_receivers)
            self.mm["Subject"] = Header(theme, "utf-8")
            log.info("电子邮件接收者有: %s" % self.format_email(self.mail_receivers))

            # 正文
            content = """%s""" % self.email_content
            send_text = MIMEText(content, "plain", "utf-8")
            self.mm.attach(send_text)

            # # 附件
            # if self.attachments is not None:
            #     self.set_file(self.attachments)
            # 设置发件人邮箱的域名和端口，端口地址为25
            self.stp.connect(conf.mail_host, 25)
            # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
            # stp.set_debuglevel(1)
            # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
            self.stp.login(conf.mail_sender, conf.mail_license)
            # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
            self.stp.sendmail(conf.mail_sender, self.mail_receivers, self.mm.as_string())
            log.info("邮件发送结束")
        except Exception as e:
            log.error(e)
        finally:
            self.stp.quit()


if __name__ == '__main__':
    mail = SendEmail(receivers="9981@qq.com", theme="test", content="test email")
    mail.set_file("../../resource/img/cat.png")
    mail.send()
