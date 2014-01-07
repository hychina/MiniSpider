# -*- coding: utf-8 -*-

import threading

from bs4 import BeautifulSoup

from xpider.logger import log


class GuardianParser:
    def __init__(self):
        self.name = 'guardian'

    def __str__(self):
        return self.name

    def set_database(self, database):
        self.database = database

    def extract_content(self, url, dom):
        title_div = dom.find('div', id='main-article-info').h1
        title = title_div.string

        content_div = dom.find('div', id='article-body-blocks')
        paras = content_div.find_all(True, recursive=False)
        paras = [''.join([s.strip() for s in p.strings])
                 for p in paras if p.name != 'div']
        paras = [p for p in paras if p.strip()]
        content = '\n'.join(paras)

        if title and content:
            return (url, title, content)

    def parse(self, url, html_page):
        dom = BeautifulSoup(html_page)
        doc = None
        try:
            doc = self.extract_content(url, dom)
            print doc[1]
            print doc[2]
        except Exception as e:
            log(threading.current_thread().name, 'error:{}:{}'.format(url, e))

        if doc:
            self.database.insert(table='docs', values=doc)
            self.database.insert(table='parsed_urls', values=(url,))

def get_parser():
    return GuardianParser()
