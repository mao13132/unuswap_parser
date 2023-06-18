from browser.createbrowser import CreatBrowser
from src.UniswapParser import UniswapParser

def main():

    filter_24_date = True

    filter_count_day = 1

    browser_core = CreatBrowser()

    print(f'Парсер запущен. Захожу на сайт')

    response_job = UniswapParser(browser_core.driver, filter_24_date, filter_count_day).start_pars()

    print(f'Работу закончил. Сохранил \n{response_job}.xlsx\n{response_job}.json')


if __name__ == '__main__':
    main()
