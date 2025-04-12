import pytest

from test.page.login_page import LoginPage


def test_login():
    """
    测试登录
    :return:
    """
    LoginPage().login()