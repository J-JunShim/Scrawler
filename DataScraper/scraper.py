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


def worker(url):
    try:
        result = DataTools.article_to_dict(url)

        if result:
            print(result['body'][0])
    except:
        print(url)
        result = None

    return result


def main():
    select = 'div.news_area > a'
    pages = 5

    obj = []
    urls = [make_url_naver('코로나', 2, page * 10) for page in range(pages)]

    with Pool(cpu_count()) as pool:
        for _, url in enumerate(urls):
            print(_)
            href = pool.apply(DataTools.get_href, (url, select))
            obj.extend(pool.map(worker, href))

    if DataTools.dict_to_json(obj, '../data/test.json'):
        print('All process complite!!')


if __name__ == '__main__':
    main()
