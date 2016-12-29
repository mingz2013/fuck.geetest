# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from PIL import Image

# from config import userId, password
from captcha import read_img_file_to_string

from web_driver import new_webdriver

driver = new_webdriver()

driver.get(domain)  # 访问首页

driver.switch_to.frame("topFrame")  # 切换到主frame

# 关闭弹窗
float_img_x = driver.find_element_by_xpath('//div[@id="float_icon"]/div/img')
float_img_x.click()

# 搜索
key_word_input = driver.find_element_by_id('key_word')
search_button = driver.find_element_by_xpath('//h3/a')
key_word_input.clear()
key_word_input.send_keys(u"一三")
search_button.click()  # search

# 处理验证码弹窗
code_img = driver.find_element_by_id('MzImgExpPwd')
text_field = driver.find_element_by_id('textfield')
search_button_2 = driver.find_element_by_xpath('//table[@class="k-00-c"]/tbody/tr/td/div/a')

# 处理验证码
while True:
    driver.save_screenshot('1.png')
    im = Image.open('1.png')
    region = im.crop((code_img.location['x'],
                      code_img.location['y'],
                      code_img.location['x'] + code_img.size['width'],
                      code_img.location['y'] + code_img.size['height']))
    # region = region.resize((200, 50), Image.ANTIALIAS)
    region.save('2.png')
    code = read_img_file_to_string('2.png')
    if code != '':
        text_field.clear()
        text_field.send_keys(code)
        search_button_2.click()
        try:
            # 错误弹窗处理
            alert = driver.switch_to.alert()
            if alert:
                alert.accept()
                code_img.click()
                continue
            else:
                break
        except Exception, e:
            # 没有错误弹窗
            break
    else:
        code_img.click()
        continue


# 处理公司详情
def do_company_detail_window():
    # TODO 处理这个窗口的东西
    pass


# 处理公司列表
a_list = driver.find_elements_by_xpath('//div[@class="bx1"]/table/tbody/tr/td/font/a')
for a in a_list:
    a.click()
    h = driver.window_handles[1]
    driver.switch_to.window(h)  # 子窗口
    do_company_detail_window()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])  # 回到搜索页面
    driver.switch_to.frame("topFrame")
# 翻页
tr = driver.find_elements_by_xpath('//div[@class="bx1"]/table/tbody/tr')[-1]
next_page = tr.find_element_by_xpath('./td/a[3]')
next_page.click()
