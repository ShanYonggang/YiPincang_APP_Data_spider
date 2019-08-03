#  采用Appium和mitmproxy联合爬取壹品仓APP商品数据信息并保存至MongoDB数据库中

import sys
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from config import *

class Action():
    def __init__(self):
        '''初始化'''
        # 配置驱动
        self.desired_caps = {
            "platformName": platformName,
            "deviceName": deviceName,
            "appPackage": "com.ypcang.android.shop",
            "appActivity": "com.ypcang.android.shop.activity.commen_activity.MainTabActivity"
        }
        self.driver = webdriver.Remote(driver_server, self.desired_caps)
        self.wait = WebDriverWait(self.driver, timeout=timeout)
        self.all_banners = []
        self.type = sys.getfilesystemencoding()

    def click_get_info(self):
        # 点击进入某个品牌的详细界面
        size = self.driver.get_window_size()
        x1 = size['width']*0.5
        y1 = size['height']*0.75
        y2 = size['height']*0.55
        try:
            banner_info = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.ypcang.android.shop:id/tvTitle')))
            sleep(1)
            banner_text = banner_info[0].text
            print(banner_text.encode(self.type).decode('GBK', 'ignore'))
            if banner_text in self.all_banners:
                self.driver.swipe(x1,y1,x1,y2,500)
                print('The banner has been saved')
                self.click_get_info()
            else:
                self.all_banners.append(banner_text)
                banner_info[0].click()
        except NoSuchElementException:
            print('Can not find this elements!')

    def scroll(self):
        size = self.driver.get_window_size()
        x1 = size['width']*0.5
        y1 = size['height']*0.75
        y2 = size['height']*0.25
        y3 = size['height']*0.5
        while True:
            try:
                self.driver.swipe(x1,y1,x1,y2,500)
                # 获取商品的信息（为了判断停止下滑按钮）
                try:
                    texts = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'android.widget.TextView')))
                    if texts[len(texts)-1].text == '-仓主，没有更多了-':
                        # 结束该品牌商品信息获取，返回首页
                        back = self.driver.find_element_by_id('com.ypcang.android.shop:id/imgBack')
                        back.click()
                        # 下滑获取下一个品牌的商品信息
                        try:
                            self.driver.swipe(x1,y1,x1,y3,500) 
                            break
                        except WebDriverException:
                            print('The banner is loading,Please Wait a moment!')
                            sleep(2)
                            self.driver.swipe(x1,y1,x1,y3,500) 
                            break
                except NoSuchElementException:
                    print('Go on slide!')
            except WebDriverException:
                print('The Service request is so quick,Please Wait a moment!')
                sleep(2)

    def main(self):
        while True:
            self.click_get_info()
            self.scroll()
            try:
                if self.driver.find_element_by_id('com.ypcang.android.shop:id/rvBanner'):
                    break
            except NoSuchElementException:
                print('Start get nextone banner goods!')
            else:
                break

if __name__ == '__main__':
    click = Action()
    click.main()