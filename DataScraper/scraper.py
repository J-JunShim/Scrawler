from pathlib import Path
from multiprocessing import Manager, Process, Queue, Pool

from progress import spinner as spin, bar

from modules import datestamp, news, urltools


class Scraper:
    def __init__(self, query, date, selector) -> None:
        self.query = query
        self.date = date
        self.selector = selector

        self.spinner = spin.MoonSpinner('Scraping ')

    def scrap(self):
        manager = Manager()
        articles = manager.list()
        
        try:
            for page in range(100):
                self._worker(page, articles)
        except KeyboardInterrupt:
            pass

        return list(filter(None, articles))
        

    def _worker(self, page, articles):
        for url in self._get_url(page):
            articles.append(news.article_to_dict(url))
            self.spinner.next()

    def _get_url(self, start):
        url = urltools.search_naver(
            self.query, start=start * 10, ds=self.date, de=self.date)

        return urltools.get_href(url, self.selector)
            


def main(i):
    dataDir = Path().absolute() / 'data'
    keyword = '코로나'
    select = 'div.news_area > a'

    for date in list(map(datestamp.get_date, range(5, 10))):
        print(date.isoformat(), 'Process start!!')

        scraper = Scraper(keyword, date, select)
        path = dataDir / f"{date.strftime('%Y%m%d')}.json"

        if news.dict_to_json(scraper.scrap(), path):
            print('\nProcess complite!!')


if __name__ == '__main__':
    main()
