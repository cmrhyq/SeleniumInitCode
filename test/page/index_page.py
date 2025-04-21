from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from common.log import Logger
from test.page.base_page import BasePage
from utils.time.time_utils import sleep


class IndexPage(BasePage):
    def __init__(self):
        super().__init__()
        self.logger = Logger().get_logger()
        self.search_input_element = (By.XPATH, '//*[@id="searchRoot"]/div[2]/div/div[1]/div/div[2]/div[4]/form/div[1]/textarea')

    def search_input(self, search_content):
        self.driver.send_keys(*self.search_input_element, input_content=search_content)
        sleep()

    def search(self):
        self.driver.send_keys(*self.search_input_element, input_content=Keys.ENTER)
        sleep(6)

    def screenshot(self):
        self.driver.screen_page()
