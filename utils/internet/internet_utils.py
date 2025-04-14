#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File internet_utils.py
@Contact cmrhyq@163.com
@License (C)Copyright 2022-2025, AlanHuang
@Modify Time 2024/5/7 下午8:12
@Author Alan Huang
@Version 0.0.1
@Description Internet Utils
"""

from random import choice
import socket
from contextlib import closing

__all__ = [
    '_get_url_contain_params',  # 根据params组合得到包含params的url
    'tuple_or_list_params_2_dict_params',  # tuple和list类型的params转dict类型的params
    'str_cookies_2_dict',  # cookies字符串转dict
    'dict_cookies_2_str',  # dict类型cookies转str
    'driver_cookies_list_2_str',  # driver_cookies_list_2_str

    # chrome下抓包后, requests处理相关
    'chrome_copy_requests_header_2_dict_headers',  # 将直接从chrome复制的Request Headers转换为dict的headers
    'chrome_copy_query_string_parameters_2_tuple_params',  # 将直接从chrome复制的Query String Parameters转换为tuple类型的params

    'get_random_pc_ua',  # 得到一个随机pc headers
    'get_random_phone_ua',  # 得到一个随机phone headers
    'get_base_headers',  # 得到一个base headers

    # ip判断
    'is_ipv4',  # 判断是否为ipv4地址
    'is_ipv6',  # 判断是否为ipv6地址
    'get_local_free_port',  # 随机获取一个可以被绑定的空闲端口

    # html
    'html_entities_2_standard_html',  # 将html实体名称/实体编号转为html标签
]


def _get_url_contain_params(url, params):
    """
    根据params组合得到包含params的url
    :param url:
    :param params:
    :return: url
    """
    return url + '?' + '&'.join([item[0] + '=' + item[1] for item in params])


def str_cookies_2_dict(str_cookies):
    """
    cookies字符串转dict
    :param str_cookies:
    :return:
    """
    _ = []
    for i in str_cookies.replace(' ', '').split(';'):
        if i != '':
            _.append((i.split('=')[0], i.split('=')[1]))

    cookies_dict = {}
    for item in _:
        cookies_dict.update({item[0]: item[1]})

    return cookies_dict


def tuple_or_list_params_2_dict_params(params):
    """
    tuple和list类型的params转dict类型的params
    :param params:
    :return:
    """
    _ = {}
    for item in params:
        _.update({
            item[0]: item[1]
        })

    return _


def chrome_copy_requests_header_2_dict_headers(copy_headers):
    """
    将直接从chrome复制的Request Headers转换为dict的headers
    :param copy_headers:
    :return: a dict
    """
    # .sub('\"\1\":\"2\"', copy_headers)
    # before_part = re.compile('^(.*):').findall(copy_headers)
    # end_part = re.compile(':(.*)$').findall(copy_headers)
    # print(before_part)
    # print(end_part)
    _ = copy_headers.split('\n')
    _ = [item.split(': ') for item in _]
    # pprint(_)

    tmp = {}
    for item in _:
        if item != ['']:
            if item[0].startswith(':'):  # 去除':authority'这些
                continue
            item_1 = item[1].replace(' ', '')
            tmp.update({item[0]: item_1})

    return tmp


def chrome_copy_query_string_parameters_2_tuple_params(copy_params):
    """
    将直接从chrome复制的Query String Parameters转换为tuple类型的params
    :param copy_params:
    :return: (('xx', 'yy'), ...)
    """
    _ = copy_params.split('\n')
    _ = [item.split(': ') for item in _]
    # pprint(_)

    tmp = []
    for item in _:
        if item != ['']:
            if len(item) == 1:
                item_1 = ''
            else:
                item_1 = item[1].replace(' ', '')
            tmp.append((item[0], item_1))

    return tuple(tmp)


def get_random_pc_ua():
    """
    得到一个随机pc ua
    :return: str 随机的User-Agent字符串
    """
    PC_HEADERS = [
        # Chrome (新版本)
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

        # Firefox (新版本)
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",

        # Safari (新版本)
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",

        # Edge (基于Chromium)
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",

        # Opera GX (新版本)
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",

        # Brave
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Brave/120.0.0.0",

        # Vivaldi
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Vivaldi/6.5.3206.53",
    ]

    return choice(PC_HEADERS)


def get_random_phone_ua():
    """
    随机一个随机phone ua
    :return:
    """
    PHONE_HEADERS = [
        # iphone
        'Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en',
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Mobile/15A5341f APP_USER/quanmama(ios_5.3.2)',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 MicroMessenger/6.5.17 NetType/WIFI Language/zh_HK',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.5.16 NetType/WIFI Language/zh_CN',
        'Mozilla/5.0 (iPhone 92; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.7.2 Mobile/15A372 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A405 MicroMessenger/6.5.15 NetType/WIFI Language/zh_CN',
        'Mozilla/5.0 (iPhone 91; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14C92 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 wxwork/2.1.5 MicroMessenger/6.3.22',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A402 MicroMessenger/6.5.16 NetType/WIFI Language/zh_CN',
        'Mozilla/5.0 (iPhone 6; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/6.0 MQQBrowser/6.6.1 Mobile/13E238 Safari/8536.25',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E277 MicroMessenger/6.5.16 NetType/4G Language/zh_CN',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.17 NetType/WIFI Language/en',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 MicroMessenger/6.5.15 NetType/4G Language/zh_CN',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 search%2F1.0 baiduboxapp/0_0.1.1.7_enohpi_8022_2421/1.2.9_1C2%257enohPi/1099a/088D84D1E9A6AEE91798B97AAA03690B96CFCB638FGIMSINMHB/1',
        'Mozilla/5.0 (iPhone 6sp; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.8.0 Mobile/15A372 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
        'Mozilla/5.0 (iPhone 6p; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 MQQBrowser/7.8.0 Mobile/12B436 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A365 Safari/600.1.4',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/12A365 UCBrowser/10.2.5.551 Mobile',
        'Mozilla/5.0 (iPhone 5SGLOBAL; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/6.0 MQQBrowser/5.6 Mobile/12A365 Safari/8536.25',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/7.0 Mobile/12A365 Safari/9537.53',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Coast/4.01.88243 Mobile/12A365 Safari/7534.48.3',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/40.0.2214.69 Mobile/12A365 Safari/600.1.4',
        'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1C28 Safari/419.3',
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A334 Safari/7534.48.3',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A405 Safari/7534.48.3',

        # android
        'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G9280 Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; SM-G9280 Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.9 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM-G9280 Build/MMB29K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.0.818 U3/0.8.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; HW-HUAWEI_C8813Q/C8813QV100R001C92B196; 480*854; CTC/2.0) AppleWebKit/534.30 (KHTML, like Gecko) Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; HUAWEI C8813Q Build/HuaweiC8813Q) UC AppleWebKit/534.31 (KHTML, like Gecko) Mobile Safari/534.31',
        'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI 4W Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.85 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.2.5',
        'Mozilla/5.0 (Linux; Android 6.0.1; MI 4W Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; HUAWEI C8813Q Build/HuaweiC8813Q) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.9 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; HTC_D820u Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; Android 4.4.4; HTC D820u Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.89 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-CN; HTC D820u Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.1.0.527 U3/0.8.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Android; Mobile; rv:35.0) Gecko/35.0 Firefox/35.0',
        'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; HTC D820u Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.6 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; HTC D820u Build/KTU84P) AppleWebKit/534.24 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.24 T5/2.0 baidubrowser/5.3.4.0 (Baidu; P1 4.4.4)',
        'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; HTC D820u Build/KTU84P) AppleWebKit/535.19 (KHTML, like Gecko) Version/4.0 LieBaoFast/2.28.1 Mobile Safari/535.19',
        'Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080',
        'Mozilla/5.0 (Linux; Android 5.1.1; vivo Xplay5A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1.1)',
        'Mozilla/5.0 (Linux; Android 6.0; LEX626 Build/HEXCNFN5902606111S) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/7.4 baiduboxapp/8.3.1 (Baidu; P1 6.0)',
        'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; ZUK Z2121 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.8.952 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM-C7000 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.2.948 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
        'Mozilla/5.0 (Linux; Android 5.1; m3 note Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1)',
        'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; SM-G9550 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.0.953 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; ZUK Z2121 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.8.952 Mobile Safari/537.36',
        'MQQBrowser/5.3/Mozilla/5.0 (Linux; Android 6.0; TCL 580 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/4G Language/zh_CN',
        'Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 wxwork/2.1.3 MicroMessenger/6.3.22',
        'Mozilla/5.0 (Linux; Android 5.1; m3 note Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 wxwork/2.1.3 MicroMessenger/6.3.22',
        'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; C106 Build/ZAXCNFN5902606201S) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.0.953 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 6.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 6.0)',
        'Mozilla/5.0 (Linux; Android 7.0; EVA-AL00 Build/HUAWEIEVA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN',
        'Mozilla/5.0 (Linux; U; Android 7.1.2; zh-cn; MI 5X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.2.2',
        'Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; EVA-DL00 Build/HUAWEIEVA-DL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 4.4.4; HM NOTE 1LTE Build/KTU84P; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_6.6.9_482_YYB_D QQ/6.6.9.3060 NetType/WIFI WebP/0.3.0 Pixel/720',
        'Mozilla/5.0 (Linux; Android 5.1; OPPO R9m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080',
        'Mozilla/5.0 (Linux; Android 5.1; vivo X6Plus D Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080',
    ]

    return choice(PHONE_HEADERS)


def get_base_headers():
    """
    得到一个基本的headers
    :return:
    """
    return {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': get_random_pc_ua(),
        'accept': '*/*'
    }


def dict_cookies_2_str(dict_cookies):
    """
    dict类型cookies转str
    :param dict_cookies:
    :return:
    """
    cookie = [str(key) + "=" + str(value) for key, value in dict_cookies.items()]
    str_cookies = ';'.join(item for item in cookie)

    return str_cookies


def is_ipv4(ip):
    """
    判断是否为ipv4地址
    :param ip:
    :return: bool
    """
    try:
        socket.inet_aton(ip)
    except socket.error:
        return False

    return True


def is_ipv6(ip):
    """
    判断是否为ipv6地址
    :param ip:
    :return: bool
    """
    try:
        socket.inet_pton(socket.AF_INET6, ip)
    except socket.error:
        return False

    return True


def get_local_free_port():
    """
    随机获取一个可以被绑定的空闲端口
    :return: int
    """
    with closing(socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)) as s:
        s.bind(('127.0.0.1', 0))
        _, port = s.getsockname()

    return port


def html_entities_2_standard_html(html_body):
    """
    将html实体名称/实体编号转为html标签
    :param html_body:
    :return:
    """
    char_entities = (
        ('&nbsp;', ' '),
        ('&#160;', ' '),
        ('&lt;', '<'),
        ('&#60;', '<'),
        ('&gt;', '>'),
        ('&#62;', '>'),
        ('&amp;', '&'),
        ('&#38;', '&'),
        ('&quot;', '"'),
        ('&#34;', '"'),
    )

    for item in char_entities:
        html_body = html_body.replace(item[0], item[1])

    return html_body


def driver_cookies_list_2_str(cookies_list: list) -> str:
    """
    driver的cookies list 转 str
    :param cookies_list: eg: [{"domain":".jianshu.com", "expirationDate":1552467568.95627, ..., "name":"_m7e_session_core", ..., "value":"cc5871cc6fd05e742b83fbf476676450",}, ...]
    :return:
    """
    res = ''
    for item in cookies_list:
        name = item.get('name', '')
        value = item.get('value', '')
        if name != '':
            res += '{}={};'.format(name, value)

    return res
