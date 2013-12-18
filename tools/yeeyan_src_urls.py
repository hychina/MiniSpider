import sqlite3
import urlparse
from operator import itemgetter

def url_stats():
    con = sqlite3.connect('../data/yeeyan/yeeyan.db')
    cur = con.cursor()
    cur.execute(sql_select)

    domains = dict()
    for url in cur:
        src = url[1].strip()
        parts = urlparse.urlparse(src)
        domain = parts.netloc
        if domain:
            if domain in domains:
                url_list = domains[domain]
            else:
                url_list = []
                domains[domain] = url_list
            url_list.append(src)

    domain_list = [(domain, len(domains[domain])) for domain in domains]
    domain_list = sorted(domain_list, key=itemgetter(1), reverse=True)

    with open('../data/yeeyan/domain_freq.txt', 'w') as count_file, \
         open('../data/yeeyan/source_urls.txt', 'w') as url_file:
        for domain, count in domain_list:
            count_file.write(u'{}\t{}\n'.format(domain, count).encode('utf-8'))
            url_list = domains[domain]
            for url in url_list:
                url_file.write(url.encode('utf-8') + '\n')

def get_target_url(src_url):
    con = sqlite3.connect('../data/yeeyan/yeeyan.db')
    cur = con.cursor()
    cur.execute(sql_select)
    for url_pair in cur:
        if src_url == url_pair[1].strip():
            print url_pair

sql_select = 'select target_url, source_url from url_pairs'
get_target_url('http://www.guardian.co.uk/travel/2013/jun/07/80-year-old-motorbike-india-delhi')
# url_stats()