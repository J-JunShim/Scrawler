import DataTools

from multiprocessing import Manager, Process, Pool, cpu_count
from itertools import repeat
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def make_url_naver(query, sort, start):
    def _dt_format(dt): return dt.strftime('%Y%m%d')

    now = datetime.now()
    ds = now - relativedelta(year=now.year - 1)
    de = now - timedelta(days=1)

    url = 'https://search.naver.com/search.naver?where=news'

    sort = [0, 1, 2][sort]
    dse = f"from{_dt_format(ds)}to{_dt_format(de)}"
    nso = f'so%3Add%2Cp%3A{dse}%2Ca%3Aall'

    url += f'&query={query}&sort={sort}&nso={nso}&start={start}&refresh_start=0'

    return url


def creator(queue, pages, select):
    hrefs = []
    with Pool(cpu_count()) as pool:
        urls = [make_url_naver('코로나', 2, page * 10) for page in range(pages)]
        for _, url in enumerate(urls):
            print(_)
            hrefs.extend(pool.apply(DataTools.get_href, (url, select)))
        pool.map(queue.put, hrefs)


def worker(queue):
    url = queue.get()

    try:
        result = DataTools.article_to_dict(url)

        if result:
            print(result['body'][0])
    except:
        pass


def main():
    select = 'div.news_area > a'

    manager = Manager()
    que = manager.Queue()

    proc1 = Process(target=creator, args=(que, 10, select))
    proc1.start()
    proc1.join()

    with Pool(cpu_count()) as pool:
        while not que.empty():
            pool.apply(worker, (que, ))



if __name__ == '__main__':
    main()
