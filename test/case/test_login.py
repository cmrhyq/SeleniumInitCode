import allure
import pytest

from test.page.login_page import LoginPage

test_data = [
    ("test_user", "test_password"),
    ("", "test_password"),
    ("test_user", ""),
    ("", ""),
]

@allure.epic("登录页面测试")
@allure.feature("登录页面测试")
class TestLoginPage:

    @allure.story("测试登录用例")
    @allure.title("测试登录")
    @pytest.mark.parametrize("username, password", test_data)
    @pytest.mark.xfail(reason="登录失败，会找不到切换登录方法的按钮元素", strict=True)
    def test_login(self, username, password):
        """
        测试登录
        :return:
        """
        login_page = LoginPage()
        login_page.open()
        login_page.index_login_button()
        login_page.switch_login_method()
        login_page.input_username(username)
        login_page.input_password(password)
        login_page.from_login_button()
        login_page.user_agreement()
        login_page.screenshot()