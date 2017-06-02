# -*- coding: utf-8 -*-
import os, sys, time, datetime
import urllib.error
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

class browseOperationListener(AbstractEventListener):
    def after_click(self, element, driver):
        #return super().after_click(element, driver)
        #result = True
        #while True::
        #   result = element.click()
        #   print(result)
        self.gi = self.generateInteger()
        self.testid = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
        time.sleep(2)
        dirname = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshot")
        filepath = os.path.join(dirname, self.testid + "-" + str(self.gi.__next__()) + ".jpg")
        driver.save_screenshot(filepath)

    def generateInteger(self):
        #連番を取得できるジェネレータ
        #スナップショットの番号付け用
        i = 0
        while True:
            i += 1
            yield i

class browseBase(object):
    def __init__(self, testid, width = 1000, height = 800, vertical = 0, horizontal = 0):
        #Seleniumで操作するブラウザを指定
        self.width = width
        self.height = height
        self.vertical = vertical
        self.horizontal = horizontal

        #self.webdriver = EventFiringWebDriver(webdriver.Ie("C:\Program Files (x86)\Python36-32\IEDriverServer.exe"), browseOperationLister())
        self.webdriver = webdriver.Ie("C:\Program Files (x86)\Python36-32\IEDriverServer.exe")
        self.webdriver.implicitly_wait(60)
        self.webdriver.set_window_position(self.vertical, self.horizontal)
        self.webdriver.set_window_size(self.width, self.height)

        self.testid = testid
        self.gi = self.generateInteger()

        self.value = None

    def __del__(self):
        #操作完了後にブラウザを閉じる
        try:
            self.webdriver.quit()
        except urllib.error.URLError as ue:
            print(ue.reason)
            print("testcaseid:" + self.testid)

    def __getstate__(self):
        #重複操作時にコード情報を子プロセスに引き渡すが、
        #コンストラクタで取得したプロパティは文字列以外は子プロセスに引き渡せないので、
        #いったん破棄する
        self.webdriver.quit()
        state = self.__dict__.copy()
        del state['webdriver']
        del state['gi']
        return state

    def __setstate__(self, state):
        #子プロセスが開始されたときに、
        #破棄されたプロパティを再度取得しなおす
        self.__dict__.update(state)
        self.webdriver = webdriver.Ie("C:\Program Files (x86)\Python36-32\IEDriverServer.exe")
        self.webdriver.set_window_position(self.vertical, self.horizontal)
        self.webdriver.set_window_size(self.width, self.height)
        self.gi = self.generateInteger()

    def generateInteger(self):
        #連番を取得できるジェネレータ
        #スナップショットの番号付け用
        i = 0
        while True:
            i += 1
            yield i

    def takeScreenshot(self, generateInteger):
        time.sleep(2)
        dirname = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshot")
        filepath = os.path.join(dirname, self.testid + "-" + str(self.gi.__next__()) + ".jpg")
        self.webdriver.save_screenshot(filepath)
        #self.webdriver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + "0")

    def parallelRunChild(self, d, key, value, e1, e2, Func, afterFunc = lambda : ()):
        #重複操作時にそれぞれの子プロセスで前処理を実施するまで待機

        self.e2 = e2
        self.d = d
        self.key = key
        self.value = value

        if key == 'Func2' :
            e1.wait()
        FuncRun = [ f() for f in Func]
        afterFunc()
        self.__del__()

    def waitParallelRun(self):
        print(sys._getframe().f_back.f_code.co_name)

        if sys._getframe().f_back.f_code.co_name == self.value :
            self.d[self.key] = self.value
            self.e2.wait()