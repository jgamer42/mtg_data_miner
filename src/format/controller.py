import helpers
from scrapy import signals
from data_sources import spiders
from scrapy.crawler import CrawlerProcess, Crawler


class Format(object):
    """
    This class is used as abstraction to format object
    """

    def __init__(self, name: str):
        self.domain_helper: helpers.Domain = helpers.Domain()
        if name not in self.domain_helper.allowed_formats:
            raise Exception("Not allowed format")
        self.name = name
        self.spiders = [spiders.GoldFishDecks, spiders.MtgTop8DecksEvents]

    def handle_scrapped_item(self, item):
        print(item, "AQUIIII")

    def get_spiders_data(self):
        process = CrawlerProcess(settings={"LOG_LEVEL": "INFO"})
        for spider in self.spiders:
            crawler = Crawler(spider)
            crawler.signals.connect(
                self.handle_scrapped_item, signal=signals.item_scraped
            )
            process.crawl(crawler, format=self.name)
        process.start()
