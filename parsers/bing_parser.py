from logger import log
from bs4 import BeautifulSoup
import re

class BingParser():
    def __init__(self):
        self.url_pattern = \
            re.compile(r"(http://cn.bing.com/dict/service\?q=.*?&offset=)([0-9]+)(&dtype=sen&mkt=zh-CN&setlang=ZH)")
        self.next_page_offset_pattern = \
            re.compile(r"BilingualAjax\.pageSen\('.*?','([0-9]+)'\)")
        self.name = 'bing'

    def __str__(self):
        return self.name

    def set_database(self, database):
        self.database = database
        self.database.create(table='source_urls', cols=[('url', 'text')])

    def extract_urls(self, url, dom_tree):
        page_number_div = dom_tree.find_all('div', class_='bi_pag')
        if len(page_number_div) == 0:
            return None
        next_page_div = page_number_div[0].ul.contents[-1]
        next_page_offset = self.next_page_offset_pattern.match(next_page_div.a['onclick']).group(1)
        next_page_url = self.url_pattern.sub('\g<1>{}\g<3>'.format(next_page_offset), url)

        new_urls = [next_page_url]
        return new_urls

    # return number of sentences extracted if success
    def extract_sentences(self, dom_tree):
        sentence_divs = dom_tree.find_all('div', class_='se_li')
        for sentence_div in sentence_divs:
            sentence_div = sentence_div.find('div', class_='se_li1')
            en_div = sentence_div.find('div', class_='sen_en')
            cn_div = sentence_div.find('div', class_='sen_cn')
            url_div = sentence_div.find('div', class_='sen_li')

            en = ''.join([s for s in en_div.strings]).strip()
            cn = ''.join([s for s in cn_div.strings]).strip()
            self.database.insert(table='sentences', values=(en, cn))

            try:
                url = url_div.a['href']
            except Exception:
                pass
            else:
                self.database.insert(table='source_urls', values=(url,))
        return len(sentence_divs)

    def parse(self, url, html_page):
        dom_tree = BeautifulSoup(html_page)
        try:
            num_sentences = self.extract_sentences(dom_tree)
        except AttributeError as e:
            log(self.name, u'no sentences found in {} ...'.format(url))
        else:
            log(self.name, u'{} sentence(s) found in {} ...'.format(num_sentences, url))
        new_urls = None
        try:
            new_urls = self.extract_urls(url, dom_tree)
        except Exception as e:
            pass

        if new_urls is not None:
            log(self.name, u'{} new url(s) extracted in {} ...'.format(len(new_urls), url))
            for new_url in new_urls:
                self.database.insert(table='extracted_urls', values=(new_url,))
        else:
            log(self.name, u'no url(s) extracted in {} ...'.format(url))

        # data integrity: no commit before url is recorded
        self.database.insert(table='parsed_urls', values=(url,))
        self.database.commit()
        return new_urls

def get_parser():
    return BingParser()
