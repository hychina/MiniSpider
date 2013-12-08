from logger import log
from bs4 import BeautifulSoup
import re

class IcibaParser():
    def __init__(self):
        self.url_pattern = re.compile(r'(http://dj.iciba.com/.*?-[0-9]+-)([0-9]+)(\.html)')
        self.name = 'iciba'

    def __str__(self):
        return self.name

    def extract_urls(self, dom_tree):
        div_page_numbers = dom_tree.find('div', class_='jkPage')

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

    def extract_sentences(self, dom_tree):
        sentence_list_div = dom_tree.find('div', class_='jkList')
        sentence_divs = sentence_list_div.find_all('dl', class_='dj_dl')
        for sentence_div in sentence_divs:
            en_div = sentence_div.find('dt')
            cn_div = sentence_div.find('dd')
            en = ''.join([s for s in en_div.strings]).strip()
            cn = ''.join([s for s in cn_div.strings]).strip()
            print en, cn

    def parse(self, url, html_page):
        dom_tree = BeautifulSoup(html_page)
        try:
            self.extract_sentences(dom_tree)
        except AttributeError:
            log(self.name, 'no sentences found in {} ...'.format(url))

        if self.url_pattern.match(url) is None:
            new_urls = self.extract_urls(dom_tree)
            if new_urls is not None:
                log(self.name, '{} new urls extracted in {} ...'.format(len(new_urls), url))
            return new_urls

def get_parser():
    return IcibaParser()