from pathlib import Path
from itertools import repeat
from multiprocessing import Manager, Process, Queue
from tqdm import tqdm
from progress import spinner as spin, bar

from modules import datestamp, news, urltools


class Scraper:
    def __init__(self, query, date, selector) -> None:
        self.query = query
        self.date = date
        self.selector = selector

    def generate_href(self, start):
        url = urltools.search_naver(
            self.query, start=start, ds=self.date, de=self.date)

        return urltools.get_href(url, self.selector)

    def creator(self, que):
        page = 0

        spinner = spin.MoonSpinner('Scraping ')

        while True:
            start = page * 10

            try:
                urls = self.generate_href(start)
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

    @staticmethod
    def worker(que, article):
        url = que.get()
        value = None

        try:
            value = news.article_to_dict(url)
        except:
            pass

        if value:
            article.append(value)

    def scrap(self):
        article = []

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


def main(i):
    keyword = '코로나'
    select = 'div.news_area > a'

    date = datestamp.get_date(i)
    scraper = Scraper(keyword, date, select)

    scraper.scrap()


if __name__ == '__main__':
    for i in range(5, 10):
        main(i)

    # with Pool() as pool:
    #     pool.map(main, range(5, 10))

    # procs = []
    # for i in range(5, 10):
    #     date = datestamp.get_date(i)
    #     # naver.scrap()
    #     try:
    #         scraper = Scraper(keyword, date, select)
    #         proc = Process(target=scraper.scrap)
    #     except:
    #         continue
    #     else:
    #         procs.append(proc)
    #         proc.start()

    # for proc in procs:
    #     proc.join()
