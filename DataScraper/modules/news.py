import json as _json

from pathlib import Path as _Path
from newspaper import Article as _Article


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
    article.nlp()

    url = article.url
    title = article.title
    text = article.text
    summary = article.summary
    publish_date = article.publish_date.isoformat()

    return dict(url=url, date=publish_date, body=[title, text, summary])


def dict_to_json(data, path):
    p = _Path().cwd() / path

    if p.parent.is_dir():
        with open(p, 'w', encoding='utf-8') as f:
            _json.dump(data, f, ensure_ascii=False)

    return p.exists()
