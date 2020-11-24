from pathlib import Path
from itertools import repeat
from multiprocessing import Process, Pool, cpu_count
from tqdm import tqdm
from progress import spinner as spin, bar

from modules import datestamp, news, urltools


class Scraper:
    def __init__(self, query, date, selector) -> None:
        self.query = query
        self.date = date
        self.selector = selector

    def creator(self):
        urls = []
        urlsLen = 0
        page = 0

        spinner = spin.MoonSpinner('Scraping ')

        while True:
            start = page * 10

            try:
                url = urltools.search_naver(
                    self.query, start=start, ds=self.date, de=self.date)

                for href in urltools.get_href(url, self.selector):
                    if not href:
                        continue
                    urls.append(href)
            except KeyboardInterrupt:
                break
            else:
                if len(urls) <= urlsLen:
                    break
                else:
                    page += 1
                    urlsLen = len(urls)
            finally:
                spinner.next()

        return urls

    @staticmethod
    def worker(url):
        value = None
        try:
            value = news.article_to_dict(url)
        except:
            pass

        if value:
            return value

    def scrap(self):
        article = []
        date = self.date.strftime('%Y%m%d')
        root = Path().absolute() / 'data'
        path = root / f"{date}.json"

        print('Process start!!')

        urls = set(self.creator())
        with Pool(cpu_count()) as pool:
            article.extend(pool.map(self.worker, tqdm(urls)))
            
        if news.dict_to_json(article, path):
            print('\nProcess complite!!')


if __name__ == '__main__':
    date = datestamp.get_date(1)
    keyword = '코로나'
    select = 'div.news_area > a'

    naver = Scraper(keyword, date, select)
    # naver.scrap()
    proc = Process(target=naver.scrap)

    proc.start()
    proc.join()
