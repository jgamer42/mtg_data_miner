
import scrapy
from lxml import html


class MtgTop8DecksEvents(scrapy.Spider):
    name: str = "mtg_top8_decks_events"
    custom_settings: dict = {"ROBOTSTXT_OBEY": False, "CONCURRENT_REQUESTS": 100}
    formats_helper: dict = {
        "standard": "ST",
        "pioneer": "PI",
        "modern": "MO",
        "pauper": "PAU",
    }
    memory: list = []
    aux = ""
    base_url: str = "https://mtgtop8.com"

    def __init__(self, format: str, *args, **kwargs):
        super(MtgTop8DecksEvents, self).__init__(*args, **kwargs)
        normalized_format: str = self.formats_helper.get(format)
        self.format = format
        self.start_urls: list = [f"{self.base_url}/format?f={normalized_format}"]
    def parse(self, response):
        tournaments: list = list(
            set(response.xpath("//td[@width='70%']/a/@href").getall())
        )
        for tournament in tournaments:
            tournament_url: str = f"{self.base_url}/{tournament}"
            self.aux = tournament_url
            yield response.follow(url=tournament_url, callback=self.tournaments)

    def tournaments(self, response):
        decks: list = response.xpath(
            "//div[@id='top8_list']/div/div/div/div/a"
        ).getall()
        if not decks:
            decks = response.xpath("//div[@style='flex:1;']/div[1]/a").getall()
        for deck in decks:
            try:
                deck_loaded = html.fromstring(deck)
                deck_link: str = deck_loaded.xpath("@href")[0]
                link: str = f"{self.base_url}/event{deck_link}"
                if "player" not in link:
                    deck_name: str = deck_loaded.xpath("text()")[0]
                    yield response.follow(
                        url=link,
                        callback=self.decks,
                        cb_kwargs={"deck_name": deck_name},
                    )
            except Exception as e:
                continue

    def decks(self, response, deck_name: str):

        deck = {
            "name": deck_name,
            "link": response.url,
            "format": self.format,
            "cards": [],
        }
        cards = response.xpath(
            "//div[position()<3]/div[@class='deck_line hover_tr']"
        ).getall()
        for card in cards:
            c = self.process_card(card)
            deck["cards"].append(c)
        return deck

    def process_card(self, raw_card: str):
        loaded_card = html.fromstring(raw_card)
        card_name: str = loaded_card.xpath("//span/text()")[0]
        cuantity: str = loaded_card.xpath("//div/text()")[0]
        card: dict = {
            "name": card_name,
            "cuantity": cuantity,
            "rarity": "",
            "mana_cost": "",
        }
        return card
