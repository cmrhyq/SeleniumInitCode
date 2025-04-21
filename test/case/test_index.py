import allure
import pytest

from test.page.index_page import IndexPage

test_data = [
    "测试是什么",
    "pytest的用法",
    "selenium的使用"
]

"""
测试首页搜索功能
1. 打开首页
2. 输入搜索内容
3. 点击搜索按钮
4. 截图
"""
@allure.epic("搜索首页测试")
@allure.feature("搜索首页测试")
class TestIndexPage:


    @allure.step("打开首页，进行搜索操作")
    @allure.story("搜索用例")
    @allure.title("测试搜索用例")
    @pytest.mark.parametrize("search_content", test_data)
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