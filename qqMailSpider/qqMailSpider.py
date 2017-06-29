# -*- coding: utf-8 -*-
# @Author: Xusen
# @Email:  xusenthu@qq.com
# @Date:   2017-06-26 11:28:40
# @Last Modified by:   Xusen
# @Last Modified time: 2017-06-29 16:36:45
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import logging
import re
import time
import json
import os
import thulac


logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


class QQMailSpider(object):

    def __init__(self):
        self.CHROMEDRIVE = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
        self.options = webdriver.ChromeOptions()
        self.mail_sender = []
        self.mail_sender_addr = []
        self.mail_subject = []
        self.mail_time = []

    def run(self):
        logging.info("启动QQ邮箱爬虫...")
        self.browser = webdriver.Chrome(
            self.CHROMEDRIVE, chrome_options=self.options)
        self.browser.maximize_window()
        self.login()
        self.mailInfo()
        self.logout()
        self.info2json()

    def login(self):
        self.browser.get('https://mail.qq.com/')
        logging.info("等待登陆，请进入浏览器页面登陆QQ邮箱")
        WebDriverWait(self.browser, 1000).until(
            lambda driver: driver.find_element_by_id('readmailbtn_link').is_displayed())  # 等待登陆完成
        self.browser.find_element_by_xpath(
            "//a[@id='readmailbtn_link']").click()  # 进入收件箱

    def logout(self):
        self.browser.switch_to_default_content()
        self.browser.find_element_by_xpath(
            "//*[@id='SetInfo']/div[1]/a[@target='_parent']").click()
        self.browser.quit()
        logging.info("已注销，浏览器退出！")

    def mailInfo(self):
        self.__switch_to_iframe('mainFrame')
        page_end = re.match(
            r'(\d+)/(\d+)\s', self.browser.find_element_by_xpath("//div[@class='right']").text).group(2)
        logging.info('共有 %s 页邮件' % page_end)
        for page_index in range(0, int(page_end)):  # range(0,5)=[0,1,2,3,4]
            logging.info('正在读取第 %s 页邮件' % str(page_index+1))
            for mailList in self.browser.find_elements_by_xpath("//td[@class='cx']/input"):
                self.mail_sender.append(mailList.get_attribute("fn"))
                self.mail_sender_addr.append(mailList.get_attribute("fa"))
                self.mail_time.append(mailList.get_attribute("totime"))
            for mailList in self.browser.find_elements_by_xpath("//div[@class='tf no']/u"):
                self.mail_subject.append(mailList.text)
            while True:
                if page_index == int(page_end)-1:
                    break
                try:
                    self.browser.find_element_by_xpath(
                        "//*[@id='nextpage1']").click()
                    if self.browser.find_element_by_xpath("//*[@id='maillistjump']").is_displayed():
                        break
                except Exception as e:
                    waitTime = 3
                    logging.info('频率太快了！等待 %ds后重试' % waitTime)
                    time.sleep(waitTime)
                    self.browser.find_element_by_xpath(
                        "//div/input[@class='btn']").click()
        logging.info("邮件信息读取完毕！")

    def info2json(self):
        jslist = []
        for i in range(0, len(self.mail_sender)):
            jslist.append({
                'sender': self.mail_sender[i],
                'from': self.mail_sender_addr[i],
                'time': self.mail_time[i],
                'subject': self.mail_subject[i],
            })
            self.json = json.dumps(jslist)
        with open('info.json', 'w') as f:
            f.write(self.json)
        logging.info("邮件信息已存至 info.json 中")

    def json2info(self):
        pass

    def __switch_to_iframe(self, iframe_name, timeout=10):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.find_element_by_id(iframe_name).is_displayed())
        self.browser.switch_to.frame(iframe_name)


def wordSplit():
    pass

if __name__ == '__main__':
    spider = QQMailSpider()
    if not os.path.exists('info.json'):
        spider.run()
