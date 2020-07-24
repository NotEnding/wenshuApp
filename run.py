import scrapy
from scrapy.crawler import CrawlerProcess
from wenshu.spiders.wenshu_spider import WenshuSpider

# 创建一个CrawlerProcess对象
process = CrawlerProcess() # 括号中可以添加参数

process.crawl(WenshuSpider)
process.start()