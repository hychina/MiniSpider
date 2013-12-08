# -*- coding: utf-8 -*-

import logging
from spider.spider_engine import SpiderEngine

def main():
    logging.basicConfig(filename='./data/spider.log', level=logging.DEBUG)
    SpiderEngine.run()

if __name__ == '__main__':
    main()