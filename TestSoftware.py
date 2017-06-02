# -*- coding: utf-8 -*-
import time
from urllib import request, parse
from http.client import RemoteDisconnected
from browseBase import browseBase
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebdriverWait
#from selenium.webdriver.support import expected_conditions

#本クラスにテスト対象のWebアプリの操作を記述する
class TestSoftware(browseBase):

    def google_search(self, keyword = "Test"):
        self.webdriver.get("https://www.google.co.jp/")
        self.webdriver.find_element_by_id("lst-ib").click()
        self.webdriver.find_element_by_id("lst-ib").clear()
        self.webdriver.find_element_by_id("lst-ib").send_keys(keyword)

        self.waitParallelRun()

        self.webdriver.find_element_by_id("lst-ib").click()
        self.webdriver.find_element_by_id("lst-ib").send_keys("\n")

        self.takeScreenshot(self.gi)


    def test_osrestart(self):
        self.waitParallelRun()

        try:
            src = request.urlopen('http://192.168.0.1:5000/restart').read()
        except RemoteDisconnected as rd:
            print(rd)

    def test_printid(self):
        try:
            details = parse.urlencode( { 'id': self.testid } )
            binary_details = details.encode('ascii')
            URL = request.Request( 'http://192.168.0.1:5000/printid/', binary_details )
            response = request.urlopen(URL).read().decode( 'utf8', 'ignore' )
            print(response)
        except RemoteDisconnected as rd:
            print(rd)