import os
import re
import base64
from bs4 import BeautifulSoup

class ParserManager:
    def __init__(self, *parsers):
        self.parsers = parsers

    def run(self):
        while True:
            for parser in self.parsers:
                parser.parse()

class Parser:
    def __init__(self, spider, dest):
        self.spider = spider
        self.dest = dest

    def add_url(self, url):
        return self.spider.add_url(url)

    def get_html_page(self):
        return self.spider.get_html_page()

    def save_html_page(self, url, html_page):
        filename = base64.urlsafe_b64encode(url)
        with open(os.path.join(self.dest, 'pages', filename), 'w') as file_:
            file_.write(html_page)
        with open(os.path.join(self.dest, 'fetchedurls'), 'a') as file_:
            file_.write(url + '\n')

class IcibaParser(Parser):
    def __init__(self, spider, dest):
        Parser.__init__(self, spider, dest)
        self.url_pattern = re.compile(r'(http://dj.iciba.com/.*?-[0-9]+-)([0-9]+)(\.html)')

    def parse_urls(self, html):
        soup = BeautifulSoup(html)
        div_page_numbers = soup.find('div', class_='jkPage')

        if div_page_numbers is None:
            return None

        anchors = [a for a in div_page_numbers.find_all('a')]
        if len(anchors) == 0:
            return None
        last_page_anchor = anchors[-2]
        last_page_number = int(last_page_anchor.string)
        last_page_href = last_page_anchor['href']

        if self.url_pattern.match(last_page_href) is not None:
            return [self.url_pattern.sub(r'\g<1>{0}\g<3>'.format(n), last_page_href)
                    for n in xrange(2, last_page_number + 1)]
        else:
            return None

    def parse(self):
        url, html = self.get_html_page()
        self.save_html_page(url=url, html_page=html)

        if self.url_pattern.match(url) is None:
            new_urls = self.parse_urls(html)
            if new_urls is not None:
                print '{0} new pages found in {0} ...'.format(len(new_urls), url)
                all_urls_file = open(os.path.join(self.dest, 'allurls'), 'a')
                for url in new_urls:
                    self.add_url(url)
                    all_urls_file.write(url + '\n')
                all_urls_file.close()
