#coding=utf-8
'''
命令行启动方式：appium -a 127.0.0.1 -p 4723 --session-override
'''
import time
from selenium import webdriver
# from appium import webdriver
from tools.usefulTools import userfulToolsFactory
from conf import settings
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import random

el_not_find = '控件未找到，控件名称：'

class Base():
    driver = None
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['noReset'] = True
    # desired_caps['platformVersion'] = '4.3'
    # desired_caps['deviceName'] = '50a4c97e'
    desired_caps['platformVersion'] = settings.platformVersion
    desired_caps['deviceName'] = settings.deviceName
    # desired_caps['platformVersion'] = '5.1'
    # desired_caps['deviceName'] = 'A10SBNGTQJ9M'
    # desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['appPackage'] = settings.appPackage
    desired_caps['appActivity'] = settings.appActivity
    desired_caps['unicodeKeyboard'] = True
    desired_caps['resetKeyboard'] = True
    desired_caps['chromeOptions'] = {'androidProcess': 'com.tencent.mm:appbrand0'}

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    # driver.find_element().is_displayed()

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            # self.fall = True
            return True
        else:
            return False


class BasicAction():
    #单个控件查找
    def find_element(self,locate):
        randomStr = str(random.randint(1, 1000000))

        file_name = locate[0] + '_failed_'+ randomStr
        file = settings.get_pic_file_path() + '//'+file_name + '.png'
        for case in switch(locate[1]):
            if case('id'):
                try:
                    element = Base.driver.find_element_by_id(str(locate[2]))
                    print (locate[0] + '-控件--已找到，查找方式：id')
                except Exception as reason:
                    print (reason)
                    print (locate[0] + el_not_find + locate[2])
                    print (u'当前查找操作随机数：' + randomStr)
                    Base.driver.save_screenshot(file)
                    raise

            if case('name'):
                try:
                    element = Base.driver.find_element_by_name(locate[2])
                    print (locate[0] + '-控件--已找到，查找方式：NAME')
                except Exception as reason:
                    print (reason)
                    print (locate[0] + el_not_find + locate[2])
                    print (u'当前查找操作随机数：' + randomStr)
                    Base.driver.save_screenshot(file)
                    raise

            if case('class_name'):
                try:
                    element = Base.driver.find_element_by_class_name(locate[2])
                    print (locate[0] + '-控件--已找到，查找方式：class_name')
                except Exception as reason:
                    print (reason)
                    print (locate[0] + el_not_find + locate[2])
                    print (u'当前查找操作随机数：' + randomStr)
                    Base.driver.save_screenshot(file)
                    raise

            if case('xpath'):
                try:
                    element = Base.driver.find_element_by_xpath(locate[2])
                    print (locate[0] + '-控件--已找到，查找方式：xpath')
                except Exception as reason:
                    print (reason)
                    print (locate[0] + el_not_find + locate[2])
                    print (u'当前查找操作随机数：' + randomStr)
                    Base.driver.get_screenshot_as_file(file)
                    raise

            return element

    #获取到控件列表
    def find_elements(self,locate):
        randomStr = str(random.randint(1, 1000000))
        file_name = locate[0] + '_find_failed_' + randomStr
        file = settings.get_pic_file_path() + '//'+file_name + '.png'
        for case in switch(locate[1]):
            if case('id'):
                try:
                    elements = Base.driver.find_elements_by_id(str(locate[2]))
                    print (locate[0] + '-控件--已找到，查找方式：id')
                except Exception as reason:
                    print (reason)
                    print (locate[0] + el_not_find + locate[2])
                    print (u'当前查找操作随机数：' + randomStr)
                    Base.driver.save_screenshot(file)
                    raise

            if case('name'):
                try:
                    elements = Base.driver.find_elements_by_name(locate[2])
                    print (locate[0] + '-控件--已找到，查找方式：NAME')
                except Exception as reason:
                    print (reason)
                    print (locate[0] + el_not_find + locate[2])
                    print (u'当前查找操作随机数：' + randomStr)
                    Base.driver.save_screenshot(file)
                    raise

            if case('class_name'):
                try:
                    elements = Base.driver.find_elements_by_class_name(locate[2])
                    print (locate[0] + '-控件--已找到，查找方式：class_name')
                except Exception as reason:
                    print (reason)
                    print (locate[0] + el_not_find + locate[2])
                    print (u'当前查找操作随机数：' + randomStr)
                    Base.driver.save_screenshot(file)
                    raise

            if case('xpath'):
                try:
                    elements = Base.driver.find_elements_by_xpath(locate[2])
                    print ()
                except Exception as reason:
                    print (reason)
                    print (locate[0] + el_not_find + locate[2])
                    print (u'当前查找操作随机数：' + randomStr)
                    Base.driver.get_screenshot_as_file(file)
                    raise
            return elements

basicAction = BasicAction()

