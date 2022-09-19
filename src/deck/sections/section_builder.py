import helpers
from utils.clean import normalize_str, clean_str
from src.card.card_controller import Card
from . import Section
from utils.filters import remove_basic_lands
from observability.execution_time import check_execution_time


class SectionsBuilder:
    """
    This class works as a factory to abstract the creations
    of the sections of a deck
    """

    def __init__(self, cards: dict):
        self.raw_cards: dict = cards
        self.domain_helper: helpers.Domain = helpers.Domain()
        self.sections: list = []

    def build(self) -> list:
        """
        This is the method with the objective of
        create the sections
        :return self.sections: a list with created sections
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
        raw_cards: list = list(
            filter(remove_basic_lands, self.raw_cards.get("cards", []))
        )
        for raw_card in raw_cards:
            clean_card: Card = (Card(raw_card), raw_card.get("cuantity"))
            card_type: str = clean_card[0].clean_type
            if card_type in types.keys():
                types[card_type].append(clean_card)
            else:
                types[card_type]: list = [clean_card]
        for type in types.keys():
            new_section: Section = Section(types[type], type)
            self.sections.append(new_section)

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
                self.sections.append(Section(cards, name))
