from pathlib import Path
from multiprocessing import Pool

from progress import spinner as spin

from modules import datestamp, news, urltools


class Scraper:
    def __init__(self, query, date, selector) -> None:
        self.query = query
        self.date = date
        self.selector = selector
        self.path = Path().absolute() / 'data'
        self.spinner = spin.MoonSpinner('Scraping ')

    def scrap(self):
        with Pool(4) as pool:
            pool.map(self.worker, self.get_url(100))

    def worker(self, urls):
        try:
            for url in urls:
                self.get_article(url)
        except:
            pass
        else:
            self.spinner.next()

    def get_url(self, end):
        for start in range(end):
            url = urltools.search_naver(
                self.query, start=start * 10, ds=self.date, de=self.date)

            yield urltools.get_href(url, self.selector)

    def get_article(self, url):
        value = news.article_to_dict(url)

        if value:
            news.dict_to_json(value, self.path, self.date.strftime('%Y%m%d'))


if __name__ == '__main__':
    keyword = '코로나'
    select = 'div.news_area > a'

    for i in range(5, 10):
        date = datestamp.get_date_days(i)
        scraper = Scraper(keyword, date, select)

        scraper.scrap()
