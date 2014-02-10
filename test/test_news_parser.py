from parsers.news_parser import NewsParser
import urllib2

url = 'http://www.economist.com/node/21558263'
agent = 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
req = urllib2.Request(url)
req.add_header('User-Agent', agent)

html = urllib2.urlopen(req).read()
print 'download success...'

news_parser = NewsParser()
news_parser.parse(url, html)
