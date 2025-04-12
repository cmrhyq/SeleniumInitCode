import pytest


def test_case_01():
    """测试函数01"""
    print("测试函数01执行完成")


def test_case_02():
    """测试函数02"""
    print("测试函数02执行完成")


def test_case_03():
    """测试函数03"""
    print("测试函数03执行完成")
    assert False


@pytest.mark.parametrize("data", [1, 3, 5, 7, 8])
def test_case_04(data):
    """测试函数04"""

    print("测试函数04执行完成")
    assert data % 2 != 0, "偶数失败，奇数通过"