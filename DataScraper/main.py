from . import DataTools

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def make_url(query, sort, start):
    now = datetime.now()
    ds = now - relativedelta(year=now.year - 1)
    de = now - timedelta(days=1)

    where = 'news'
    sms = ['jum', 'pge', 'srt', 'opt'][3]
    sm = f'tab_{sms}'
    sort = [0, 1, 2][sort]
    dse = f"from{ds.strftime('%Y%m%d')}to{de.strftime('%Y%m%d')}"
    nso = f'so%3Add%2Cp%3A{dse}%2Ca%3Aall'

    url = f'https://search.naver.com/search.naver?where={where}&query={query}&sm={sm}&sort={sort}&nso={nso}&start={start}'

    return url


def craw(page):
    select = 'div.news_area > a'
    url = make_url('코로나', 2, page * 10)

    return DataTools.get_href(url, select)
