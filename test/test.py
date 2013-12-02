# -*- coding: utf-8 -*-

import os
import parser
import base64
from spider import Spider

def main():
    #with open('../data/corpus.result', 'r') as file_:
    #    lines = file_.read().strip().split('\n')
    #    all_words = [line.split('\t')[0] for line in lines]
    #print 'all words loaded ...'
    #
    #iciba_url_pattern = 'http://dj.iciba.com/{0}'
    #iciba_urls = [iciba_url_pattern.format(word) for word in all_words]
    #with open('../data/iciba/allurls', 'w') as file_:
    #    file_.write('\n'.join(iciba_urls))

    with open('../data/iciba/allurls', 'r') as file_:
        iciba_all_urls = file_.read().strip().split('\n')
    with open('../data/iciba/fetchedurls', 'r') as file_:
        iciba_fetched_urls = set(file_.read().strip().split('\n'))

    iciba_dest = '../data/iciba/'
    iciba_urls = [url for url in iciba_all_urls if url not in iciba_fetched_urls]
    iciba_rejection_msg = '非常抱歉，来自您ip的请求异常频繁，为了保护其他用户的正常访问，只能暂时禁止您目前的访问。'

    iciba_spider = Spider(urls=iciba_urls,
                          thread_name='iciba',
                          rejection_msg=iciba_rejection_msg,
                          batch_size=10,
                          batch_interval=10)
    iciba_parser = parser.IcibaParser(iciba_spider, iciba_dest)
    parser_manager = parser.ParserManager(iciba_parser)

    iciba_spider.start()
    parser_manager.run()

if __name__ == '__main__':
    main()