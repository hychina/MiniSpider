from goose import Goose
import urllib2

url = 'http://www.dailymail.co.uk/health/article-2476507/How-washing-hands-makes-HAPPIER-Cleaning-boosts-confidence-washes-away-feelings-failure.html'
agent = 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
req = urllib2.Request(url)
req.add_header('User-Agent', agent)
# proxy = urllib2.ProxyHandler({'http': 'adslspider01.web.zw.vm.sogou-op.org:8080'})
# proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8087'})

opener = urllib2.build_opener()
html = opener.open(req).read()
print '.........'

g = Goose()
article = g.extract(url=url, raw_html=html)
print article.title
print '....................................'
print article.cleaned_text
