from decorators import get_thread_name
from bs4 import BeautifulSoup

class YeeyanParser:
    def __init__(self):
        self.name = 'yeeyan'

    def __str__(self):
        return self.name

    def set_database(self, database):
        self.database = database

    def extract_urls(self, dom):
        article_divs = dom.find_all('div', class_='y_space_article')
        article_urls = [article_div.h3.a['href'] for article_div in article_divs]
        return article_urls

    @get_thread_name
    def parse(self, url, html_page):
        dom = BeautifulSoup(html_page)
        urls = self.extract_urls(dom)
        for url in urls:
            print url
            self.database.insert(thread_name=self.name, table='extracted_urls', values=(url,))
        self.database.commit(thread_name=self.name)

def get_parser():
    return YeeyanParser()
