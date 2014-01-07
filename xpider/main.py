# -*- coding: utf-8 -*-

import logging
import sys
import getopt
from spider.spider_engine import SpiderEngine

def main(argv):
    log_path = './data/xpider.log'
    spider_cfg = './data/spiders.cfg'
    try:
        opts, args = getopt.getopt(argv, 'l:c:', ['log=', 'config='])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-l', '--log'):
            log_path = arg
        elif opt in ('-c', '--config'):
            spider_cfg = arg
    logging.basicConfig(filename=log_path, level=logging.DEBUG)
    SpiderEngine.run(spider_cfg=spider_cfg)

if __name__ == '__main__':
    main(sys.argv[1:])