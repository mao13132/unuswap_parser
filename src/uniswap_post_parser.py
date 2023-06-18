import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UniswapPostPars:
    def __init__(self, driver, links_post):
        self.driver = driver
        self.source_name = 'Uniswap'
        self.links_post = links_post
        self.post_data = {}

    def load_page(self, url):
        try:


            self.driver.get(url)
            return True
        except Exception as es:
            print(f'Ошибка при заходе на "{url}" "{es}"')
            return False

    def __check_load_page(self, name_post):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "{name_post[:-3]}")]')))
            return True
        except Exception as es:
            print(f'Ошибка при загрузке "{name_post}" поста "{es}"')
            return False

    def loop_load_page(self, post):
        coun = 0
        coun_ower = 10

        while True:
            coun += 1

            if coun >= coun_ower:
                print(f'Не смог зайти в пост {post["name_post"]}')
                return False

            response = self.load_page(post['link'])

            if not response:
                continue

            result_load = self.__check_load_page(post['name_post'])

            if not result_load:
                self.driver.refresh()
                return False

            return True

    def get_theme(self):
        try:
            theme = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'title-wrapper')]"
                                                                f"//*[contains(@class, 'category-name')]").text

        except:
            theme = ''

        return theme

    def get_author(self):
        try:
            author = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'topic-body')]"
                                                                 f"//*[contains(@class, 'username')]").text

        except:
            author = ''

        return author

    def get_text_post(self):
        try:
            text_post = self.driver.find_element(by=By.XPATH, value=f""
                                                                    f"//*[contains(@class, 'topic-owner')]"
                                                                    f"//*[contains(@class, 'topic-body')]"
                                                                    f"//*[contains(@class, 'regular contents')]"
                                                                    f"//*[@class='cooked']").text

        except:
            text_post = ''

        return text_post

    def get_like(self):
        try:
            like = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'topic-owner')]"
                                                               f"//*[contains(@class, 'topic-map')]"
                                                               f"//*[contains(@class, 'likes')]").text


        except:
            like = '0'

        try:
            like = like.split('\n')[0]
        except:
            like = '0'

        if like == '':
            like = '0'

        return like


    def get_row_comments(self):
        try:
            rows_comm = self.driver.find_elements(by=By.XPATH, value=f"//*[(contains(@class, 'topic-post')) and (not(contains(@class, 'owner')))]")
        except Exception as es:
            print(f'Не могу получить комментарии "{es}"')
            return []

        return rows_comm

    def get_author_comment(self, comm):
        try:
            author_comment = comm.find_element(by=By.XPATH, value=f".//*[contains(@class, 'names')]").text

        except:
            author_comment = ''

        return author_comment

    def get_date_comment(self, comm):
        try:
            date_comment = comm.find_element(by=By.XPATH, value=f".//*[contains(@class, 'post-date')]").text

        except:
            date_comment = ''

        return date_comment

    def get_text_comment(self, comm):
        try:
            text_comment = comm.find_element(by=By.XPATH, value=f".//*[contains(@class, 'cooked')]").text

        except:
            text_comment = ''

        return text_comment

    def get_likes_comments(self, comm):
        try:
            likes_comment = comm.find_element(by=By.XPATH, value=f".//*[contains(@class, 'like')]").text

        except:
            likes_comment = ''

        return likes_comment

    def itter_rows_comm(self, rows_comm, post):

        comments_list = []

        for comm in rows_comm:
            comment_dict = {}

            author_comment = self.get_author_comment(comm)
            if author_comment == '':
                continue

            comment_dict['name_comment'] = author_comment

            time_comment = self.get_date_comment(comm)
            comment_dict['time_comment'] = time_comment

            text_comment = self.get_text_comment(comm)
            comment_dict['text_comment'] = text_comment

            like = self.get_likes_comments(comm)
            comment_dict['like'] = like

            comments_list.append(comment_dict)


        post['comments'] = comments_list

        return True


    def job_comments(self, post):
        rows_comm = self.get_row_comments()

        response_itter = self.itter_rows_comm(rows_comm, post)


    def start_pars(self):
        for count, post in enumerate(self.links_post):

            result_load_page = self.loop_load_page(post)

            if not result_load_page:
                continue

            name_them = self.get_theme()
            post['name_them'] = name_them

            name_author = self.get_author()
            post['name_author'] = name_author

            text_post = self.get_text_post()
            post['text_post'] = text_post

            like = self.get_like()
            post['like'] = like

            list_comments = self.job_comments(post)


        return self.links_post

