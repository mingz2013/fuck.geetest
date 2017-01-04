# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from selenium.webdriver import ActionChains
import time


class MyActionChains(ActionChains):
    def __init__(self, driver):
        ActionChains.__init__(self, driver)

    def sleep(self, seconds):
        self._actions.append(lambda: time.sleep(seconds))
        return self
