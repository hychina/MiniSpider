import os
import ConfigParser
from spider import Spider
import parsers

class SpiderEngine:
    cfg = ConfigParser.ConfigParser()

    @classmethod
    def load_parsers(cls):
        parser_mod = __import__('parsers', fromlist=parsers.__all__)
        parsers_ = {}
        for parser_ in parsers.__all__:
            parser_obj = getattr(parser_mod, parser_).get_parser()
            parsers_[str(parser_obj)] = parser_obj
        return parsers_

    @classmethod
    def init_spiders(cls, parsers_):
        cls.cfg.read('./data/spiders.cfg')
        sections_names = cls.cfg.get('spiders', 'names').split(' ')
        spider_configs = []

        for section_name in sections_names:
            spider_config = {}
            spider_config['spider_name'] = section_name
            spider_config['data_path'] = os.path.join('./../data', section_name)
            for option in cls.cfg.options(section_name):
                spider_config[option] = cls.cfg.get(section_name, option)
            spider_configs.append(spider_config)

        return [Spider(spider_config=cfg, parser=parsers_[cfg['spider_name']])
                for cfg in spider_configs]

    @classmethod
    def run(cls):
        parsers_ = cls.load_parsers()
        spiders_ = cls.init_spiders(parsers_)
        [spider.run() for spider in spiders_]