class element_Operate():
    #找到控件并进行点击
    def element_click(self,locate):
        randomStr = str(random.randint(1, 1000000))

        file_name = locate[0] + '_click_failed_' + randomStr
        file = settings.get_pic_file_path() + '//' + file_name + '.png'
        try:
            element = basicAction.find_element(locate)
            element.click()
            sleep(2)
            # Base.driver.implicitly_wait(60)
        except Exception as reason:
            print (reason)
            print ('点击操作失败,控件名称：' + locate[0])
            print (u'当前点击操作随机数：' + randomStr)
            Base.driver.save_screenshot(file)
            raise

    #多个控件的点击操作
    def elements_click(self, locate, elements_id = None):
        try:
            elements = basicAction.find_elements(locate)
            #根据传入的ID判断是否单独的点击一个控件
            if elements_id==0 or elements_id:
                element = elements[int(elements_id)]
                element.click()
            else:
                elements_id = len(elements)
                while(elements_id > 0):
                    element = elements[elements_id-1]
                    print (element)
                    element.click()
                    elements_id = elements_id -1
                    sleep(2)
            # Base.driver.implicitly_wait(60)
        except Exception as reason:
            print (reason)
            print ('点击操作失败,控件名称：' + locate[0])
            raise

    #实现找到控件，并进行右键点击
    def element_right_hand_click(self,locate):
        try:
            element = basicAction.find_element(locate)
            # element.click()
            ActionChains(Base.driver).context_click(element).perform()
            sleep(2)
        except Exception as reason:
            print (reason)
            print ('右键点击操作失败,控件名称：' + locate[0])
            raise

    #找到控件进行双击
    def element_double_click(self,locate):
        try:
            element = basicAction.find_element(locate)
            element.double_click()
            sleep(2)
        except Exception as reason:
            print (reason)
            print ('点击操作失败,控件名称：' + locate[0])

    #找到控件，进行内容清除
    def elemet_clear(self,locate):
        try:
            element = basicAction.find_element(locate)
            element.clear()
            sleep(1)
        except Exception as reason:
            print (reason)
            print ('清空操作失败,控件名称：' + locate[0])

    #找到控件，进行内容输入
    def element_send_keys(self,locate,context):
        try:
            self.locate = locate
            element = basicAction.find_element(self.locate)
            element.clear()
            # 部分手机出现:clear() 无法完全删除内容的情况，切换清除内容方法，计算内容长度，循环删除
            # 进行内容删除操作
            locate_input_text = element.get_attribute('text')
            element.click()
            # 光标移动到末尾
            Base.driver.press_keycode(123)
            # element.clear()
            for i in range(len(locate_input_text)):
                # 点击删除按钮
                Base.driver.press_keycode(67)
            element.click()
            #进行内容输入操作
            element.send_keys(context)
            # element.set_value(context)
            Base.driver.implicitly_wait(30)
        except Exception as reason:
            print (reason)
            print ('输入内容失败,控件名称：' + locate[0])

    def element_display_commit(self,locate):
        try:
            self.locate = locate
            element = basicAction.find_element(self.locate)
            element.is_displayed()
            return True
        except Exception as reason:
            return False
            # print (reason)
            # print '检查的控件未找到,控件名称：' + locate[0]

    def element_save_pic(self,file_name):
        file = settings.get_pic_file_path() + '//'+ file_name + '.png'
        Base.driver.get_screenshot_as_file(file)

    #等待控件并点击
    def wait_element_click(self,locate,file_name=None):
        randomStr = str(random.randint(1, 1000000))
        if file_name:
            print (u'当前截图名称：'+file_name)
        else:
            file_name = str(locate[0])
            print (u'当前截图名称：'+str(locate[0]))
        for wait_cycle in range(5):
            if element_Operate.element_display_commit(self,locate):
                print (u'控件已找到，进行点击操作，控件信息：'+str(locate[0]))
                element_Operate.element_click(self,locate)
                element_Operate.element_save_pic(self,file_name+'_done_'+randomStr)
                return 0
            else:
                print (u'控件未找到，进行等待5s处理，当前等待时间：'+str(wait_cycle*5 + wait_cycle*2))
                if wait_cycle ==4:
                    print (u'已等待30s，未找到控件，进行异常处理，控件信息：'+ str(locate[0]))
                    element_Operate.element_save_pic(self, file_name + '_fail_' + randomStr)
                    raise(u'已等待30s，未找到控件，进行异常处理')
                sleep(5)
                continue

    #发送物理按钮操作


def test():
    return 0

if __name__ == '__main__':
    # base = Base()
    test = ['登录输入框','id',"cn.com.egova.egovamobile:id/login_txtUsername"]
    baseFunction = Base()
    print  (test[2])
    # el = baseFunction.find_element(test)
    # el.clear()
    # baseFunction.element_send_keys(test,'test')
    # baseFunction.element_save_pic('d:/','测试')