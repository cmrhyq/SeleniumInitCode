from common.selenium.selenium_service_normal import SeleniumServiceNormal
from config.read_config import ReadConfig
from model.entity.selenium import SeleniumBase
from utils.time.time_utils import sleep


class BasePage(SeleniumServiceNormal):
    def __init__(self):
        super().__init__()
        config = SeleniumBase(
            is_headless=False,
            is_cdp=True,
            is_dev=True,
            proxy="127.0.0.1:7890",
        )
        self.driver = SeleniumServiceNormal()
        self.driver.start_browser(config)
        self.conf = ReadConfig()

    def open(self):
        self.driver.start_page(self.conf.url)
        sleep()