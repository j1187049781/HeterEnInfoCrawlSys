# coding: utf-8
import urllib2
import cv2
import numpy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def curl_gt_img(browser,img_name):

    browser.get('http://www.gsxt.gov.cn/index.html')

    element = WebDriverWait(browser, 1000) \
        .until(EC.presence_of_element_located((By.ID, "keyword")))
    elem = browser.find_element_by_id('keyword')  # Find the search box
    elem.send_keys('selenium')
    time.sleep(2)
    elem.send_keys(Keys.ENTER)
    img = WebDriverWait(browser, 10) \
        .until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_item_img")))
    time.sleep(2)
    imgurl = img.get_attribute('src')

    req = urllib2.Request(imgurl)
    res = urllib2.urlopen(req).read()
    img = numpy.asarray(bytearray(res), dtype='uint8')
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    img.shape
    cv2.imwrite(img_name, img)


if __name__=='__main__':
    start=201
    img_num=202
    browser = webdriver.Safari()
    try:
        for i in range(start,img_num):
            name='./data/{}.jpg'.format(i)
            curl_gt_img(browser,name)
    finally:
        browser.quit()
