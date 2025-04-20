import os

from selenium import webdriver
import threading

from selenium.common import NoSuchElementException
from selenium.webdriver import Proxy
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from common.log import Logger, log_execution
from model.entity.selenium import SeleniumBase
from utils.internet.internet_utils import get_random_pc_ua


logger = Logger().get_logger()

class SeleniumServiceSingleton:
    """
    SeleniumServiceSingleton 是一个单例类，用于管理 Selenium WebDriver 实例。
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, config: SeleniumBase):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SeleniumServiceSingleton, cls).__new__(cls)
                option = webdriver.ChromeOptions()
                if config.is_headless:
                    logger.info("启动无头模式")
                    option.add_argument('--headless')
                elif config.is_cdp:
                    logger.info("启动CDP模式")
                    option.add_experimental_option('excludeSwitches', ['enable-automation'])
                    option.add_experimental_option('useAutomationExtension', False)

                if config.proxy:
                    logger.info(f"设置代理: {config.proxy}")
                    # 旧方法，selenium弃用了
                    # option.ignore_local_proxy_environment_variables()
                    # os.environ['HTTPS_PROXY'] = config.proxy
                    # os.environ['HTTP_PROXY'] = config.proxy
                    # 新设置代理的方法
                    settings = {
                        "httpProxy": config.proxy,
                        "httpsProxy": config.proxy,
                        "sslProxy": config.proxy,
                    }
                    Proxy(settings)

                service = Service(config.driver or ChromeDriverManager().install())
                ua = get_random_pc_ua()
                logger.debug(f"使用User-Agent: {ua}")
                option.add_argument(f'user-agent={ua}')
                cls._instance.driver = webdriver.Chrome(service=service, options=option)  # 只创建一次 WebDriver
        return cls._instance


    def get_driver(self):
        return self.driver

    # 查找多个元素
    def find_elements(self, selector_type, selector_element):
        # 传了selector_type就获取 没传就通过selector_element进行解析

        """
        查找多个元素。

        参数:
        selector_element (str): 要查找的元素选择器。
        selector_type (str, optional): 选择器类型（例如 'css', 'xpath' 等）。

        返回:
        elements (list): 包含匹配元素的列表。
        """
        return self.driver.find_elements(selector_type, selector_element)

    @log_execution(level="INFO")
    def find_element(self, selector_type, selector_element):
        """
        查找单个元素。

        参数:
        selector_element (str): 要查找的元素选择器。
        selector_type (str, optional): 选择器类型（例如 'css', 'xpath' 等）。

        返回:
        element (WebElement): 匹配的元素。
        """
        try:
            element = self.driver.find_element(selector_type, selector_element)
            return element
        except NoSuchElementException:
            # 处理元素未找到的情况
            logger.error(f"未找到匹配的元素: {selector_element}")
            return None  # 或者你可以选择抛出自定义的异常，或者返回其他默认值

# 示例
if __name__ == "__main__":
    driver1 = SeleniumServiceSingleton(SeleniumBase(
        is_headless=False,
        is_cdp=True,
        is_dev=True,
        proxy="127.0.0.1:7890"
    )).get_driver()
    driver2 = SeleniumServiceSingleton(SeleniumBase(
        is_headless=False,
        is_cdp=True,
        is_dev=True,
        proxy="127.0.0.1:7890"
    )).get_driver()

    print(driver1 is driver2)  # True，确保只有一个实例
    driver1.get("https://www.baidu.com")
    driver1.find_element(By.ID, "kw").send_keys("selenium")
    driver1.find_element(By.ID, "su").click()