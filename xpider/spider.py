class BaseSpider(object):
    name = None

    def __init__(self):
        if not getattr(self, 'name') or self.name is None:
            raise ValueError("%s must have a name" % type(self).__name__)

        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    def set_crawler(self, crawler):
        assert not hasattr(self, '_crawler'), "Spider already bounded to %s" % crawler
        self._crawler = crawler

    def parse(self, response):
        raise NotImplementedError

    def start(self):
        pass

    def __str__(self):
        return "<%s %r at 0x%0x>" % (type(self).__name__, self.name, id(self))

    __repr__ = __str__
