# -*- coding: utf-8 -*-
#from selenium.webdriver.firefox.webdriver import Webdriver
#from selenium.webdriver.common.action_chains import ActionChains
import time, unittest, datetime, locale
from selenium import webdriver
import QAtestType
from TestSoftware import TestSoftware

def is_alert_present(wd):
    try:
        wd.switch_to_alert().text
        return True
    except:
        return False

class QASeleniumTest(unittest.TestCase):
    def setUp(self):
        # スナップショットやログ記録用のID取得
        #self.testid = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
        self.testid0 = datetime.datetime.today().strftime("%m%d-%H%M")
        self.testid = self.testid0 + "00"
        self.testid1 = self.testid0 + "01"
        self.testid2 = self.testid0 + "02"

    def test_google_search(self):
        success = True
        print(self.testid)
        sw = TestSoftware(self.testid)
        sw.google_search()
        
        self.assertTrue(success)

    def test_google_search_limit(self):
        success = True
        print(self.testid)
        sw = TestSoftware(self.testid)
        sw.google_search("99999999999999999999999999999999999999999999999999")
        
        self.assertTrue(success)

    def test_google_search_irregular(self):
        success = True
        print(self.testid)
        sw = TestSoftware(self.testid)
        sw.google_search("ν")
        
        self.assertTrue(success)

    def test_google_search_serial(self):
        success = True
        print(self.testid)
        sw = TestSoftware(self.testid)
        QAtestType.serialRun([lambda : ()], [sw.google_search])
        
        self.assertTrue(success)

    def test_google_search_parallel(self):
        success = True
        print(self.testid1)
        print(self.testid2)
        sw1 = TestSoftware(self.testid1)
        sw2 = TestSoftware(self.testid2)
        QAtestType.parallelRun(sw1, sw2, [sw1.google_search], None, [sw2.google_search], None)
        
        self.assertTrue(success)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()