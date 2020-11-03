import requests as _requests

from bs4 import BeautifulSoup as _BeautifulSoup
from newspaper import Article as _Article


def get_href(url, selector):
    urls = []
    request = _requests.get(url)

    if request.ok:
        document = _BeautifulSoup(request.text, 'html.parser')
        urls = [a.get('href') for a in document.select(selector)]

    return urls


def get_article(url):
    article = _Article(url, language='ko')

    if article.is_valid_url:
        article.download()
        article.parse()

    if not article.is_parsed:
        article = None

    return article


def article_to_dict(url):
    article = get_article(url)

    if not article.is_valid_url():
        return {}

    url = article.url
    title = article.title
    text = article.text
    publish_date = article.publish_date

    return {'url': url, 'date': publish_date, 'body': [title, text]}
