# import pytest
#
#
# # fixture函数(类中) 作为多个参数传入
# @pytest.fixture()
# def login():
#     print("打开浏览器")
#     a = "account"
#     return a
#
#
# @pytest.fixture()
# def logout():
#     print("关闭浏览器")
#
# def test_case_01():
#     """测试函数01"""
#     print("测试函数01执行完成")
#
#
# def test_case_02():
#     """测试函数02"""
#     print("测试函数02执行完成")
#
#
# def test_case_03():
#     """测试函数03"""
#     print("测试函数03执行完成")
#     assert False
#
#
# @pytest.mark.parametrize("data", [1, 3, 5, 7, 8])
# def test_case_04(data):
#     """测试函数04"""
#
#     print("测试函数04执行完成")
#     assert data % 2 != 0, "偶数失败，奇数通过"
#
#
# class TestCase:
#     # 传入lonin fixture
#     def test_001(self, login):
#         print("001传入了loging fixture")
#         assert login == "account"
#
#     # 传入logout fixture
#     def test_002(self, logout):
#         print("002传入了logout fixture")
#
#     def test_003(self, login, logout):
#         print("003传入了两个fixture")
#
#     def test_004(self):
#         print("004未传入仍何fixture哦")
#
#
# if __name__ == '__main__':
#     pytest.main()
