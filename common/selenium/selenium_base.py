"""
@File selenium_base.py
@Contact cmrhyq@163.com
@License (C)Copyright 2022-2025, AlanHuang
@Modify Time 2024/6/21 16:15
@Author Alan Huang
@Version 0.0.1
@Description None
"""


class BrowserSimulateBase:
    def __init__(self):
        pass

    def start_browser(self, is_headless=False, is_cdp=False, is_dev=False, proxy=None, is_socks5=False, *args,
                      **kwargs):
        """
        启动浏览器。

        Args:
            is_headless (bool, optional): 是否开启无头模式。默认为 False。
            is_cdp (bool, optional): 是否使用 Chrome Devtools Protocol。默认为 False。
            is_dev (bool, optional): 是否启用调试模式。默认为 False。
            proxy (str, optional): 代理设置。默认为 None。
            is_socks5 (bool, optional): 是否使用 SOCKS5 代理。默认为 False。
            *args, **kwargs: 其他参数。

        Raises:
            NotImplementedError: 派生类需要实现该方法。
        """
        raise NotImplementedError

    # 启动页面
    def start_page(self, url):
        raise NotImplementedError

    # 显式等待
    def wait_until_element(self, selector_location, timeout=None, selector_type=None):
        raise NotImplementedError

    # 等待时间
    def wait_time(self, timeout):
        raise NotImplementedError

    # 等待时间
    def wait_for_time(self, timeout):
        raise NotImplementedError

    # 查找多个元素
    def find_elements(self, selector_location, selector_type=None):
        raise NotImplementedError

    # 查找元素
    def find_element(self, selector_location, selector_type=None):
        raise NotImplementedError

    # 输入框 输入内容并提交
    def send_keys(self, selector_location, input_content, selector_type=None):
        raise NotImplementedError

    # 执行js命令
    def execute_script(self, script_command):
        raise NotImplementedError

    # 浏览器回退
    def go_back(self):
        raise NotImplementedError

    # 浏览器前进
    def go_forward(self):
        raise NotImplementedError

    # 获取cookies
    def get_cookies(self):
        raise NotImplementedError

    # 添加cookies
    def add_cookie(self, cookie):
        raise NotImplementedError

    # 删除cookies
    def del_cookies(self):
        raise NotImplementedError

    # 切换选项卡
    def switch_tab(self, tab_index):
        raise NotImplementedError

    # 刷新页面
    def reload_page(self):
        raise NotImplementedError

    # 截图
    def screen_page(self, file_name=None):
        raise NotImplementedError

    # 关闭浏览器
    def close_browser(self):
        raise NotImplementedError

    # 获取页面内容
    def get_content(self):
        raise NotImplementedError

    # 点击
    def click(self, selector_location, selector_type=None):
        raise NotImplementedError

    # 拉拽动作
    def drag_and_drop(self, source_element, target_element):
        raise NotImplementedError

    # 拉拽动作
    def to_iframe(self, frame):
        raise NotImplementedError
