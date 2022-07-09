import helpers
from .sections import SectionsBuilder


class Deck(object):
    """
    Class used as abstraction for a domain object deck
    """

    def __init__(self, raw_data: dict):
        self.attributes: list = ["source", "name", "link", "format", "format_info"]
        self.name: str = ""
        self.format: str = ""
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
