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
    result = None
    article = get_article(url)

    if article:
        article.nlp()

        url = article.url
        title = article.title
        text = article.text
        summary = article.summary
        publish_date = article.publish_date.isoformat()

        result = dict(url=url, date=publish_date, body=[title, text, summary])

    return result


def dict_to_json(data, path, name):
    p = _Path().cwd() / path / f"{name}.jsonl"

    if p.parent.is_dir() and data:
        with open(p, 'a', encoding='utf-8') as f:
            f.write(_json.dump(data, f, ensure_ascii=False)+'\n')

    return p.exists()
