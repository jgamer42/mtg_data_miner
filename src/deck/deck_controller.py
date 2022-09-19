import helpers
from observability.execution_time import check_execution_time
from .sections import SectionsBuilder
from utils.clean import normalize_dict


class Deck(object):
    """
    Class used as abstraction for a domain object deck
    """

    def __init__(self, raw_data: dict):
        self.attributes: list = ["source", "name", "link", "format", "format_info"]
        self.name: str = ""
        self.format: str = ""
        self.cards: list = []
        self.cards_cuantity: dict = {}
        self.raw_data: dict = raw_data
        self.domain_helper: helpers.Domain = helpers.Domain()
        self.get_deck_strategy()
        builder: SectionsBuilder = SectionsBuilder(self.raw_data)
        self.sections: list = builder.build()
        for key in raw_data:
            if key in self.attributes:
                setattr(self, key, raw_data.get(key, None))
        for section in self.sections:
            self.cards += section.cards
            self.cards_cuantity.update(section.cards_cuantity)

    def __str__(self) -> str:
        return self.name

    def get_atributes(self) -> dict:
        """
        Method used to get the basic attributes of Deck
        :return output: a dict with the data required
        """
        output: dict = {}
        for attribute in self.attributes:
            output[attribute] = getattr(self, attribute, None)
        return output

    def get_deck_strategy(self):
        """
        Method used to determine which strategy could have a deck
        """
        for strategy in self.domain_helper.strategies:
            if strategy in self.name:
                self.strategy: str = strategy
                break

    def get_info(self):
        mana_wave: dict = {}
        collections: dict = {}
        colors: dict = {}
        rarity: dict = {}
        card_colors: list = []
        edh_rank_average: int = 0
        penny_rank_average: int = 0
        reserved_list_count: int = 0
        basic_data: dict = self.get_atributes()
        sections_data: dict = self.get_sections_data()
        for card in self.cards:
            card_name: str = str(card)
            card_cuantity: int = self.cards_cuantity.get(card_name, 0)
            color: str = card.clean_color
            card_collection: str = card.first_set_in_format(self.format)
            cmc: int = int(card.cmc)
            if f"{card.rarity}" in rarity.keys():
                rarity[f"{card.rarity}"] += card_cuantity
            else:
                rarity[f"{card.rarity}"] = card_cuantity

            if color in colors.keys():
                colors[color] += card_cuantity
            else:
                colors[color] = card_cuantity
            if card_collection in collections.keys():
                collections[card_collection] += card_cuantity
            else:
                collections[card_collection] = card_cuantity
            if card.reserved:
                reserved_list_count += card_cuantity
            if card.edhrec_rank:
                edh_rank_average += card.edhrec_rank
            if card.penny_rank:
                penny_rank_average += card.penny_rank
            if card.clean_type != "land":
                if f"turn_{cmc}" in mana_wave.keys():
                    mana_wave[f"turn_{cmc}"] += card_cuantity
                else:
                    mana_wave[f"turn_{cmc}"] = card_cuantity
            if hasattr(card, "colors") and card.colors != []:
                card_colors += card.colors
            else:
                card_colors += card.color_identity

        card_colors = list(set(card_colors))
        card_colors.sort()
        data: dict = {
            f"domain_color": max(colors, key=lambda x: colors[x]),
            f"domain_collection": max(collections, key=lambda x: collections[x]),
            f"reserved_cards": reserved_list_count,
            f"avg_edhreck_rank": edh_rank_average / len(self.cards),
            f"avg_penny_rank": penny_rank_average / len(self.cards),
            f"color": self.domain_helper.colors_map["".join(card_colors)],
        }
        data.update(mana_wave)
        data.update(rarity)
        data.update(basic_data)
        data.update(sections_data)
        return normalize_dict(data)

    def get_sections_data(self) -> dict:
        """
        Method used to retrieve all sections information
        :return output: a dict with all sections information
        """
        output: dict = {}
        for section in self.sections:
            output.update(section.get_info(self.format))
        return output

    def export(self):
        for card in self.cards:
            card.export()
