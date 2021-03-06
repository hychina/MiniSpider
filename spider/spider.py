# -*- coding: utf-8 -*-

from logger import log
from Queue import LifoQueue
from downloader import Downloader
import re

class Spider():
    def load_user_agents(self):
        with open('data/user_agents.txt', 'r') as file_:
            user_agents = file_.read().strip().split('\n')
        return user_agents

    def initialize_urls(self):
        start_urls_path = 'data/{}/start_urls'.format(self.spider_name)
        start_urls = []
        try:
            with open(start_urls_path, 'r') as file_:
                start_urls = file_.read().strip().split('\n')
        except IOError:
            print "start_urls doesn't exist at {}".format(start_urls_path)
        else:
            start_urls = [url.decode('utf-8') for url in start_urls]

        parsed_urls = self.database.select('parsed_urls', cols=('url',))
        extracted_urls = self.database.select('extracted_urls', cols=('url',))

        parsed_urls = set([row[0] for row in parsed_urls])
        extracted_urls = [row[0] for row in extracted_urls]

        urls = [url for url in (start_urls + extracted_urls) if url not in parsed_urls]
        if self.url_pattern:
            urls = [url for url in urls if self.url_pattern.match(url)]

        [self.urls.put(url) for url in urls]

    def __init__(self, spider_name, spider_config, parser, database):
        log(spider_name, 'initializing ...')

        self.spider_name = spider_name
        self.database = database
        self.user_agents = self.load_user_agents()
        self.num_threads = int(spider_config.get('num_threads', 5))
        self.urls = LifoQueue()

        # 对 url 进行过滤
        self.url_pattern = None
        url_pattern = spider_config.get('url_pattern', '')
        if url_pattern:
            self.url_pattern = re.compile(url_pattern)

        self.initialize_urls()
        self.downloaders = [Downloader(spider_config=spider_config,
                                       thread_name='{}{}'.format(self.spider_name, n),
                                       urls=self.urls,
                                       user_agents=self.user_agents,
                                       parser=parser,
                                       database=self.database)
                            for n in xrange(self.num_threads)]

    def run(self):
        for d in self.downloaders:
            d.start()
