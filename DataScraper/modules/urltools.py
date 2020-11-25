import requests as _requests

from urllib import parse as _parse
from bs4 import BeautifulSoup as _BeautifulSoup

from . import datestamp


def get_href(url, selector):
    urls = []
    response = _requests.get(url)

    if response.ok:
        document = _BeautifulSoup(response.text, 'html.parser')
        urls = [a.get('href') for a in document.select(selector)]

    return urls


def parse_url(url):
    unquoted = _parse.unquote(url)

    return _parse.urlparse(unquoted)


def get_query(parsed):
    return _parse.parse_qs(parsed.query)


def make_url(parsed, queries):
    encoded = _parse.urlencode(queries)
    url = _parse.SplitResult(scheme=parsed.scheme, netloc=parsed.netloc,
                             path=parsed.path, query=encoded, fragment=parsed.fragment)

    return url.geturl()


def search_naver(query, start=0, sort='acc', ds=None, de=None):
    parsed = parse_url('https://search.naver.com/search.naver')

    sort = {'acc': 0, 'new': 1, 'old': 2}.get(sort)
    nso = dict(
        so='r', p=f'from{datestamp.dt_format(ds)}to{datestamp.dt_format(de)}', a='all')
    nso = _parse.urlencode(nso).replace('=', ':').replace('&', ',')
    queries = dict(where='news', query=query, sort=sort, nso=nso, start=start)

    return make_url(parsed, queries)
