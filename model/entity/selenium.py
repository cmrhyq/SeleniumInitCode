from dataclasses import dataclass

from selenium.webdriver.support.wait import WebDriverWait

from model.enum.enums import LocateElementMethod


@dataclass
class SeleniumConfig(object):
    """
    is_headless (bool, optional): 是否开启无头模式。默认为 False。
    is_cdp (bool, optional): 是否使用 Chrome Devtools Protocol。默认为 True。
    is_dev (bool, optional): 是否启用调试模式。默认为 True。
    proxy (str, optional): 代理设置。默认为 None，等于None则不适用代理。
    driver (str, optional): 浏览器驱动的路径。默认为 None。等于None会使用webdriver_manager自动下载驱动
    """
    is_headless: bool = False
    is_cdp: bool = True
    is_dev: bool = True
    proxy: str = None
    driver: str = None

@dataclass
class LocateElementOptions(object):
    """
    定位元素选项
    wait (WebDriverWait): WebDriverWait 对象，用于显示等待元素出现
    by (str): 元素定位方式（例如 id，xpath）,必须输入的是字符类型。
    value (str): 元素定位值（例如元素的 ID，XPath 表达式）。
    method (LocateElementMethod): 操作方法（默认为 None）。
    key (str): 输入文本的值（默认为 None）。
    is_more (bool): 是否返回多个元素，默认为 False。
    check_visibility (bool): 是否检查元素可见性（默认为 False）。
    """
    wait: WebDriverWait
    by: str = 'xpath'
    value: str = None
    method: LocateElementMethod = None
    key: str = None
    is_more: bool = False
    check_visibility: bool = False