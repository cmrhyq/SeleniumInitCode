from selenium.webdriver.common.by import By

from common.log import Logger
from test.page.base_page import BasePage
from utils.time.time_utils import sleep


class LoginPage(BasePage):
    def __init__(self):
        super().__init__()
        self.logger = Logger().get_logger()
        self.index_login_button_element = (By.XPATH, '//*[@id="left-menu"]/div/div[1]/div[2]/button')
        self.switch_login_method_element = (By.XPATH, "/html/body/div[16]/div[3]/div[2]/div/div[2]/div[2]/button")
        self.username_element = (By.ID, 'desktop-login-account')
        self.password_element = (By.ID, 'desktop-login-pwd')
        self.login_button_element = (By.XPATH, '/html/body/div[16]/div[3]/div[2]/form/div/div[1]/button[1]')
        self.user_agreement_element = (By.ID, 'desktop-login-policy')

    def index_login_button(self):
        """
        主页登录按钮
        :return:
        """
        self.driver.click(*self.index_login_button_element)
        sleep()

    def switch_login_method(self):
        """
        切换登录方式
        :return:
        """
        self.driver.click(*self.switch_login_method_element)
        sleep()

    def input_username(self, username):
        """
        输入用户名
        :param username:
        :return:
        """
        self.driver.send_keys(*self.username_element, input_content=username)
        sleep()

    def input_password(self, password):
        """
        输入密码
        :param password:
        :return:
        """
        self.driver.send_keys(*self.password_element, input_content=password)
        sleep()

    def from_login_button(self):
        """
        点击登录按钮
        :return:
        """
        self.driver.click(*self.login_button_element)
        sleep()

    def user_agreement(self):
        """
        点击用户协议
        :return:
        """
        self.driver.click(*self.user_agreement_element)
        sleep()

    def screenshot(self):
        self.driver.screen_page()
