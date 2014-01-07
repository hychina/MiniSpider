from lxml import etree

parser = etree.HTMLParser()
tree = etree.parse('data/russias-election', parser)
title_path = etree.XPath('(//h1|//h2|//h3|//h4)[@class="headline"]')
paras_path = etree.XPath('//div[@class="main-content"]/p')
stringify = etree.XPath('string()')
print stringify(title_path(tree)[0]).strip()
for p in paras_path(tree):
    # print etree.tostring(p, method='text', encoding='utf-8')
    content = stringify(p)
    if content.strip():
        print content