from common.selenium.selenium_service import SeleniumService
from config.read_config import ReadConfig
from domain.entity.selenium import SeleniumBase


class BasePage(SeleniumService):
    def __init__(self):
        super().__init__()
        config = SeleniumBase(
            is_headless=False,
            is_cdp=True,
            is_dev=True,
            proxy=True,
            proxy_value="127.0.0.1:7890",
        )
        self.driver = SeleniumService()
        self.driver.start_browser(config)
        self.conf = ReadConfig()

    def open(self):
        self.driver.start_page(self.conf.url)
        self.wait_for_time(2)