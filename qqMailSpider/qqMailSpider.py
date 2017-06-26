# -*- coding: utf-8 -*-
# @Author: Xusen
# @Date:   2017-06-26 11:28:40
# @Last Modified by:   Xusen
# @Last Modified time: 2017-06-26 18:01:52
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import os
import time
import sys
import logging
import datetime
import requests

logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


class QQMailSpider(object):
    """docstring for QQMailSpider"""

    def __init__(self):
        self.CHROMEDRIVE = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
        self.options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(
            self.CHROMEDRIVE, chrome_options=self.options)
        self.browser.maximize_window()

    def login(self):
        self.browser.get('https://mail.qq.com/')
        logging.info("Waiting login")
        # self.browser.switch_to.frame('login_frame')
        # self.browser.find_element_by_xpath(
        #     "//div/a[@id='switcher_plogin']").click()
        # self.username = input("Please input your email count:")
        # self.browser.find_element_by_xpath(
        #     "//input[@id='u']").send_keys(self.username)
        # self.passwd = input("Please input the password:")
        # self.browser.find_element_by_xpath(
        #     "//input[@id='p']").send_keys(self.passwd)
        # if self.browser.find_element_by_xpath("//*[@id='verifyArea']").is_displayed():
        #     self.verifycode = input("Please input the verifycode:")
        #     self.browser.find_element_by_xpath(
        #         "//input[@id='verifycode']").send_keys(self.verifycode)
        # time.sleep(1)
        # # self.browser.find_element_by_xpath(
        # #     "//input[@id='login_button']").click()

    def mailInfo(self):
        WebDriverWait(self.browser, 1000).until(
            lambda driver: driver.find_element_by_id('readmailbtn_link').is_displayed())
        self.browser.find_element_by_xpath(
            "//a[@id='readmailbtn_link']").click()  # 进入收件箱
        self.__switch_to_iframe('mainFrame')
        mailListUrlBase = self.browser.execute_script(
            'return document.location.href').split('page=0')
        page_index = 0
        mailListUrl = ('page='+str(page_index)).join(mailListUrlBase)
        p = self.browser.page_source
        with open('p.html', 'w', encoding='gb18030') as f:  # qq邮箱网页编码为gb18030
            f.write(p.encode('gb18030').decode('gb18030'))
            f.close()

    def __switch_to_iframe(self, iframe_name, timeout=10):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.find_element_by_id(iframe_name).is_displayed())
        self.browser.switch_to.frame(iframe_name)

if __name__ == '__main__':
    spider = QQMailSpider()
    spider.login()
    spider.mailInfo()
