from decorators import get_thread_name
from bs4 import BeautifulSoup
import bs4
import re

class YeeyanParser:
    def __init__(self):
        self.name = 'yeeyan'
        self.select_pattern = re.compile(r'http://select.yeeyan.org/view/[0-9]+/[0-9]+')
        self.article_pattern = re.compile(r'http://article.yeeyan.org/view/[0-9]+/[0-9]+')

    def __str__(self):
        return self.name

    def set_database(self, database):
        self.database = database
        self.database.create(table='docs', cols=[('url', 'text'),
                                                 ('title', 'text'),
                                                 ('content', 'text')])
        self.database.create(table='url_pairs', cols=[('target_url', 'text'),
                                                      ('source_url', 'text')])

    def extract_source_url(self, url, dom):
        source_url = ''
        if self.select_pattern.match(url):
            source_div = dom.find('ul', class_='sa_source')
            source_url = source_div.find_all('li')[1].a['href']
        elif self.article_pattern.match(url):
            source_div = dom.find('div', class_='y_article_copyright')
            source_url = source_div.find_all('li')[0].a['href']
        print 'source_url: {}'.format(source_url)
        # self.database.insert(self.name, 'extracted_urls', values=(source_url,))
        # self.database.insert(self.name, 'url_pairs', values=(url, source_url))
        # self.database.commit(self.name)

    def extract_content(self, url, dom):
        title = ''
        content = ''
        doc_div = dom.find('div', class_='y_l no_border')
        if doc_div:
            h1_divs = doc_div.find_all('h1')
            title = h1_divs[0].string
            content_div = doc_div.find('div', class_='y_article_content clearfix')
        else:
            title_div = dom.find('h1', class_='sa_title')
            title = title_div.string
            content_div = dom.find('div', class_='sa_content')

        para_tags = content_div.find_all('p')
        if para_tags:
            paras = content_div.find_all(True, recursive=False)
            paras = [''.join([s.strip() for s in p.strings]) for p in paras]
            paras = [p for p in paras if p.strip()]
            content = '\n'.join(paras)
        else:
            paras = []
            for c in content_div.children:
                if type(c) == bs4.element.NavigableString:
                    paras.append(c.strip())
                else:
                    paras.append(''.join([s.strip() for s in c.strings]))
            content = ''.join(paras)
        # print url
        # print title
        # print content
        # self.database.insert(self.name, table='docs', values=(url, title, content))
        # self.database.insert(self.name, table='parse_urls', values=(url,))
        # self.database.commit(self.name)

    @get_thread_name
    def parse(self, url, html_page):
        dom = BeautifulSoup(html_page)
        self.extract_content(url, dom)
        self.extract_source_url(url, dom)

def get_parser():
    return YeeyanParser()
