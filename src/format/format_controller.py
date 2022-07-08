from black import out
import helpers
from scrapy import signals
from data_sources import spiders
from observability.execution_time import check_execution_time
from scrapy.crawler import CrawlerProcess, Crawler
from src.deck.deck_controller import Deck
import json
import os
import uuid


class Format(object):
    """
    This class is used as abstraction to format object
    """

    def __init__(self, name: str):
        self.domain_helper: helpers.Domain = helpers.Domain()
        if name not in self.domain_helper.allowed_formats:
            raise Exception("Not allowed format")
        self.name: str = name
        self.spiders: list = [spiders.GoldFishDecks, spiders.MtgTop8DecksEvents]
        self.decks: list = []

    def handle_scrapped_item(self, item: dict):
        """
        Method used as a trigger when a spiders gets an item
        :param item: A dict with the scrapped raw data information
        """
        # self.decks.append(Deck(item)
        output = f"{item.get('source')}_{item.get('name')}.json"
        if os.path.exists(output):
            output = f"{item.get('source')}_{item.get('name','').strip()}_{uuid.uuid4()}.json"
        file = open(output, "w+")
        json.dump(item, file)
        file.close()

    @check_execution_time
    def get_spiders_data(self) -> None:
        """
        Method used to get the data from the spiders allowed
        """
        process = CrawlerProcess()
        for spider in self.spiders:
            crawler = Crawler(spider)
            crawler.signals.connect(
                self.handle_scrapped_item, signal=signals.item_scraped
            )
            process.crawl(crawler, format=self.name)
        process.start()

    def build_report(self):
        data: list = []
        for deck in self.decks:
            data.append(deck.get_info())
