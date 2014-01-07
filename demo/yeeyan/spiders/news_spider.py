# coding: utf-8

from xpider.db import models
from xpider.spider import BaseSpider
from xpider.selector import Selector

# xpaths = {
#     'www.economist.com': (
#         '(//h1//h3)[@class="headline"]',
#         '//div[@class="main-content"]/p'
#     ),
#     'www.nytimes.com': (
#         '//*[@id="article"]/div[1]/h1/nyt_headline',
#         '//*[@id="article"]/div[1]/div[3]/nyt_text/p'
#     ),
#     'www.dailymail.co.uk': (
#         '//*[@id="js-article-text"]/h1',
#         '//*[@id="js-article-text"]/p'
#     ),
#     'www.time.com': (
#         '//h2[@class="item-title"]',
#         '//div[@class="entry-content group"]/p'
#     ),
#     'www.readwriteweb.com': (
#         '//h1[@class="instapaper_title" and @itemprop="headline"',
#         '//*[@id="article-content"]/section/p'
#     ),
#     'www.telegraph.co.uk': (
#         '//h1[@itemprop="headline name"]',
#         '//*[@id="mainBodyArea"]/div/p'
#     ),
# }

class NewsArticle(models.Model):
    url = models.CharField()
    title = models.CharField()
    content = models.CharField()

class NewsSpider(BaseSpider):
    allowed_domains = []
    start_urls = []

    def parse(self, response):
        s = Selector(response)
        article = NewsArticle()
        article.save()

def main():
    spider = NewsSpider()
    spider.start()

main()
