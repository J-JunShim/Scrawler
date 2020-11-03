from . import DataTools

from multiprocessing import cpu_count, Process, Manager, Queue
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def make_url_naver(query, sort, start):
    def _dt_format(dt): return dt.strftime('%Y%m%d')

    now = datetime.now()
    ds = now - relativedelta(year=now.year - 1)
    de = now - timedelta(days=1)

    url = 'https://search.naver.com/search.naver?where=news'

    sms = ['jum', 'pge', 'srt', 'opt'][3]
    sm = f'tab_{sms}'
    sort = [0, 1, 2][sort]
    dse = f"from{_dt_format(ds)}to{_dt_format(de)}"
    nso = f'so%3Add%2Cp%3A{dse}%2Ca%3Aall'

    url += f'&query={query}&sm={sm}&sort={sort}&nso={nso}&start={start}&refresh_start=0'

    return url


def creator(queue, url, select):
    urls = DataTools.get_href(url, select)
    for url in urls:
        queue.put(url)
        print()


def worker(queue, results):
    while not queue.empty():
        url = queue.get()
        result = DataTools.article_to_dict(url)

        if result:
            results.append(result)


def main():
    que = Queue()
    manager = Manager()

    results = manager.list()
    select = 'div.news_area > a'

    for page in range(10):
        url = make_url_naver('코로나', 2, page * 10)

        proc1 = Process(target=creator, args=(que, url, select))
        proc2 = Process(target=worker, args=(que, results))

        proc1.start()
        proc1.join()
        proc2.start()
        proc2.join()

        print('page: ', page)

    print(len(results))


if __name__ == '__main__':
    main()
