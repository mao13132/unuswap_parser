import time

import json

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from save_result import SaveResult
from src.uniswap_post_parser import UniswapPostPars


class UniswapParser:
    def __init__(self, driver, filter_24_date, count_day_filter):
        self.driver = driver
        self.url = f'https://gov.uniswap.org/latest?order=activity'
        self.source_name = 'Uniswap'
        self.links_post = []
        self.filter_24_date = filter_24_date
        self.count_day_filter = count_day_filter

    def load_page(self, url):
        try:
            self.driver.get(url)
            return True
        except Exception as es:
            print(f'Ошибка при заходе на стартовую страницу "{es}"')
            return False

    def __check_load_page(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'sign-up-button')]")))
            return True
        except:
            # print(f'Ошибка при загрузке стартовой страницы страницы')
            return False






    def load_start_site(self):
        pass
        # start_page = self.load_page(self.url)
        #
        # if not start_page:
        #     return False
        #
        # check_page = self.__check_load_page()
        #
        # if not check_page:
        #     return False
        #
        # print(f'Успешно зашёл на {self.source_name}')
        #
        # return True

    def loop_load_page(self):
        count = 0
        count_ower = 10


        while True:

            count += 1

            if count >= count_ower:
                print(f'Не смог открыть {self.source_name}')
                return False

            start_page = self.load_page(self.url)

            if not start_page:
                continue

            check_page = self.__check_load_page()

            if not check_page:
                self.driver.refresh()
                continue

            print(f'Успешно зашёл на {self.source_name}')

            return True


    def get_all_post(self):
        try:
            rows_post = self.driver.find_elements(by=By.XPATH,
                                 value=f"//table[contains(@class, 'topic-list')]//tr")
        except Exception as es:
            print(f'Ошибка при получение постов"{es}"')
            return False

        return rows_post

    def get_date(self, row):
        try:
            date = row.find_element(by=By.XPATH, value=f".//*[contains(@class, 'relative-date')]").text
        except:
            date = ''

        return date

    def filter_date(self, date_post):
        if 'ч' in date_post or 'h' in date_post:
            return True

        if 'd' in date_post:
            try:
                coun_day = date_post.replace('d', '')
                coun_day = int(coun_day)
            except:
                return True
            if coun_day <= self.count_day_filter:
                return True


        if 'дн' in date_post:
            try:
                coun_day = int(date_post.split()[0])
            except:
                return True
            if coun_day <= self.count_day_filter:
                return True

        return False

    def get_name_post(self, row):
        try:
            name_post = row.find_element(by=By.XPATH, value=f".//a[contains(@class, 'title')]").text
        except:
            name_post = ''

        return name_post

    def get_link(self, row):
        try:
            link_post = row.find_element(by=By.XPATH, value=f".//a[contains(@class, 'title')]").get_attribute('href')
        except:
            link_post = ''

        return link_post

    def get_link(self, row):
        try:
            link_post = row.find_element(by=By.XPATH, value=f".//a[contains(@class, 'title')]").get_attribute('href')
        except:
            link_post = ''

        return link_post

    def get_views(self, row):
        try:
            views_post = row.find_element(by=By.XPATH, value=f".//*[contains(@class, 'views')]").text
        except:
            views_post = ''

        return views_post

    def itter_rows_post(self, rows_post):

        for row in rows_post[1:]:

            date_post = self.get_date(row)

            date_result = self.filter_date(date_post)

            if not date_result:
                continue

            name_post = self.get_name_post(row)

            link = self.get_link(row)

            views_post = self.get_views(row)

            good_itter = {}

            good_itter['name_post'] = name_post
            good_itter['link'] = link
            good_itter['views_post'] = views_post
            good_itter['date_post'] = date_post

            self.links_post.append(good_itter)



    def step_one_parse(self):

        rows_post = self.get_all_post()

        if not rows_post:
            return False

        response = self.itter_rows_post(rows_post)

        print(f'Обнаружил {len(self.links_post)} постов')

        return True


    def save_to_json(self, filename):

        filename = f'{filename}.json'

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.links_post, file, indent=4, ensure_ascii=False)
        except:
            return False

        return filename

    def start_pars(self):
        result_start_page = self.loop_load_page()

        if not result_start_page:
            return False

        response_one_step = self.step_one_parse()

        # from .temp import temp_list as links_post

        # good_pars_row = UniswapPostPars(self.driver, links_post).start_pars()
        good_pars_row = UniswapPostPars(self.driver, self.links_post).start_pars()

        file_name = f'{datetime.now().strftime("%H_%M_%S")}'

        file_name_exel = SaveResult(good_pars_row).save_file(file_name)

        file_name_json = self.save_to_json(file_name)

        return True



