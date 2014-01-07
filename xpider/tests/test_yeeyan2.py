from demo.spiders.yeeyan2 import YeeyanParser

def test():
    url = 'http://article.yeeyan.org/view/111988/390917'
    with open('data/390917', 'r') as file_:
        html = file_.read()
    parser = YeeyanParser()
    parser.parse(url, html)

test()