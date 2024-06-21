"""
@File read_config.py
@Contact cmrhyq@163.com
@License (C)Copyright 2022-2025, AlanHuang
@Modify Time 2024/6/21 9:43
@Author Alan Huang
@Version 0.0.1
@Description None
"""
import configparser
from config.conf import cm


class ReadConfig(object):
    """配置文件"""

    def __init__(self):
        self.config = configparser.RawConfigParser()  # 当有%的符号时请使用Raw读取
        self.config.read(cm.ini_file, encoding='utf-8')

    def _get(self, section, option):
        """获取"""
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """更新"""
        self.config.set(section, option, value)
        with open(cm.ini_file, 'w') as f:
            self.config.write(f)

    @property
    def url(self):
        return self._get("site", 'url')

    @property
    def log_filename(self):
        return self._get("log", 'filename')

    @property
    def chrome_driver(self):
        return self._get("chrome", 'driver')

    @property
    def site_data_total(self):
        return self._get("site", 'data_total')


if __name__ == '__main__':
    conf = ReadConfig()
    print(conf.url)
