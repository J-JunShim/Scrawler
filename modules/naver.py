from bs4 import BeautifulSoup as _bs

from modules.driver import Driver
from modules.utils import urltools, iotools, timestamp


def url_gen_list(clubid, menuid, page):
    url = 'https://apis.naver.com/cafe-web/cafe2/ArticleList.json'
    queries = {'search.clubid': clubid, 'search.menuid': menuid,
               'search.page': page, 'userDisplay': 20}

    return urltools.url_gen(url, queries)


def url_gen_read(clubid, articleid):
    url = f'https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/{clubid}/articles/{articleid}'

    return url


class CafeArticle:
    def __init__(self, article, menu, cafe):
        self.id = article
        self.menu = menu
        self.cafe = cafe
        self.title = None
        self.author = None
        self.date = None
        self.content = None
        self._comments = []

    def get_article_to_dict(self):
        self.article = dict(
            id=self.id,
            menu=self.menu,
            cafe=self.cafe,
            title=self.title,
            author=self.author,
            date=self.date.isoformat(),
            content=self.content)

        return self.article

    def get_comments_to_dict(self):
        return self._comments

    def set_from_json(self, data):
        article = data['article']
        comments = data['comments']
        contentHTML = article['contentHtml']
        contentDom = _bs(contentHTML, 'html.parser')

        self.title = article['subject']
        self.author = article['writer']['id']
        date = article['writeDate']
        self.date = timestamp.millisecond_to_datetime(date)
        self.content = contentDom.get_text(strip=True)

        for comment in comments['items']:
            self._set_comment(comment)

    def _set_comment(self, data):
        name = data['writer']['id']
        text = data['content']
        date = data['updateDate']
        date = timestamp.millisecond_to_datetime(date)

        comment = dict(id=self.id, cafe=self.cafe, name=name,
                       date=date.isoformat(), text=text)

        self._comments.append(comment)

    def save_article(self, file):
        data = self.get_article_to_dict()

        iotools.write_in_csv(file, data)

    def save_comment(self, file):
        dataset = self.get_comments_to_dict()

        for data in dataset:
            iotools.write_in_csv(file, data)


class CafeDriver(Driver):
    def __init__(self):
        super().__init__()
        self.cookieFile = "./data/naver_cafe-user.json"

    def load_cookie(self):
        self.cookies = iotools.load_from_json(self.cookieFile)

        self.login()
        self.set_cookie()

    def save_cookie(self):
        self.get_cookie()

        iotools.save_in_json(self.cookieFile, self.cookies)

    def login(self):
        url = 'https://nid.naver.com/'

        self.request(url)

    def get_article_list(self, url):
        target = 'id', 'main-area'

        self.request(url)
        self.driver.switch_to.frame('cafe_main')
        self.wait(target)

        elements = self.driver.find_elements(
            'css selector', 'div.article-board div.board-number')

        return [int(element.text) for element in elements]

    def get_article_read(self, url):
        target = 'css selector', 'div.ArticleContentBox'

        self.request(url)
        self.driver.switch_to.frame('cafe_main')
        self.wait(target)

        element = self.driver.find_element(*target)

        return element.get_attribute('innerHTML')
