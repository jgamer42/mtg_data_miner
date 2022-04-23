import scrapy
import sys

sys.path.append("../")
from utils.context_helper import contextHelper
from extract.API import mtg_api


class MtgWtf(scrapy.Spider):
    name: str = "mtg_wtf_formats"
    custom_settings: dict = {"ROBOTSTXT_OBEY": True, "CONCURRENT_REQUESTS": 100}

    def __init__(self, format: str, *args, **kwargs):
        self.context_helper: contextHelper = contextHelper()
        xpath_expresions = {
            "standard": "//*[contains(text(),'Included sets')]/following-sibling::ul[1]/li/a/text()",
            "modern": "//h3/following-sibling::ul[1]/li/a/text()",
            "pioneer": "//*[contains(text(),'Included sets')]/following-sibling::ul[1]/li/a/text()",
        }
        if format in self.context_helper.get_allowed_formats():
            self.xpath = xpath_expresions.get(format)
            super(MtgWtf, self).__init__(*args, **kwargs)
            self.start_urls: list = [f"https://mtg.wtf/format/{format}"]
            self.format: str = format
        else:
            return None

    def parse(self, response):
        if self.format == "pauper":
            yield self.context_helper.get_legal_sets()
        else:
            output: dict = {}
            legal_sets: list = self.context_helper.get_legal_sets()
            scraped_sets: list = response.xpath(self.xpath).getall()
            for scraped_set in scraped_sets:
                if scraped_set.strip() not in [
                    legal_sets[legal_set] for legal_set in legal_sets.keys()
                ]:
                    pending_set: dict = mtg_api.get_pending_set(scraped_set)
                    if pending_set:
                        self.context_helper.add_new_legal_set(pending_set)
                        output[pending_set[0]] = pending_set[1]
                else:
                    for legal_set in legal_sets.keys():
                        if legal_sets[legal_set].strip() == scraped_set:
                            output[legal_set] = scraped_set
            yield output
