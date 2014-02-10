# -*- coding: utf-8 -*-

from goose import Goose
from logger import log
import threading

def get_parser():
    return NewsParser()

class NewsParser(Parser):
    name = 'news'
    extractor = Goose()

    def extract_content(self, url, html):
        article = self.extractor.extract(raw_html=html)
        title = article.title
        content = article.cleaned_text

        if title and content:
            return (url, title, content)
        else:
            raise Exception('Goose parse error.')

    def parse(self, url, html):
        doc = None
        try:
            doc = self.extract_content(url, html)
        except Exception as e:
            log(threading.current_thread().name, u'error:{}:{}'.format(url, e))

        if doc:
            self.database.insert(table='docs', values=doc)
            self.database.insert(table='parsed_urls', values=(url,))
