#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File loguru_log.py
@Contact cmrhyq@163.com
@License (C)Copyright 2022-2025, AlanHuang
@Modify Time 2024/6/21 0:18
@Author Alan Huang
@Version 0.0.1
@Description None
"""
import sys
from pathlib import Path

from loguru import logger


class VulcanLogger:
    def __init__(self, tag='Vulcan', log_file_name='Vulcan.log'):
        """
        log记录模块
        :param tag: 标签，用于区分log
        :param log_file_name: log名称，默认Vulcan.log
        """
        # 1.仅仅记录log，并将log的内容以print的方式输出到控制台(默认配色)
        # logger.configure(handlers=[{
        #     "sink": f'{Path.cwd()}/logs/{str(log_file_name).rstrip(".log")}-' +
        #             '{time:YYYY-MM-DD}.log',
        #     "rotation": '16 MB',
        #     "retention": '7 days',
        #     "compression": 'zip'
        # }])
        # logger.add(sys.stdout,
        #            format='{time:YYYY-MM-DD HH:mm:ss} | {level:<7} | {module}:{line} - {message}',
        #            filter=lambda record: record['extra'].get('name') == tag, level='DEBUG')

        # 2.记录log，并以更加美观的方式将log输出到控制台
        logger.add(f'{Path.cwd()}/logs/{str(log_file_name).rstrip(".log")}-' + '{time:YYYY-MM-DD}.log',
                   format='{time:YYYY-MM-DD HH:mm:ss} | {level:<7} | {module}:{line} - {message}',
                   filter=lambda record: record['extra'].get('name') == tag, level='DEBUG', rotation='16 MB',
                   retention='7 days', compression='zip')
        self.logger = logger.bind(name=tag)

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    run_logger = VulcanLogger('run', 'Run.log').get_logger()
    test_logger = VulcanLogger('test', 'Run.log').get_logger()

    # 日志输出到Run.log中
    run_logger.info('AAA')
    run_logger.warning('AAA')
    test_logger.error('AAA')
    test_logger.debug('AAA')