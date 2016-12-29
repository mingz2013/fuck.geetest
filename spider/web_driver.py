# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config import implicitly_wait

from selenium.webdriver.common.proxy import Proxy, ProxyType


def new_webdriver(proxy_type, proxy_ip, proxy_port):
    # 使用phantomjs
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
    )
    service_args = [
        '--proxy=%s:%s' % (proxy_ip, proxy_port),
        '--proxy-type=%s' % proxy_type,
    ]
    # driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
    # driver = webdriver.PhantomJS(desired_capabilities=dcap)

    # 使用firefox
    proxy_str = "%s:%s" % (proxy_ip, proxy_port)
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': proxy_str,
        'ftpProxy': proxy_str,
        'sslProxy': proxy_str,
        'noProxy': ''
    })
    driver = webdriver.Firefox(proxy=proxy)

    # 使用chrome
    # driver = webdriver.Chrome()

    driver.implicitly_wait(implicitly_wait)  # seconds

    driver.maximize_window()  # 窗口最大化, 这一步很重要,否则响应式网页,有部分菜单自动隐藏,访问不到
    return driver
