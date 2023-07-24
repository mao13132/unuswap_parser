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

    def get_comment(self, count):

        good_list = []

        for count_it in range(count):

            try:
                rows_comm = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@class, 'topic-post')]")
            except:
                return good_list

            if rows_comm == []:
                return good_list

            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except:
                return good_list

            time.sleep(2)

            if good_list == []:
                good_list.extend(rows_comm)
                continue

            old_id = [elem.id for elem in good_list]

            for row in rows_comm:
                if not row.id in old_id:
                    good_list.append(row)

        return good_list

    def get_row_comments(self):
        try:

            rows_comm = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@class, 'topic-post')]")


        except Exception as es:
            print(f'Не могу получить комментарии "{es}"')
            return []

        if len(rows_comm) == 1:
            return []

        return rows_comm[1:]

    def get_author_comment(self, comm):
        try:
            author_comment = comm.find_element(by=By.XPATH, value=f".//*[contains(@class, 'names')]").text

        except:
            try:
                author_comment = comm.text.split('\n')[0]

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
            return 0

        if likes_comment == '':
            return 0

        return likes_comment

    def itter_rows_comm(self, rows_comm, post):

        comments_list = []

        # print(f'Начинаю обработку {len(rows_comm)}')

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

        post['comments'].extend(comments_list)

        return True

    def try_element_itter(self, old_list):
        good_list = []

        for elem in old_list:

            try:
                good_list.append(elem.id)
            except:
                continue

        return good_list

    def job_comments(self, post):
        old_elem = []
        post['comments'] = []

        # rows_comm = self.get_comment(5)
        _count_try = 3

        for cont_tru in range(_count_try):

            # temp_list = []

            rows_comm = self.get_row_comments()

            if rows_comm == []:
                return old_elem

            if old_elem == []:
                old_elem.extend(rows_comm)
                temp_list = rows_comm
            else:
                temp_list = []

                old_id = self.try_element_itter(old_elem)

                for row in rows_comm:
                    if not row.id in old_id:
                        temp_list.append(row)
                        old_elem.append(row)

            if temp_list == []:
                return True

            response_itter = self.itter_rows_comm(temp_list, post)

            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except:
                continue

            time.sleep(2)

        print(f'Собрал {len(post["comments"])} комментариев')

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
