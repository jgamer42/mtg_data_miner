import helpers 
import logging
from data_sources.spiders import MtgWtf
from scrapy.crawler import CrawlerProcess, Crawler
logging.getLogger("scrapy").propagate=False
logging.getLogger("filelock").propagate=False
process = CrawlerProcess()
crawler = Crawler(MtgWtf)
process.crawl(crawler, format="standard")
process.start()