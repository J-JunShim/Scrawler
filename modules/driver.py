from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support import ui, expected_conditions
from selenium.webdriver.common import keys, alert


class Driver:
    def __init__(self):
        self.cookies = None
        self.driver = None

    @staticmethod
    def now():
        now = datetime.now()
        print(f'[{now.isoformat()}]', end=' ')

        return now

    def start_driver(self, *args):
        options = webdriver.EdgeOptions()

        for arg in args:
            options.add_argument(arg)

        options.add_argument('inprivate')
        # options.add_argument('headless')
        options.add_argument("disable-gpu")
        options.add_argument('--no-sandbox')
        options.add_argument('--mute-audio')
        options.add_argument('--blink-settings=imagesEnabled=false')

        self.driver = webdriver.Edge(options=options)

        self.driver.implicitly_wait(10)

        return self.driver

    def close_driver(self):
        self.driver.close()

    def get_cookie(self):
        self.cookies = self.driver.get_cookies()

    def set_cookie(self):
        self.now()
        print('Add cookies:', end=' ')

        for cookie in self.cookies:
            print(cookie.get('name'), end=', ')
            self.driver.add_cookie(cookie)
        print()

    def request(self, url):
        self.driver.get(url)
        self.now()
        print('Request to', url)

    def script(self, script):
        self.driver.execute_script(script)

    def alert(self):
        try:
            alert.Alert(self.driver).accept()
        except:
            pass

    def wait(self, target):
        wait = ui.WebDriverWait(self.driver, 10)
        ec = expected_conditions.presence_of_element_located(
            target)

        wait.until(ec)

    def insert_values(self, form, name, values):
        element = form.find_element('name', name)

        element.clear()
        element.send_keys(values)

    def select_value(self, form, name, value):
        element = form.find_element('name', name)
        select = ui.Select(element)

        select.select_by_value(value)
