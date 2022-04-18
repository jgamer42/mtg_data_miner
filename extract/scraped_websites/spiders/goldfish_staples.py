import scrapy
from lxml import html
from scraped_websites.items import Staple


class GoldFishSpider(scrapy.Spider):
    name = "goldfish_staples"
    formats = ["standard", "modern", "pioneer", "pauper"]
    staples_urls = [
        f"https://www.mtggoldfish.com/format-staples/{game_format}"
        for game_format in formats
    ]
    start_urls = staples_urls
    custom_settings = {"ROBOTSTXT_OBEY": True, "CONCURRENT_REQUESTS": 30}

    def parse(self, response):
        format = response._get_url().split("/")[-1]
        view_more_links = response.xpath(
            "//a[@class='staples-view-more']/@href"
        ).getall()
        for link in view_more_links:
            yield response.follow(
                url=link, callback=self.view_more_section, cb_kwargs={"format": format}
            )

    def view_more_section(self, response, **kwargs):
        source = response._get_url().split("/")[-1]
        cards = response.xpath("//tr").getall()
        cards = cards[1:]
        if source != "all":
            for card in cards:
                yield self.get_card_info(kwargs["format"], source, card)

    def get_card_info(self, format, source, card):
        item = Staple()
        row_loaded = html.fromstring(card)
        item["format"] = format
        item["type"] = source
        item["name"] = row_loaded.xpath("//td[@class='col-card']/span/a/text()")
        item["percentage_deck"] = row_loaded.xpath("//td[contains(text(),'%')]/text()")
        item["image"] = row_loaded.xpath(
            "//td[@class='col-card']/span/a/@data-full-image"
        )
        item["played_number"] = row_loaded.xpath(
            "//td[not(contains(text(),'%')) and @class='text-right' and not(following-sibling::td)]/text()"
        )
        try:
            mana_cost = row_loaded.xpath(
                "//td[@class='responsive-column']/span/@aria-label"
            )
            clean_mana_cost = mana_cost.split(":")[1].strip()
            item["mana_cost"] = clean_mana_cost
        except:
            item["mana_cost"] = 0
        return item
