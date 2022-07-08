import helpers
from utils.clean import clean_str, clean_list, normalize_str
from utils.filters import remove_basic_lands
from src.card.card_controller import Card
from observability.execution_time import check_execution_time
from typing import Union


class Deck(object):
    """
    Class used as abstraction for a domain object deck
    """

    def __init__(self, raw_data: dict):
        self.raw_data: dict = raw_data
        self.domain_helper: helpers.Domain = helpers.Domain()
        builder: SectionsBuilder = SectionsBuilder(self.raw_data)
        self.sections: list = builder.build()


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

    @check_execution_time
    def build(self):
        """
        This method is used to build a specific section
        """
        for card in self.raw_cards:
            if type(card) == dict:
                new_card: Card = Card(card)
                self.cards_cuantity[str(new_card)] = card.get("cuantity")
                self.cards.append(new_card)
            elif type(card) == tuple:
                self.cards_cuantity[str(card)] = card[1]
                self.cards.append(card[0])
            else:
                raise Exception("format to build sections not allowed")

    def get_cards(self) -> list:
        """
        this methods is used to retrieve the cards from a section
        :return self.cards: a list with the cards in the section
        """
        return self.cards


class SectionsBuilder:
    """
    This class works as a factory to abstract the creations
    of the sections of a deck
    """

    def __init__(self, cards: Union[list, dict]):
        self.raw_cards: Union[list, dict] = cards
        self.domain_helper: helpers.Domain = helpers.Domain()
        self.sections: list = []

    def build(self):
        """
        This is the method with the objective of
        create the sections
        """
        if "cards" in self.raw_cards.keys():
            self.build_from_cards_list()
        elif "sections" in self.raw_cards.keys():
            self.build_from_defined()
        else:
            raise Exception("format for build sections not allowed ")
        return self.sections

    def build_from_cards_list(self):
        """
        This methods build the sections when the raw_data
        does not has defined the sections
        """
        types: dict = {}
        raw_cards = list(filter(remove_basic_lands, self.raw_cards.get("cards")))
        for raw_card in raw_cards:
            clean_card: Card = Card(raw_card)
            card_type: str = normalize_str(clean_card.get_type())
            if card_type in types.keys():
                types[card_type].append(clean_card)
            else:
                types[card_type]: list = [clean_card]

    # @check_execution_time
    def build_from_defined(self):
        """
        Method used to build deck information when the
        raw data becomes with sections specified
        """
        for section in self.raw_cards.get("sections").keys():
            cards: list = self.raw_cards.get("sections").get(section)
            name: str = clean_str(section)
            if name in self.domain_helper.allowed_sections:
                if name == "lands":
                    cards = list(filter(remove_basic_lands, cards))
                cards = clean_list(cards)
                self.sections.append(Section(cards, name))
