import helpers
import requests
from operator import itemgetter
from requests.models import Response
from utils.filters import allowed_sets


class Scryfall:
    """
    Class used as integration to scryfall API
    """

    def __init__(self):
        self.base_url: str = "https://api.scryfall.com"
        self.domain_helper: helpers.Domain = helpers.Domain()

    def get_card_info_by_name(self, card_name: str) -> dict:
        """
        Method used to get detailed card information
        :param card_name: Str with the name of the card to find
        :return output: dict with the card information
        """
        data: Response = requests.get(f"{self.base_url}/cards/named?fuzzy={card_name}")
        if data.status_code != 200:
            raise Exception("Card not found try again")
        return data.json()

    def get_sets(self) -> list:
        """
        Method used to get detailed set information
        :return output: a list sorted by release date with the sets information
        """
        data: Response = requests.get(f"{self.base_url}/sets")
        procesed_data: dict = data.json().get("data", [])
        if data.status_code != 200:
            raise Exception("Card not found try again")
        output = list(filter(allowed_sets, procesed_data))
        output.sort(key=itemgetter("released_at"))
        return output
