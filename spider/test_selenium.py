# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from PIL import Image
import time

from selenium import webdriver
from selenium.webdriver import ActionChains


def new_driver():
    driver = webdriver.Chrome('/users/zhaojm/ides/chromedriver/chromedriver')
    driver.implicitly_wait(1)  # seconds
    driver.maximize_window()
    return driver


def get_img(div_list, filename):
    sub_list = []
    for div in div_list:
        style = div.get_attribute('style')
        img_url = style.split('"')[1]
        pos_x = style.split(';')[1].split(':')[1].split()[0][:-2]
        pos_y = style.split(';')[1].split(':')[1].split()[1][:-2]
        sub_list.append({
            "url": img_url,
            "x": int(pos_x),
            "y": int(pos_y)
        })
        pass
    # print sub_list

    import requests
    image = sub_list[0].get("url")
    ir = requests.get(image, stream=True)
    if ir.status_code == 200:
        with open('%s.webp' % filename, 'wb') as f:
            for chunk in ir:
                f.write(chunk)

    l = len(sub_list)
    im = Image.open('%s.webp' % filename)
    w, h = im.size

    resultImg = Image.new('RGBA', (l / 2 * 10, h), (0, 0, 0, 0))
    for index, sub in enumerate(sub_list):
        region = im.crop(box=(
            -sub.get('x'),
            -sub.get("y"),
            -sub.get('x') + 10,
            -sub.get('y') + h / 2
        ))
        resultImg.paste(region, box=(
            index % (l / 2) * 10,
            sub.get("y") + 58,
            index % (l / 2) * 10 + 10,
            sub.get('y') + 58 + h / 2
        ))
    resultImg.save("%s.png" % filename)


def is_pixel_equal(im1, im2, x, y):
    pixel1 = im1.getpixel((x, y))
    pixel2 = im2.getpixel((x, y))
    print "p1,p2: (%d, %d)" % (x, y)
    print pixel1
    print pixel2
    for i in range(0, 3):
        if abs(pixel1[i] - pixel2[i]) > 50:
            return False
    return True


def get_diff_x(im1, im2):
    w1, h1 = im1.size
    w2, h2 = im2.size
    for x in range(0, w1):
        for y in range(0, h1):
            if not is_pixel_equal(im1, im2, x, y):
                return x
    return -1


def main():
    driver = new_driver()
    driver.get("http://127.0.0.1:5000")  # 访问首页
    time.sleep(2)
    btn = driver.find_element_by_id("popup-submit")  # 找到按钮
    btn.click()  # 点击按钮,显示验证码框
    time.sleep(1)

    # 这里获取第一张图片,拼装第一张图片
    div_list = driver.find_elements_by_css_selector('div[class="gt_cut_fullbg_slice"]')
    print "div_list len: ", len(div_list)
    get_img(div_list=div_list, filename='fullbg')
    # 拿到第二张图片
    div_list = driver.find_elements_by_css_selector('div[class="gt_cut_bg_slice"]')
    print "div_list len: ", len(div_list)
    get_img(div_list=div_list, filename='bg')
    #  计算移动位置
    im1 = Image.open('fullbg.png')
    im2 = Image.open('bg.png')
    x = get_diff_x(im1, im2)
    print "diff: ", x

    # 找到滑块
    btn1 = driver.find_element_by_css_selector('div[class="gt_slider_knob gt_show"]')
    action_chains = ActionChains(driver)
    # action_chains.click_and_hold(btn1) # 按住滑块
    # action_chains.perform()
    # action_chains.move_by_offset(x - 5, 0)
    # # action_chains.perform()
    # time.sleep(1)
    # action_chains.release()

    action_chains.drag_and_drop_by_offset(btn1, x - 5, 0)
    action_chains.perform()

    print "over and sleeping..."
    time.sleep(10000)


if __name__ == "__main__":
    main()
