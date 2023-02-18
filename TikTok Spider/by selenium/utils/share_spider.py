from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from random import randint
import time

DEFAULT_SHARE_BTN_XPATH = '//*[@id="root"]/div/div[2]/div/div/div[1]/div[1]/div[3]/div/div[2]/div[1]/div[4]'
DEFAULT_SHARE_MSG_XPATH = '//*[@id="root"]/div/div[2]/div/div/div[1]/div[1]/div[3]/div/div[2]/div[1]/div[4]/div/div/div/div[1]/div/img'
DEFAULT_NEXT_BTN_XPATH = '//*[@id="root"]/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/xg-bar[3]/div[1]/div/div/div[2]'
DEFAULT_LOGINED_XPATH = '//*[@id="root"]/div/div[1]/div/header/div[2]/div[2]/div/div/div[2]/div/li/a/div'


class ShareSpider():

    def __init__(self,
                 start_url,
                 driver_name,
                 driver_executable_path,
                 spider_duration=60 * 60 * 24,
                 next_after_second=5,
                 share_btn_xpath=DEFAULT_SHARE_BTN_XPATH,
                 share_msg_xpath=DEFAULT_SHARE_MSG_XPATH,
                 next_btn_xpath=DEFAULT_NEXT_BTN_XPATH,
                 logined_xpath=DEFAULT_LOGINED_XPATH,
                 shares_saved_path='./shares.txt'):
        assert (driver_name
                in ('Edge', 'Chrome'), 'driver_name must Edge or Chrome!')
        self.start_url = start_url
        self.driver = getattr(
            webdriver, driver_name)(executable_path=driver_executable_path)
        self.next_after_second = next_after_second
        self.spider_duration = spider_duration
        self.share_btn_xpath = share_btn_xpath
        self.share_msg_xpath = share_msg_xpath
        self.next_btn_xpath = next_btn_xpath
        self.logined_xpath = logined_xpath
        self.shares_saved_path = shares_saved_path

    def get_element_until(self, xpath, second=10):
        return WebDriverWait(self.driver, second).until(
            EC.presence_of_element_located((By.XPATH, xpath)))

    def get_element(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    def wait(self, second=3):
        time.sleep(second)

    def close(self):
        if hasattr(self, 'log'):
            self.log.close()
        self.driver.close()
        self.driver.quit()

    def start(self):
        self.driver.get(self.start_url)
        self.log = open(self.shares_saved_path, 'a', encoding='utf-8')

    def write(self, share_msg):
        self.log.write(share_msg + '\n')

    def get_now_time(self):
        return time.time()

    def run(self):
        try:
            print('-' * 20 + ' Share Clawing ' + '-' * 20)
            self.start()

            self.wait(2)
            print('Please login your account.')
            # login fail will throw a error
            self.get_element_until(self.logined_xpath, 60)
            print('Login successfully.')

            start_time = time.time()
            now_time = start_time
            clawed_count = 0
            while now_time - start_time < self.spider_duration:
                self.wait(1)
                self.get_element_until(self.share_btn_xpath).click()
                share_msg = self.get_element_until(
                    self.share_msg_xpath).get_attribute('alt')
                self.write(share_msg)

                self.wait(
                    randint(self.next_after_second,
                            self.next_after_second + 3))
                self.get_element_until(self.next_btn_xpath).click()

                now_time = self.get_now_time()
                clawed_count += 1
                print('clawed_count: %s\r' % clawed_count, end='')

            self.wait(1)
            print('clawed_count: %s' % clawed_count)

        except:
            print('There is something wrong.')

        finally:
            self.close()
            print('Crawling finish.')


if __name__ == '__main__':
    spider = ShareSpider('https://www.douyin.com/video/6995844232653163806',
                         'Edge', 'msedgedriver.exe', 30)
    spider.run()
