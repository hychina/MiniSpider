import threading
import urllib2

def fetch_page(word):
    global baseurl
    request = urllib2.Request(baseurl + word)
    #request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) \
    #                                  Gecko/20080404 (FoxPlus) \
    #                                  Firefox/2.0.0.14')
    count = 0
    while True:
        resp = urllib2.urlopen(request, timeout=5)
        print count
        count += 1
        with open(word + '.html', 'w') as file_:
            file_.write(resp.read())

baseurl = 'http://www.iciba.com/'
threads = [threading.Thread(target=fetch_page, args=('hello',)) for n in xrange(10)]
for t in threads:
    t.start()
