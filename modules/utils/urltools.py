from urllib import parse as _parse


def url_gen(url, query: dict) -> str:
    parsed = _parse.urlparse(url)
    query = query_gen(query)
    url = _parse.SplitResult(scheme=parsed.scheme, netloc=parsed.netloc,
                             path=parsed.path, query=query, fragment=parsed.fragment)

    return url.geturl()


def query_gen(query) -> str:
    encoded = _parse.urlencode(query)
    query = _parse.unquote(encoded)

    return query
