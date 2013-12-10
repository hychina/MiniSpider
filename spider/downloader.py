from logger import log
from bs4 import UnicodeDammit
import threading
import urllib2
import time
import random

class Downloader(threading.Thread):
    def __init__(self, spider_config, thread_name, urls, user_agents, parser, database):
        threading.Thread.__init__(self, name=thread_name)

        self.rejection_msg = spider_config.get('rejection_msg', None)
        self.max_retry = int(spider_config.get('max_retry', 5))
        self.timeout = int(spider_config.get('timeout', 5))
        self.fetch_interval = int(spider_config.get('fetch_interval', 1))
        self.batch_size = int(spider_config.get('batch_size', 100))
        self.batch_interval = int(spider_config.get('batch_interval', 100))

        self.parser = parser
        self.urls = urls
        self.user_agents = user_agents
        self.database = database

    def fetch(self, url):
        request = urllib2.Request(url.encode('utf-8'))
        user_agent = random.choice(self.user_agents)
        request.add_header('User-Agent', user_agent)
        fail_count = 0
        while True:
            try:
                time.sleep(self.fetch_interval)
                resp = urllib2.urlopen(request, timeout=self.timeout)
                return resp.read()
            except Exception as e:
                fail_count += 1
                if fail_count <= self.max_retry:
                    log(self.name, u'error:{0} {1}, retry {2} ...'.format(url, str(e), fail_count))
                else:
                    raise e

    def save_page(self, url, html_page):
        dammit = UnicodeDammit(html_page)
        enc = dammit.original_encoding
        html_page = html_page.decode(enc)
        self.database.insert(thread_name=self.name, table='pages', values=(url, html_page))

    def wait(self, interval):
        log(self.name, 'start waiting ...')
        start_time = time.time()
        time.sleep(interval)
        end_time = time.time()
        log(self.name, 'stop waiting ...')
        log(self.name, 'waited {0} seconds ...'.format(end_time - start_time))

    def run(self):
        log(self.name, 'started ...')
        num_fetches = 0
        while True:
            url = self.urls.get()
            try:
                html = self.fetch(url)
            except Exception as e:
                log(self.name, u'fail:{0} {1}'.format(url, e))
            else:
                if self.rejection_msg is not None and self.rejection_msg not in html:
                    log(self.name, u'success:{0}'.format(url))

                    # save html page to dest
                    self.save_page(url=url, html_page=html)

                    # feed to parser
                    new_urls = self.parser.parse(url=url, html_page=html)
                    if new_urls:
                        [self.urls.put(url) for url in new_urls]

                else:
                    log(self.name, u'rejected:{0}'.format(url))
                    self.urls.put(url)
                    self.wait(interval=200*60)
            finally:
                num_fetches += 1
                if num_fetches == self.batch_size:
                    self.wait(self.batch_interval)
                    num_fetches = 0
