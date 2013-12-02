# -*- coding: utf-8 -*- 

import threading
import urllib2
import logging
import time
import sys
import Queue

class Spider(threading.Thread):
    def __init__(self, thread_name, urls=[], rejection_msg=None,
                 max_retry_count=5, timeout=5, fetch_interval=1,
                 batch_size=0, batch_interval=0):
        threading.Thread.__init__(self, name=thread_name)
        logging.basicConfig(filename='spider.log', level=logging.DEBUG)
        self.log('initializing ...')
        self.urls = Queue.LifoQueue()
        [self.urls.put(url) for url in urls]
        self.html_pages = Queue.LifoQueue()
        self.rejection_msg = rejection_msg
        self.max_retry_count = max_retry_count
        self.timeout = timeout
        self.fetch_interval = fetch_interval
        self.batch_size = batch_size
        self.batch_interval = batch_interval
        self.user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) \
Gecko/20080404 (FoxPlus) Firefox/2.0.0.14'

    def fetch(self, url):
        request = urllib2.Request(url)
        request.add_header('User-Agent', self.user_agent)
        fail_count = 0
        while True:
            try:
                time.sleep(self.fetch_interval)
                resp = urllib2.urlopen(request, timeout=self.timeout)
                break
            except Exception as e:
                fail_count += 1
                if fail_count <= self.max_retry_count:
                    self.log('error:{0}:{1}, retry {2} ...'.format(url, str(e), fail_count))
                else:
                    raise e
        return resp.read()

    def log(self, msg):
        msg = '{0}:{1}\n'.format(self.name, msg)
        sys.stdout.write(msg)
        logging.debug(msg)

    def get_html_page(self):
        return self.html_pages.get()

    def add_url(self, url):
        self.urls.put(url)

    def run(self):
        self.log('started ...')
        num_fetches = 0
        while True:
            url = self.urls.get()
            try:
                html = self.fetch(url)
            except Exception as e:
                self.log('fail:{0}:{1}'.format(url, e))
            else:
                if self.rejection_msg is not None and self.rejection_msg not in html:
                    self.log('success:{0}'.format(url))
                    self.html_pages.put((url, html))
                else:
                    self.log('rejected:{0}'.format(url))
            finally:
                num_fetches += 1
                if num_fetches == self.batch_size:
                    self.log('start waiting ...')
                    start_time = time.time()
                    time.sleep(self.batch_interval)
                    end_time = time.time()
                    self.log('stop waiting ...')
                    self.log('waited {0} seconds ...'.format(end_time - start_time))
                    num_fetches = 0
