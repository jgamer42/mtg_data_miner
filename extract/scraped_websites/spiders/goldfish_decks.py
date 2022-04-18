import scrapy
from lxml import html, etree


class GoldFishSpider(scrapy.Spider):
    name = "goldfish_decks"
    formats = ["standard", "modern", "pioneer", "pauper"]
    staples_urls = [
        f"https://www.mtggoldfish.com/metagame/{game_format}" for game_format in formats
    ]
    start_urls = staples_urls
    custom_settings = {"ROBOTSTXT_OBEY": True, "CONCURRENT_REQUESTS": 100}

    def parse(self, response):
        format = response._get_url().split("/")[-1]
        decks = response.xpath(
            "//div[@class='archetype-tile-title']/span[@class='deck-price-paper']/a/@href"
        ).getall()
        meta = response.xpath(
            "//div[@class='archetype-tile-statistic-value' and contains(text(),'%')]"
        ).extract()

        for i, deck_link in enumerate(decks):
            link = deck_link.replace("#paper", "#arena")
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

    def deck_section(self, response, format, meta_info=None):
        title = response.xpath("//h1[@class='title']/text()").get()
        row_table = response.xpath("//div[@id='tab-arena']/div/table").get()
        row_table_loaded = html.fromstring(row_table)
        headers = row_table_loaded.xpath("//tr[@class='deck-category-header']")
        cards = row_table_loaded.xpath("//tr")
        deck = {
            "name": title,
            "format": format,
            "format_info": meta_info,
            "sections": {},
            "price": "",
        }
        for i in range(len(headers) - 1):
            aux = headers[i]
            section = aux.text_content().strip().replace("\n", "")
            if section not in deck["sections"].keys():
                deck["sections"][section] = []
            current_header = cards.index(aux)
            next_header = cards.index(headers[i + 1])
            cards_in_section = cards[current_header + 1 : next_header]
            for card in cards_in_section:
                card_inner_html = etree.tostring(card)
                processed_card = self.card_section(card_inner_html)
                deck["sections"][section].append(processed_card)

        return deck

    def card_section(self, raw_card):
        loaded_card = html.fromstring(raw_card)

        name = loaded_card.xpath("//a/text()")
        cuantity = loaded_card.xpath("//td[@class='text-right']/text()")
        rarity = loaded_card.xpath(
            "//td[@class='price-arena-rarity text-right']/text()"
        )
        mana_cost = loaded_card.xpath("//span[@class='manacost']/@aria-label")
        if mana_cost != []:
            mana_cost = mana_cost[0].split(":")[-1]
        else:
            mana_cost = 0
        card_dict = {
            "name": name[0],
            "cuantity": cuantity[0],
            "rarity": rarity[0],
            "mana_cost": mana_cost,
            "price": "",
        }

        return card_dict
