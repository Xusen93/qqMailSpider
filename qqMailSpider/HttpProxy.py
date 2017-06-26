# -*- coding: utf-8 -*-
# @Author: Xusen
# @Date:   2017-06-25 13:53:35
# @Last Modified by:   Xusen
# @Last Modified time: 2017-06-26 11:22:56
import requests
import logging
logging.basicConfig(level=logging.INFO)
import random


class HttpProxy(object):
    """docstring for HttpProxy"""

    def __init__(self):
        self.setProxyApi('http://api.xicidaili.com/')
        logging.info('initializing HttpProxy')
        self.refreshProxy()

    def refreshProxy(self):
        self.proxyList = requests.get(self.proxyApi).text.split('\r\n')

    def setProxyApi(self, proxyApi):
        self.proxyApi = proxyApi

    def getProxy(self):
        logging.info('get a proxy http:')
        return random.choice(self.proxyList)


if __name__ == '__main__':
    proxy = HttpProxy()
    print(proxy.getProxy())