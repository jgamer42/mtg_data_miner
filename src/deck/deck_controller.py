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
        self.attributes = ["source", "name", "link", "format", "format_info"]
        for key in raw_data:
            if key in self.attributes:
                setattr(self, key, raw_data.get(key, None))
        self.raw_data: dict = raw_data
        self.domain_helper: helpers.Domain = helpers.Domain()
        self.get_deck_strategy()
        builder: SectionsBuilder = SectionsBuilder(self.raw_data)
        self.sections: list = builder.build()

    def get_atributes(self) -> dict:
        output: dict = {}
        for attribute in self.attributes:
            output[attribute] = getattr(self, attribute, None)
        return output

    def __str__(self) -> str:
        return self.name

    # @check_execution_time
    def get_deck_strategy(self):
        """
        Method used to determine which strategy could have a deck
        """
        for strategy in self.domain_helper.strategies:
            if strategy in self.name:
                self.strategy: str = strategy
                break

    def get_info(self):
        basic_data: dict = self.get_atributes()
        sections_data: dict = self.get_sections_data()
        print(sections_data)

    def get_sections_data(self) -> dict:
        output: dict = {}
        for section in self.sections:
            output.update(section.get_info(self.format))
        return output

    def get_domain_collection(self) -> str:
        pass

    def get_domain_color(self) -> str:
        pass

    def get_reserved_cards_list(self) -> int:
        pass

    def get_prices(self) -> int:
        pass

    def get_rarity(self) -> int:
        pass

    def get_mana_wave(self) -> int:
        pass


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
                self.cards_cuantity[str(new_card)] = card.get("cuantity")
                self.cards.append(new_card)
            elif type(card) == tuple:
                self.cards_cuantity[str(card[0])] = card[1]
                self.cards.append(card[0])
            else:
                raise Exception("format to build sections not allowed")

    @check_execution_time
    def get_info(self, format) -> dict:
        output: dict = {}
        colors: dict = {}
        cards_count: int = 0
        for card in self.cards:
            card_cuantity: int = int(self.cards_cuantity.get(str(card), 0))
            cards_count += card_cuantity
            if f"{self.name}_{card.rarity}" in output.keys():
                output[f"{self.name}_{card.rarity}"] += card_cuantity
            else:
                output[f"{self.name}_{card.rarity}"] = card_cuantity

        output.update(
            {
                f"{self.name}_cards": cards_count,
                # f"{self.name}_collection": self.get_domain_collection(format),
                # f"{self.name}_color": self.get_domain_color(),
                # f"{self.name}_reserved_cards": self.get_reserved_cards_list(),
            }
        )
        return output

    def get_domain_collection(self, format) -> str:
        return "coleccion"

    def get_domain_color(self) -> str:
        return "color"

    def get_reserved_cards_list(self) -> int:
        return 1

    def get_total_cards(self) -> int:
        return 1


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

    @check_execution_time
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
            card_type: str = normalize_str(clean_card[0].get_type())
            if card_type in types.keys():
                types[card_type].append(clean_card)
            else:
                types[card_type]: list = [clean_card]
        for type in types.keys():
            new_section: Section = Section(types[type], type)
            self.sections.append(new_section)

    @check_execution_time
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
