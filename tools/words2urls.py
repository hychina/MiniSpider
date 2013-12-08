def main():
    corpus = 'data/corpus.result'
    with open(corpus, 'r') as file_:
        lines = file_.read().strip().split('\n')
        all_words = [line.split('\t')[0] for line in lines]
    print 'all words loaded ...'

    iciba_url_pattern = 'http://dj.iciba.com/{0}\n'
    iciba_urls = [iciba_url_pattern.format(word) for word in all_words]
    with open('data/iciba/start_urls', 'w') as file_:
        file_.write(''.join(iciba_urls))

if __name__ == '__main__':
    main()
