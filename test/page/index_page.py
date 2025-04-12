from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from test.page.base_page import BasePage


class IndexPage(BasePage):
    def __init__(self):
        super().__init__()

    def search_input(self):
        xpath = '//*[@id="searchRoot"]/div[1]/div[2]/div[4]/form/div[1]/textarea'
        self.driver.find_element(By.XPATH, xpath).send_keys("测试是什么")
        self.driver.wait_for_time(3)

    def search(self):
        xpath = '//*[@id="searchRoot"]/div[1]/div[2]/div[4]/form/div[1]/textarea'
        self.driver.find_element(By.XPATH, xpath).send_keys(Keys.ENTER)
        self.driver.wait_for_time(3)

    def screenshot(self):
        self.driver.screen_page()

    def main(self):
        self.open()
        self.search_input()
        self.search()
        self.screenshot()

if __name__ == '__main__':
    IndexPage().main()