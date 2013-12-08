# -*- coding: utf-8 -*-

from logger import log
from Queue import LifoQueue
from downloader import Downloader
from datastore import DataStore

class Spider():
    def __init__(self, spider_config, parser):
        self.urls = LifoQueue()
        self.load_start_urls()

        self.spider_name = spider_config.get('spider_name')
        log(self.spider_name, 'initializing ...')
        self.num_threads = spider_config.get('num_threads', 1)
        self.database = spider_config.get('database')

        DataStore.create(database=self.database,
                         table='pages',
                         cols='')

        self.downloaders = [Downloader(spider_config=spider_config,
                                       thread_name='{}{}'.format(self.spider_name, n),
                                       urls=self.urls,
                                       parser=parser,
                                       database=self.database)
                            for n in self.num_threads]

    def load_start_urls(self):
        with open('data/iciba/start_urls', 'r') as file_:
            urls = file_.read().strip().split('\n')
        [self.urls.put(url) for url in urls]

    def run(self):
        for d in self.downloaders:
            d.start()
