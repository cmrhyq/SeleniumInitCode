"""
@File selenium_service.py
@Contact cmrhyq@163.com
@License (C)Copyright 2022-2025, AlanHuang
@Modify Time 2024/6/21 16:15
@Author Alan Huang
@Version 0.0.1
@Description None
"""
import os
import time

import pyperclip
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from domain.entity.selenium import SeleniumBase, LocateElementOptions
from domain.enum.enums import LocateElementMethod
from utils.internet.internet_utils import get_random_pc_ua

from common.log import Logger, log_execution


class SeleniumService:
    """Selenium 服务类，提供浏览器自动化操作"""

    def __init__(self):
        self.logger = Logger(name="selenium").get_logger()
        self.browser = None

    @log_execution(level="INFO")
    def start_browser(self, config: SeleniumBase) -> webdriver.Chrome:
        """启动 Chrome 浏览器"""
        try:
            option = webdriver.ChromeOptions()
            if config.is_headless:
                self.logger.info("启动无头模式")
                option.add_argument('--headless')
            elif config.is_cdp:
                self.logger.info("启动CDP模式")
                option.add_experimental_option('excludeSwitches', ['enable-automation'])
                option.add_experimental_option('useAutomationExtension', False)

            if config.proxy:
                self.logger.info(f"设置代理: {config.proxy_value}")
                option.ignore_local_proxy_environment_variables()
                os.environ['HTTPS_PROXY'] = config.proxy_value
                os.environ['HTTP_PROXY'] = config.proxy_value

            service = Service(config.driver or ChromeDriverManager().install())
            ua = get_random_pc_ua()
            self.logger.debug(f"使用User-Agent: {ua}")
            option.add_argument(f'user-agent={ua}')

            self.browser = webdriver.Chrome(service=service, options=option)
            self.browser.maximize_window()

            if config.is_cdp:
                self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        })
                    """
                })

            self.logger.info("浏览器启动成功")
            return self.browser

        except Exception as e:
            self.logger.error(f"浏览器启动失败: {str(e)}")
            raise

    @log_execution(level="INFO")
    def locate_and_operate_element(self, options: LocateElementOptions):
        """定位元素并执行操作"""
        try:
            self.logger.debug(f"开始定位元素: {options.by}={options.value}")

            if not isinstance(options.wait, WebDriverWait):
                raise ValueError("wait 参数必须是 WebDriverWait 类型")
            if not options.value:
                raise ValueError(f"value 参数不能为空")

            element = options.wait.until(ec.presence_of_element_located((options.by, options.value)))

            if not options.method:
                if options.is_more:
                    elements = options.wait.until(ec.presence_of_all_elements_located((options.by, options.value)))
                    self.logger.debug(f"找到 {len(elements)} 个元素")
                    return elements
                if options.check_visibility:
                    return options.wait.until(ec.visibility_of_element_located((options.by, options.value)))
                return element

            if options.method == LocateElementMethod.CLICK:
                self.logger.debug(f"点击元素: {options.by}={options.value}")
                options.wait.until(ec.element_to_be_clickable((options.by, options.value))).click()
                time.sleep(2)
            elif options.method == LocateElementMethod.INPUT:
                if not options.key:
                    raise ValueError("输入操作必须提供key参数")
                self.logger.debug(f"输入内容: {options.key}")
                options.wait.until(ec.visibility_of_element_located((options.by, options.value)))
                self._safe_input(element, options.key)

        except TimeoutException:
            self.logger.error(f"元素定位超时: {options.by}={options.value}")
            return None
        except NoSuchElementException:
            self.logger.error(f"元素不存在: {options.by}={options.value}")
            return None
        except Exception as e:
            self.logger.error(f"元素操作失败: {str(e)}")
            return None

    def _safe_input(self, element, text):
        """安全的输入文本方法"""
        try:
            pyperclip.copy(text)
            time.sleep(0.2)
            element.send_keys(Keys.CONTROL, 'A')
            time.sleep(0.2)
            element.send_keys(Keys.DELETE)
            time.sleep(0.2)
            element.send_keys(Keys.CONTROL, 'V')
            time.sleep(0.2)
        except Exception as e:
            self.logger.error(f"输入文本失败: {str(e)}")
            raise

    # 启动页面
    def start_page(self, url):
        """
       在浏览器中打开指定的 URL。

       参数:
       url (str): 要打开的网址。

       无返回值。
       """
        self.browser.get(url)

    # 等待时间
    def wait_for_time(self, timeout):
        """
        异步等待指定的时间（秒）。

        参数:
        timeout (int): 等待的时间（秒）。

        无返回值。
        """
        time.sleep(timeout)

    # 查找多个元素
    def find_elements(self, selector_element, selector_type=None):
        # 传了selector_type就获取 没传就通过selector_element进行解析

        """
        查找多个元素。

        参数:
        selector_element (str): 要查找的元素选择器。
        selector_type (str, optional): 选择器类型（例如 'css', 'xpath' 等）。

        返回:
        elements (list): 包含匹配元素的列表。
        """
        return self.browser.find_elements(selector_type, selector_element)

    # 查找元素
    @log_execution(level="INFO")
    def find_element(self, selector_type=None, selector_element=None):
        """
        查找单个元素。

        参数:
        selector_element (str): 要查找的元素选择器。
        selector_type (str, optional): 选择器类型（例如 'css', 'xpath' 等）。

        返回:
        element (WebElement): 匹配的元素。
        """
        try:
            element = self.browser.find_element(selector_type, selector_element)
            return element
        except NoSuchElementException:
            # 处理元素未找到的情况
            self.logger.error(f"未找到匹配的元素: {selector_element}")
            return None  # 或者你可以选择抛出自定义的异常，或者返回其他默认值

    # 输入框 输入内容并提交
    @log_execution(level="INFO")
    def send_keys(self, selector_element, input_content, selector_type=None):
        """
        在指定的选择器位置输入文本内容。

        参数:
        selector_element (str): 要输入文本的元素选择器。
        input_content (str): 要输入的文本内容。
        selector_type (str, optional): 选择器类型（例如 'css', 'xpath' 等）。

        无返回值。
        """
        input_element = self.find_element(selector_element, selector_type)  # 查找输入框元素
        if input_element:
            input_element.send_keys(input_content)  # 输入文本内容
        else:
            self.logger.error(f"未找到元素: {selector_element}")

    # 执行js命令
    def execute_script(self, script_command):
        """
        在当前页面上执行 JavaScript 脚本。

        参数:
        script_command (str): 要执行的 JavaScript 脚本命令。

        无返回值。
        """
        self.browser.execute_script(script_command)

    # 浏览器回退
    def go_back(self):
        """
        在浏览器中回退到上一个页面。

        无返回值。
        """
        self.browser.back()

    # 浏览器前进
    def go_forward(self):
        """
        在浏览器中执行前进操作，前往下一页。

        无返回值。
        """
        self.browser.forward()

    # 获取cookies
    def get_cookies(self):
        """
        获取当前页面的所有 Cookies。

        返回:
        cookies (List): 包含所有 Cookies 的列表。
        """
        return self.browser.get_cookies()

    # 添加cookies
    def add_cookie(self, cookie):
        """
        向当前页面添加一个 Cookie。

        参数:
        cookie (dict): 要添加的 Cookie 对象，应包含 'name' 和 'value' 属性。

        无返回值。
        """
        self.browser.add_cookie(cookie)

    # 删除cookies
    def del_cookies(self):
        """
        删除当前页面的所有 Cookies。

        无返回值。
        """
        self.browser.delete_all_cookies()

    # 切换选项卡
    def switch_tab(self, tab_index):
        """
        在浏览器窗口中切换到指定的标签页。

        参数:
        tab (int): 要切换到的标签页的索引号。

        无返回值。
        """
        self.browser.switch_to.window(self.browser.window_handles[tab_index])

    # 刷新页面
    def reload_page(self):
        """
        重新加载当前页面。

        无返回值。
        """
        self.browser.reload()

    # 截图
    def screen_page(self, file_path=None):
        """
        截取当前页面的屏幕截图并保存到指定路径。

        参数:
        file_path (str, optional): 保存截图的文件路径。如果未提供，将保存为默认文件名（当前目录下的'screenshot.png'）。

        无返回值。
        """
        # 如果未提供文件路径，默认保存为'screenshot.png'在当前目录下
        if not file_path:
            file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "\\resource\\image\\screenshot.png")
        # 获取文件扩展名
        file_extension = os.path.splitext(file_path)[1][1:]
        # 如果不是png格式，转换成png
        if file_extension != 'png':
            file_path = os.path.splitext(file_path)[0] + '.png'

        # 截取屏幕截图并保存
        self.logger.info(f"截图保存路径: {file_path}")
        self.browser.save_screenshot(file_path)

    # 关闭浏览器
    def close_browser(self):
        """
        关闭浏览器。

        无返回值。
        """
        self.browser.close()


    @log_execution(level="INFO")
    def click(self, selector_element, selector_type=None):
        """
        在页面上点击指定的元素。

        参数:
        selector_element (str): 要点击的元素选择器。
        selector_type (str, optional): 选择器类型（例如 'css', 'xpath' 等）。

        无返回值。
        """
        element = self.find_element(selector_element, selector_type)  # 查找要点击的元素
        if element:
            element.click()  # 点击元素
        else:
            self.logger.error(f"未找到元素: {selector_element}")

    # 拉拽动作
    def drag_and_drop(self, source_element, target_element):
        """
        在页面上执行拖拽动作。

        参数:
        source_element (WebElement): 要拖拽的源元素。
        target_element (WebElement): 拖拽的目标元素。

        无返回值。
        """
        actions = ActionChains(self.browser)  # 创建动作链对象
        actions.drag_and_drop(source_element, target_element)  # 执行拖拽操作
        actions.perform()  # 执行动作链中的所有动作
        self.browser.switch_to.alert.accept()  # 处理可能出现的弹窗（假设拖拽操作可能触发了弹窗）

    # iframe
    def to_iframe(self, frame):
        """
        切换到指定的 iframe。

        参数:
        frame (str or WebElement): 要切换的 iframe 元素或者 iframe 的名称或 ID。

        无返回值。
        """
        self.browser.switch_to.frame(frame)

    # 获取页面内容
    def get_content(self):
        """
        获取当前页面的内容。

        返回:
        content (str): 当前页面的 HTML 内容。
        """
        return self.browser.page_source

    def get_child_element_count(self, selector_element, selector_type=None):
        """
        获取当前元素的子元素数量
        :param selector_element: (str): 要查找的元素选择器。
        :param selector_type: (str, optional): 选择器类型（例如 'css', 'xpath' 等）。
        :return:
        """
        element = self.browser.find_element(selector_type, selector_element)
        child_element_count = len(element.find_elements(selector_type, "./child::*"))
        return child_element_count
