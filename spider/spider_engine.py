import ConfigParser
import parsers
from spider import Spider
from database import Database

class SpiderEngine:

    @classmethod
    def run(cls, spider_cfg):
        cfg = ConfigParser.ConfigParser()

        cfg.read(spider_cfg)
        sections_names = cfg.get('spiders', 'names').split(' ')
        spider_configs = dict()

        # initialize parsers
        parser_pkg = __import__('parsers', fromlist=parsers.__all__)
        parsers_ = dict()
        for parser_mod_name in parsers.__all__:
            parser_obj = getattr(parser_pkg, parser_mod_name).get_parser()
            parsers_[str(parser_obj)] = parser_obj

        spiders = []
        # read spider configs
        for spider_name in sections_names:
            spider_config = dict()
            for option in cfg.options(spider_name):
                spider_config[option] = cfg.get(spider_name, option)
            spider_configs[spider_name] = spider_config

            database = Database(database_path=spider_config['database_path'])
            # create database tables
            # needs orm to be configurable
            database.create(table='pages', cols=[('url', 'text'), ('html', 'text')])
            database.create(table='sentences', cols=[('en', 'text'), ('cn', 'text')])
            database.create(table='parsed_urls', cols=[('url', 'text')])
            database.create(table='extracted_urls', cols=[('url', 'text')])

            parser = parsers_[spider_name]
            parser.set_database(database)
            spiders.append(Spider(spider_name, spider_config, parser, database))
        [spider.run() for spider in spiders]
