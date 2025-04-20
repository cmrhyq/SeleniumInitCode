import allure
import pytest

from test.page.index_page import IndexPage

@allure.feature("搜索首页测试")
class TestIndexPage:

    @allure.story("搜索用例")
    @allure.title("测试搜索用例")
    @pytest.mark.parametrize("search_content", ["测试是什么"])
    def test_search(self, search_content):
        """
        测试搜索
        :return:
        """
        index_page = IndexPage()
        index_page.open()
        index_page.search_input(search_content)
        index_page.search()
        index_page.screenshot()