# -*- coding: utf-8 -*-

import threading

from bs4 import BeautifulSoup, UnicodeDammit

from xpider.logger import log


class YeeyanParser:
    def __init__(self):
        self.name = 'yeeyan'

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
        source_div = dom.find('ul', class_='sa_source')
        if not source_div:
            source_div = dom.find('div', class_='y_article_copyright')

        source_url = source_div.find_all('li')[2].a['href']
        return source_url

    def extract_content(self, url, dom):
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
            content = [s.strip() for s in content_div.strings]
            content = ''.join([s for s in content if s != ''])

        if title and content:
            return (url, title, content)

    def save_page(self, url, html_page):
        dammit = UnicodeDammit(html_page)
        enc = dammit.original_encoding
        html_page = html_page.decode(enc)
        self.database.insert(table='pages', values=(url, html_page))

    def parse(self, url, html_page):
        # self.save_page(url, html_page)

        dom = BeautifulSoup(html_page)
        source_url = None
        doc = None
        try:
            doc = self.extract_content(url, dom)
            source_url = self.extract_source_url(url, dom)
        except:
            log(threading.current_thread().name, 'error: {}'.format(url))

        if source_url and doc:
            log(threading.current_thread().name, source_url)
            self.database.insert('extracted_urls', values=(source_url,))
            self.database.insert('url_pairs', values=(url, source_url))
            self.database.insert(table='docs', values=doc)
            self.database.insert(table='parsed_urls', values=(url,))

def get_parser():
    return YeeyanParser()
