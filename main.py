#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File main.py
@Contact cmrhyq@163.com
@License (C)Copyright 2022-2025, AlanHuang
@Modify Time 2024/6/19 23:05
@Author Alan Huang
@Version 0.0.1
@Description None
"""
from time import sleep

from openpyxl.reader.excel import load_workbook
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from common.logging_log import MyLogger
from common.read_config import ReadConfig
from common.selenium.selenium_service import SeleniumSimulate

# 常用配置
conf = ReadConfig()
selenium_service = SeleniumSimulate()
browser = selenium_service.start_browser()
# 日志设置
log = MyLogger(tag='ballLog', colorful=True, save_pth="../logs", existing_counts=7)


if __name__ == '__main__':
    browser.get(conf.url)
