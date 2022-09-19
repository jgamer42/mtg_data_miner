import helpers
from src.card.card_controller import Card
from utils.clean import normalize_dict


class Section(object):
    """
    Class used as abstraction of a section
    section: group of cards of the same type
    """

    def __init__(self, cards: list, name):
        self.domain_helper: helpers.Domain = helpers.Domain()
        self.cards_cuantity: dict = {}
        self.raw_cards: list = cards
        self.cards: list = []
        self.name: str = name
        self.build()

    def build(self):
        """
        This method is used to build a specific section
        """
        for card in self.raw_cards:
            if type(card) == dict:
                new_card: Card = Card(card)
                self.cards_cuantity[str(new_card)] = int(card.get("cuantity", 0))
                self.cards.append(new_card)
            elif type(card) == tuple:
                self.cards_cuantity[str(card[0])] = int(card[1])
                self.cards.append(card[0])
            else:
                raise Exception("format to build sections not allowed")

    def get_info(self, format: str) -> dict:
        """
        Method used to build the basic information for a section
        :param format: the name of the format that belongs this sections Ie 'standard'
        :return dict: a dict with the information
        """
        output: dict = {}
        colors: dict = {}
        collections: dict = {}
        reserved_list_count: int = 0
        edh_rank_average: float = 0
        penny_rank_average: float = 0
        cards_count: int = 0
        for card in self.cards:
            card_cuantity: int = int(self.cards_cuantity.get(str(card), 0))
            cards_count += card_cuantity
            card_collection: str = card.first_set_in_format(format)
            color: str = card.clean_color
            if f"{self.name}_{card.rarity}" in output.keys():
                output[f"{self.name}_{card.rarity}"] += card_cuantity
            else:
                output[f"{self.name}_{card.rarity}"] = card_cuantity
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
                edh_rank_average += float(card.edhrec_rank)
            if card.penny_rank:
                penny_rank_average += float(card.penny_rank)
        output.update(
            {
                f"{self.name}_cards": cards_count,
                f"{self.name}_domain_color": max(colors, key=lambda x: colors[x])
                if colors != {}
                else "not info",
                f"{self.name}_domain_collection": max(
                    collections, key=lambda x: collections[x]
                )
                if collections != {}
                else "not info",
                f"{self.name}_reserved_cards": reserved_list_count,
                f"{self.name}_avg_edhreck_rank": float(
                    edh_rank_average / len(self.cards)
                )
                if len(self.cards) > 0
                else float("nan"),
                f"{self.name}_avg_penny_rank": float(
                    penny_rank_average / len(self.cards)
                )
                if len(self.cards) > 0
                else float("nan"),
            }
        )
        return normalize_dict(output)
