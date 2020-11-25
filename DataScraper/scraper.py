from pathlib import Path
from multiprocessing import Manager, Process, Queue, Pool

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

        try:
            create.start()
            work.start()
        except KeyboardInterrupt:
            pass
        finally:
            que. close()
            create.join()
            work.join()

        article = list(filter(None, article))

        if news.dict_to_json(article, path):
            print('\nProcess complite!!')

    def creator(self, que):
        spinner = spin.MoonSpinner('Scraping ')

        with Pool() as pool:
            for page in range(100):
                urls = pool.apply(self.get_url, [page])
                map(que.put, urls)
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
            self.query, start=start * 10, ds=self.date, de=self.date)

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
