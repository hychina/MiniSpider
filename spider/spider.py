# -*- coding: utf-8 -*-

from logger import log
from Queue import LifoQueue
from downloader import Downloader
from database import Database

class Spider():
    def __init__(self, spider_name, spider_config, parser, database):
        log(spider_name, 'initializing ...')

        self.spider_name = spider_name
        self.database = database
        self.urls = LifoQueue()
        self.initialize_urls()
        self.num_threads = spider_config.get('num_threads', 1)

        self.downloaders = [Downloader(spider_config=spider_config,
                                       thread_name='{}{}'.format(self.spider_name, n),
                                       urls=self.urls,
                                       parser=parser,
                                       database=self.database)
                            for n in self.num_threads]

    def initialize_urls(self):
        with open('data/iciba/start_urls', 'r') as file_:
            start_urls = file_.read().strip().split('\n')

        parsed_urls = self.database.select('parsed_urls', cols=('url',))
        extracted_urls = self.database.select('extracted_urls', cols=('url',))
        parsed_urls = [row[0] for row in parsed_urls]
        extracted_urls = [row[0] for row in extracted_urls]

        urls = [url for url in (start_urls + extracted_urls) if url not in set(parsed_urls)]

        [self.urls.put(url) for url in urls]

    def run(self):
        for d in self.downloaders:
            d.start()
