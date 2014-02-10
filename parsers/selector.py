class Selector(object):
    parser = etree.HTMLParser()
    get_string = etree.XPath('string()')

    def __init__(self, xpath):
        self.xpath = etree.XPath(xpath)

    def select(self, html):
        tree = etree.parse(source=StringIO(html), parser=self.parser)
        elems = []
        for elem in self.xpath(tree):
            text = self.get_string(elem).strip() 
            if text: elems.append(text) 
        return elems
