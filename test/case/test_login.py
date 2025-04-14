import pytest

from test.page.login_page import LoginPage


class TestLoginPage():
    def test_login(self):
        """
        测试登录
        :return:
        """
        LoginPage().login()