import requests as _requests

from bs4 import BeautifulSoup as _BeautifulSoup
from newspaper import Article as _Article


def get_href(url, select):
    urls = []
    request = _requests.get(url)

    if request.ok:
        document = _BeautifulSoup(request.text, 'html.parser')
        urls = [a.get('href') for a in document.select(select)]

    return urls


def get_article(url):
    article = _Article(url, language='ko')
    article.download()
    article.parse()

    return article
