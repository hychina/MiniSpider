import os
import ConfigParser
from spider import Spider
import parsers

class SpiderEngine:

    @classmethod
    def run(cls):
        cfg = ConfigParser.ConfigParser()

        cfg.read('./data/spiders.cfg')
        sections_names = cfg.get('spiders', 'names').split(' ')
        spider_configs = dict()

        # read spider configs
        for section_name in sections_names:
            spider_config = dict()
            spider_config['spider_name'] = section_name
            spider_config['data_path'] = os.path.join('./../data', section_name)
            for option in cfg.options(section_name):
                spider_config[option] = cfg.get(section_name, option)
            spider_configs[section_name] = spider_config

        # initialize parsers
        parser_pkg = __import__('parsers', fromlist=parsers.__all__)
        parsers_ = {}
        for parser_mod_name in parsers.__all__:
            parser_obj = getattr(parser_pkg, parser_mod_name).get_parser()
            parsers_[str(parser_obj)] = parser_obj

        for parser_name in parsers_:
            parsers_[parser_name].set_database(spider_configs[parser_name]['database'])

        spiders = [Spider(spider_config=spider_configs[spider_name],
                          parser=parsers_[spider_name])
                   for spider_name in spider_configs]

        [spider.run() for spider in spiders]


