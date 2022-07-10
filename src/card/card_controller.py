from operator import itemgetter
import helpers
from data_sources import API
from observability.execution_time import check_execution_time
from utils.clean import normalize_str
from .manager.file_system import FileSystem


class Singelton(type):
    _instances: dict = {}
    """
    Class used as a singelton implementation
    this singelton implementation depends 
    of the format that is go to be loaded
    """

    def __call__(self, *args, **kwargs):
        card_name: str = kwargs.get("card_information", args[0])["name"]
        if card_name not in self._instances.keys():
            new_instance: Card = super().__call__(*args, **kwargs)
            self._instances[card_name] = new_instance
        return self._instances[card_name]


class Card(metaclass=Singelton):
    def __init__(self, card_information: dict):
        self.domain_helper: helpers.Domain = helpers.Domain()
        self.name: str = card_information.get("name", "")
        self.scryfall: API.Scryfall = API.Scryfall()
        self.mtgstocks: API.MtgStocks = API.MtgStocks()
        self.colors: list = []
        self.printings: list = []
        self.color_identity: list = []
        self.cmc: float = 0.0
        self.prices: dict = self.mtgstocks.get_prices(self.name)
        self.reserved: bool = False
        self.rarity: str = ""
        self.edhrec_rank: int = 0
        self.penny_rank: int = 0
        self.clean_type: str = ""
        self.clean_color: str = ""
        self.clean_attributes: list = [
            "printings",
            "cmc",
            "power",
            "thoughness",
            "colors",
            "color_identity",
            "reserved",
            "edhrec_rank",
            "penny_rank",
            "rarity",
            "type_line",
        ]
        self.managers: dict = {"file_system": FileSystem(self)}
        self.get_info()
        self.get_color()
        self.get_type()

    def __str__(self):
        return self.name

    def get_info(self):
        """
        Method used to load card information, it could come from API or from a manager
        and filter the relevant fields
        """
        data: dict = {}
        if not self.check_if_exists():
            aditional_data: dict = self.scryfall.get_card_info_by_name(self.name)
            aditional_data["printings"] = self.scryfall.get_card_printings(
                aditional_data["prints_search_uri"]
            )
            data.update(aditional_data)
        else:
            raw_data: dict = self.load()
            data.update(raw_data)
        for key in data:
            if key in self.clean_attributes:
                setattr(self, key, data.get(key, None))
        self.type: list = normalize_str(data.get("type_line"))
        self.raw_data: dict = data
        self.managers["file_system"] = FileSystem(self)

    def check_if_exists(self) -> bool:
        """
        This methods checks in the managers if the raw_card information exists
        :return bool: a flag if the data exists or not
        """
        return self.managers["file_system"].find()

    def get_color(self):
        """
        Method used to define the color of a card Ie :Rakdos ,Gruul, Green
        :return color: A str with the color of the card
        """
        color: str = ""
        if hasattr(self, "colors") and self.colors != []:
            self.colors.sort()
            color = self.domain_helper.colors_map.get("".join(self.colors), "colorless")
        else:
            if self.color_identity != []:
                self.color_identity.sort()
                color = self.domain_helper.colors_map.get(
                    "".join(self.color_identity), "colorless"
                )
            else:
                color = "colorless"
        self.clean_color = color

    def first_set_in_format(self, format: str) -> str:
        """
        Method used to determine which was the first print of a card
        in a given format
        :param format: the name of the format to find Ie 'standard','modern'
        :output str: the name of the first set where was printed a card
        """
        context_helper: helpers.Context = helpers.Context(format)
        reprints: list = []
        for set in self.printings:
            posible_set: dict = context_helper.context_data.get(set, {})
            if posible_set:
                reprints.append(posible_set)
        reprints.sort(key=itemgetter("released"))
        return reprints[0].get("name")

    def get_type(self):
        """
        Methodo used to get a specific type for a card
        :return str: A string with the specific type of the card
        """
        output: str = ""
        if "//" in self.type:
            self.type = self.type.split("//")[0]
        if "creature" in self.type:
            output = "creature"
        elif "sorcery" in self.type or "instant" in self.type:
            output = "spell"
        elif "artifcat" in self.type:
            output = "artifact"
        elif "enchantment" in self.type:
            output = "enchantment"
        elif "artifact" in self.type:
            output = "artifact"
        elif "planeswalker" in self.type:
            output = "planeswalker"
        elif "land" in self.type:
            output = "land"
        self.clean_type = output

    def get_prices(self) -> dict:
        """
        Method used to return the dict of prices
        :return output: a dict the prices in tix,usd,eur
        """
        return self.prices

    def export(self):
        self.managers["file_system"].export("json")

    def load(self) -> dict:
        return self.managers["file_system"].load()
