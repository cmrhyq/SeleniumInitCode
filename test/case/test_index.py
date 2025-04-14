import pytest

from test.page.index_page import IndexPage


class TestIndexPage():
    def test_search(self):
        """
        测试登录
        :return:
        """
        IndexPage().main()