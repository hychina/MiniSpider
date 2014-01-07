url_patt = 'http://article.yeeyan.org/lists/new/{}'
with open('../data/yeeyan/start_urls', 'w') as file_:
    for n in xrange(1, 19309):
        url = url_patt.format(n)
        file_.write(url + '\n')
