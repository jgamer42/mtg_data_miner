import sys

from black import out
import helpers

sys.path.append("/home/user/Escritorio/code/mtg_data_miner")
from data_sources import API
from observability.execution_time import check_execution_time
from utils.clean import normalize_str


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
        self.mtg_api: API.MtgApi = API.MtgApi()
        self.get_info()

    def __str__(self):
        return self.name

    # @check_execution_time
    def get_info(self):
        """
        Method used to load card information, it could come from API or from a manager
        and filter the relevant fields
        """
        data: dict = self.check_if_exists()
        if data == {}:
            aditional_data: dict = self.scryfall.get_card_info_by_name(self.name)
            try:
                card_id: int = aditional_data["multiverse_ids"][0]
                more_data: dict = self.mtg_api.get_card_info_by_id(card_id)
            except:
                more_data: dict = self.mtg_api.get_card_info_by_name(self.name)
            data.update(more_data)
            data.update(aditional_data)
        self.reprints: list = data.get("printings")
        self.mana_cost: str = data.get("cmc")
        self.power: str = data.get("power", None)
        self.thoughness: str = data.get("thoughness", None)
        self.colors: list = data.get("colors", None)
        self.colors_identity: list = data.get("corlor_identity")
        self.reserved: bool = data.get("reserved")
        self.prices: dict = data.get("prices")
        self.edhrec_rank: str = data.get("edhrec_rank")
        self.penny_rank: str = data.get("penny_rank")
        self.rarity: str = data.get("rarity")
        self.type: list = [normalize_str(t) for t in data.get("types")]
        self.raw_data: dict = data

    def check_if_exists(self) -> dict:
        """
        This methods checks in the managers if the raw_card information exists
        :return dict: a dict with the raw card information
        """
        return self.raw_data if hasattr(self, "raw_data") else {}

    def first_print_in_format(self, format: str) -> str:
        pass

    def get_type(self) -> str:
        """
        Methodo used to get a specific type for a card
        :return str: A string with the specific type of the card
        """
        output: str = ""
        if len(self.type) == 1:
            output = self.type[0]
        else:
            if "creature" in self.type:
                output = "creature"
            elif "land" in self.type:
                output = "land"
            elif "sorcery" in self.type or "instant" in self.type:
                output = "spell"
            else:
                for type in self.type:
                    if type in self.domain_helper.allowed_sections:
                        output = type
                        break
        return output
