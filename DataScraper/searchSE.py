import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class SearchImage:
    def __init__(self, keyword, path=None):
        self.query = '+'.join(keyword.split(' '))
        self.path = path

    @staticmethod
    def progress_bar(value, endvalue, stamp, bar_length=50):
        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write('\rPercent: [{0}] {1}%  Time: {2}'.format(
            arrow + spaces, int(round(percent * 100)), time.strftime('%M:%S', time.gmtime(stamp))))
        sys.stdout.flush()

    @staticmethod
    def sel_driver(url):
        print('Collecting images...')

        driver = webdriver.Chrome()
        driver.get(url)

        return driver

    @staticmethod
    def closed_sel_windows(driver):
        for window in driver.window_handles:
            driver.switch_to_window(window)
            driver.close()

    def naver_image(self, n_round=10, down=True):
        tic = time.time()
        url = f'https://search.naver.com/search.naver?where=image&query={self.query}'

        driver = self.sel_driver(url)
        driver.find_element_by_css_selector(
            'div.photo_grid div.img_area').click()

        srcList = list()
        for n in range(n_round):
            try:
                dom = BeautifulSoup(driver.page_source, 'lxml')
                srcList.extend([_['src'] for _ in dom.select(
                    'div.viewer img') if _.has_attr('src')])

                self.progress_bar(n+1, n_round, time.time()-tic)

                try:
                    driver.find_element_by_css_selector(
                        'div.viewer_content a.btn_next span').click()
                except NoSuchElementException:
                    driver.find_element_by_css_selector(
                        'a.btn_more').click()
                except:
                    pass
            except KeyboardInterrupt:
                print('\nStop collecting!')
                break

        self.closed_sel_windows(driver)

        srcList = set(srcList)
        self.save_imgs(srcList, self.query, self.path)

    def daum_image(self, n_round=10, down=True):
        tic = time.time()
        url = f'https://search.daum.net/search?w=img&enc=utf8&q={self.query}'

        driver = self.sel_driver(url)
        driver.find_element_by_css_selector(
            'div.cont_img div.wrap_thumb').click()

        srcList = []
        for n in range(n_round):
            try:
                dom = BeautifulSoup(driver.page_source, 'lxml')
                srcList.extend([_['src'] for _ in dom.select(
                    'div.cont_viewer div.inner_thumb img:last-child') if _.has_attr('src')])

                self.progress_bar(n+1, n_round, time.time()-tic)

                try:
                    driver.find_element_by_css_selector('a.btn_next').click()
                except NoSuchElementException as e:
                    driver.find_element_by_css_selector(
                        'a.expender.open').click()
                    driver.find_elements_by_css_selector(
                        'div.cont_img div.wrap_thumb')[n].click()
                except:
                    pass
            except KeyboardInterrupt:
                print('\nStop collecting!')
                break

        self.closed_sel_windows(driver)
        srcList = set(srcList)
        self.save_imgs(srcList, self.query, self.path)

    def google_image(self, down=True):
        import json

        tic = time.time()
        url = f'https://www.google.com/search?q={self.query}&tbm=isch'

        driver = self.sel_driver(url)

        last_height = driver.execute_script(
            'return document.body.scrollHeight')
        while True:
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')

            time.sleep(0.5)

            new_height = driver.execute_script(
                'return document.body.scrollHeight')
            if new_height == last_height:
                try:
                    driver.find_element_by_css_selector('input#smb').click()
                except:

                    break
            last_height = new_height

        dom = BeautifulSoup(driver.page_source, 'lxml')
        self.closed_sel_windows(driver)
        srcList = {json.loads(_.text)['ou'] for _ in dom.find_all(
            'div', {'class': 'rg_meta'})}

        stamp = time.time() - tic
        print('Time: ', time.strftime('%M:%S', time.gmtime(stamp)))

        self.save_imgs(srcList, self.query, self.path)
