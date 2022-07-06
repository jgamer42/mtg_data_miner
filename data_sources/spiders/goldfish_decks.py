import scrapy
from lxml import html, etree


class GoldFishDecks(scrapy.Spider):
    """
    Spider used to retrieve data from mtg goldfish decks sections
    """

    name: str = "goldfish_decks"
    custom_settings: dict = {"ROBOTSTXT_OBEY": True, "CONCURRENT_REQUESTS": 100}

    def __init__(self, format: str, *args, **kwargs):
        """
        Constructor of the object
        :param format: Is a str with the format to scrape
        """
        super(GoldFishDecks, self).__init__(*args, **kwargs)
        self.start_urls: list = [f"https://www.mtggoldfish.com/metagame/{format}"]

    def parse(self, response):
        """
        Start of the scraper
        """
        format: str = response._get_url().split("/")[-1]
        decks: list = response.xpath(
            "//div[@class='archetype-tile-title']/span[@class='deck-price-paper']/a/@href"
        ).getall()
        meta: list = response.xpath(
            "//div[@class='archetype-tile-statistic-value' and contains(text(),'%')]"
        ).extract()

        for i, deck_link in enumerate(decks):
            link: str = deck_link.replace("#paper", "#arena")
            try:
                yield response.follow(
                    url=link,
                    callback=self.deck_section,
                    cb_kwargs={"format": format, "meta_info": meta[i]},
                )
            except:
                yield response.follow(
                    url=link, callback=self.deck_section, cb_kwargs={"format": format}
                )

    def deck_section(self, response, format: str, meta_info=None):
        """
        Function used to retrieve information from a deck section
        :param response: Response object with the information from the page
        :param format: Is a str with the format to scrape
        :param meta_info: A dict with metagame percentage if available
        :return deck: A dict with the raw deck information
        """
        title: str = response.xpath("//h1[@class='title']/text()").get()
        row_table: str = response.xpath("//div[@id='tab-arena']/div/table").get()
        row_table_loaded = html.fromstring(row_table)
        headers = row_table_loaded.xpath("//tr[@class='deck-category-header']")
        cards = row_table_loaded.xpath("//tr")
        deck: dict = {
            "source":self.name,
            "name": title,
            "format": format,
            "format_info": meta_info,
            "sections": {},
            "price": "",
            "link": response.url,
        }
        for i in range(len(headers) - 1):
            aux = headers[i]
            section: str = aux.text_content().strip().replace("\n", "")
            if section not in deck["sections"].keys():
                deck["sections"][section] = []
            current_header = cards.index(aux)
            next_header = cards.index(headers[i + 1])
            cards_in_section = cards[current_header + 1 : next_header]
            for card in cards_in_section:
                card_inner_html: str = etree.tostring(card)
                processed_card = self.card_section(card_inner_html)
                deck["sections"][section].append(processed_card)

        return deck

    def card_section(self, raw_card: str):
        """
        Function used to retrieve information from a specific card
        :param raw_card: Str with the html from the card
        :return card: A dict with the raw deck information
        """
        loaded_card = html.fromstring(raw_card)

        name: str = loaded_card.xpath("//a/text()")
        cuantity: str = loaded_card.xpath("//td[@class='text-right']/text()")
        rarity: str = loaded_card.xpath(
            "//td[@class='price-arena-rarity text-right']/text()"
        )
        raw_mana_cost: list = loaded_card.xpath("//span[@class='manacost']/@aria-label")
        if raw_mana_cost != []:
            mana_cost = raw_mana_cost[0].split(":")[-1]
        else:
            mana_cost = 0
        card_dict: dict = {
            "name": name[0],
            "cuantity": cuantity[0],
            "rarity": rarity[0],
            "mana_cost": mana_cost,
        }

        return card_dict
