# -*- coding: utf-8 -*-
# @Author: Xusen
# @Date:   2017-06-26 11:28:40
# @Last Modified by:   Xusen
# @Last Modified time: 2017-06-28 22:26:42
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import logging
import re
import time


logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


class QQMailSpider(object):

    def __init__(self):
        self.CHROMEDRIVE = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
        self.options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(
            self.CHROMEDRIVE, chrome_options=self.options)
        self.browser.maximize_window()
        self.mail_sender = []
        self.mail_sender_addr = []
        self.mail_subject = []
        self.mail_time = []

    def login(self):
        self.browser.get('https://mail.qq.com/')
        logging.info("等待登陆")
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
        WebDriverWait(self.browser, 1000).until(
            lambda driver: driver.find_element_by_id('readmailbtn_link').is_displayed())  # 等待登陆完成
        self.browser.find_element_by_xpath(
            "//a[@id='readmailbtn_link']").click()  # 进入收件箱

    def logout(self):
        self.browser.switch_to_default_content()
        self.browser.find_element_by_xpath("//*[@id='SetInfo']/div[1]/a[@target='_parent']").click()
        self.browser.quit()
        logging.info("注销登陆，浏览器退出！")

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


    def __switch_to_iframe(self, iframe_name, timeout=10):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.find_element_by_id(iframe_name).is_displayed())
        self.browser.switch_to.frame(iframe_name)

if __name__ == '__main__':
    spider = QQMailSpider()
    spider.login()
    spider.mailInfo()
    spider.logout()
