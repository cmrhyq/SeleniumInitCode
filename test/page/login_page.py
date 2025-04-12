from selenium.webdriver.common.by import By
from test.page.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self):
        super().__init__()

    def index_login_button(self):
        """
        主页登录按钮
        :return:
        """
        xpath = '//*[@id="searchRoot"]/div[1]/div[1]/div/div[1]/div[2]/button'
        self.driver.wait_for_time(3)
        self.driver.find_element(By.XPATH, xpath).click()

    def switch_login_method(self):
        xpath = "/html/body/div[11]/div[3]/div[2]/div/div[2]/div[2]"
        self.driver.wait_for_time(3)
        self.driver.find_element(By.XPATH, xpath).click()

    def input_username(self, username):
        xpath = '//*[@id="username"]'
        self.driver.wait_for_time(3)
        self.driver.find_element(By.XPATH, xpath).send_keys(username)

    def input_password(self, password):
        xpath = '//*[@id="password"]'
        self.driver.wait_for_time(3)
        self.driver.find_element(By.XPATH, xpath).send_keys(password)

    def from_login_button(self):
        """
        点击登录按钮
        :return:
        """
        xpath = '/html/body/div[11]/div[3]/div[2]/form/div/div[1]/button[1]'
        self.driver.wait_for_time(3)
        self.driver.find_element(By.XPATH, xpath).click()

    def user_agreement(self):
        xpath = '//*[@id="desktop-login-policy"]'
        self.driver.wait_for_time(3)
        self.driver.find_element(By.XPATH, xpath).click()

    def login(self):
        self.open()
        self.index_login_button()
        self.switch_login_method()
        self.input_username(self.conf.site_username)
        self.input_password(self.conf.site_password)
        self.from_login_button()
        self.user_agreement()


if __name__ == "__main__":
    LoginPage().login()