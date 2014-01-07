import os
import re

num_sentences = 0
dir = '../data/data/sentences'
sen_pattern = re.compile('<sentence>.*?</sentence>')

for filename in os.listdir(dir):
    with open(os.path.join(dir, filename), 'r') as file_:
        count = len(sen_pattern.findall(file_.read()))
        print '{0} {1}'.format(filename, count)
        num_sentences += count
print num_sentences
