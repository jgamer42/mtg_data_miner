import scrapy


class MtgWtf(scrapy.Spider):
    name: str = "mtg_wtf_formats"
    custom_settings: dict = {"ROBOTSTXT_OBEY": True, "CONCURRENT_REQUESTS": 100}

    def __init__(self, format: str, *args, **kwargs):
        xpath_expresions = {
            "standard": "//*[contains(text(),'Included sets')]/following-sibling::ul[1]/li/a/text()",
            "modern": "//h3/following-sibling::ul[1]/li/a/text()",
            "pioneer": "//*[contains(text(),'Included sets')]/following-sibling::ul[1]/li/a/text()",
        }
        self.xpath = xpath_expresions.get(format)
        super(MtgWtf, self).__init__(*args, **kwargs)
        self.start_urls: list = [f"https://mtg.wtf/format/{format}"]
        self.format: str = format

    def parse(self, response):
        if self.format == "pauper":
            yield {}
        else:
            output:list = []
            scraped_sets: list = response.xpath(self.xpath).getall()
            for scraped_set in scraped_sets:
                output.append(scraped_set)
            yield {"data":output,"format":self.format}
