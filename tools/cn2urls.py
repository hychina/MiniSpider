import os

def main():
    corpus = '../data/corpus.cn'
    with open(corpus, 'r') as file_:
        lines = file_.read().strip().split('\n')
        all_words = [line.split('\t')[0] for line in lines]
    print 'all words loaded ...'

    url_pattern = 'http://cn.bing.com/dict/service?q={}&offset=0&dtype=sen&mkt=zh-CN&setlang=ZH'
    urls = [url_pattern.format(word) for word in all_words]
    with open('../data/bing/start_urls', 'w') as file_:
        file_.write('\n'.join(urls))

if __name__ == '__main__':
    main()
