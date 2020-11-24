from pathlib import Path
from itertools import repeat
from multiprocessing import Manager, Process, Pool, cpu_count
from tqdm import tqdm
from progress import spinner as spin, bar

from modules import datestamp, news, urltools


class Scraper:
    def __init__(self, query, date, selector) -> None:
        self.query = query
        self.date = date
        self.selector = selector

    def generate_href(self, start, urls):
        url = urltools.search_naver(
            self.query, start=start, ds=self.date, de=self.date)
        hrefs = urltools.get_href(url, self.selector)

        map(urls.append, hrefs)

        # return len(hrefs)

    def creator(self):
        page = 0
        urlsLen = 0
        procs = []

        manager = Manager()
        urls = manager.list()
        spinner = spin.MoonSpinner('Scraping ')

        while True:
            start = page * 10
            urlsLen = len(urls)

            try:
                proc = Process(target=self.generate_href, args=(start, urls))
                procs.append(proc)
                proc.start()
            except KeyboardInterrupt:
                break
            else:
                page += 1
            finally:
                spinner.next()

                if len(urls) - 1 >= urlsLen:
                    break

        for proc in procs:
            proc.join()

        return set(urls)

    @staticmethod
    def worker(url, article=None):
        value = None
        try:
            value = news.article_to_dict(url)
        except:
            pass
        return value

    def scrap(self):
        article = []

        date = self.date.strftime('%Y%m%d')
        root = Path().absolute() / 'data'
        path = root / f"{date}.json"

        print('Process start!!')

        urls = set(self.creator())

        with Pool(cpu_count()) as pool:
            article.append(pool.map(self.worker, urls))

        article = list(filter(None, article[0]))
        if news.dict_to_json(article, path):
            print('\nProcess complite!!')


if __name__ == '__main__':
    keyword = '코로나'
    select = 'div.news_area > a'

    procs = []

    for i in range(5, 10):
        date = datestamp.get_date(i)
        # naver.scrap()
        try:
            scraper = Scraper(keyword, date, select)
            proc = Process(target=scraper.scrap)
        except:
            continue
        else:
            procs.append(proc)
            proc.start()

    for proc in procs:
        proc.join()
