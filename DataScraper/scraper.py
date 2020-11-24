from pathlib import Path
from itertools import repeat
from multiprocessing import Manager, Process, Queue, Pool
from tqdm import tqdm
from progress import spinner as spin, bar

from modules import datestamp, news, urltools


class Scraper:
    def __init__(self, query, date, selector) -> None:
        self.query = query
        self.date = date
        self.selector = selector

    def scrap(self):
        date = self.date.strftime('%Y%m%d')
        root = Path().absolute() / 'data'
        path = root / f"{date}.json"

        print('Process start!!')

        que = Queue()
        manager = Manager()
        article = manager.list()

        create = Process(target=self.creator, args=[que])
        work = Process(target=self.worker, args=[que, article])

        create.start()
        work.start()
        que. close()
        create.join()
        work.join()

        article = list(filter(None, article))

        if news.dict_to_json(article, path):
            print('\nProcess complite!!')

    def creator(self, que):
        page = 0
        spinner = spin.MoonSpinner('Scraping ')

        while True:
            start = page * 10

            try:
                urls = self.get_url(start)
            except KeyboardInterrupt:
                break
            else:
                if urls:
                    map(que.put, urls)
                else:
                    break
            finally:
                page += 1
                spinner.next()

    def worker(self, que, article):
        proc = []

        while que.empty():
            url = que.get()
            p = Process(target=self.get_article, args=[url, article])
            p.start()

        for p in proc:
            p.join()

    def get_url(self, start):
        url = urltools.search_naver(
            self.query, start=start, ds=self.date, de=self.date)

        return urltools.get_href(url, self.selector)

    @staticmethod
    def get_article(url, article):
        value = news.article_to_dict(url)

        if value:
            article.append(value)


def main(i):
    keyword = '코로나'
    select = 'div.news_area > a'

    date = datestamp.get_date(i)
    scraper = Scraper(keyword, date, select)

    scraper.scrap()


if __name__ == '__main__':
    for i in range(5, 10):
        main(i)
