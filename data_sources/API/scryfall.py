import helpers
import json
from operator import itemgetter
from utils.filters import allowed_sets
from observability.execution_time import check_execution_time
import urllib3
from urllib3.response import HTTPResponse


class Scryfall:
    """
    Class used as integration to scryfall API
    """

    def __init__(self):
        self.base_url: str = "https://api.scryfall.com"
        self.domain_helper: helpers.Domain = helpers.Domain()
        self.api = urllib3.PoolManager(num_pools=50, maxsize=100)

    # @check_execution_time
    def get_card_info_by_name(self, card_name: str) -> dict:
        """
        Method used to get detailed card information
        :param card_name: Str with the name of the card to find
        :return output: dict with the card information
        """
        data: HTTPResponse = self.api.request(
            "GET",
            f"{self.base_url}/cards/named?fuzzy={card_name}",
            preload_content=False,
        )
        if data.status != 200:
            raise Exception("Card not found try again")
        output = json.loads(data.data.decode("utf-8"))
        output["printings"] = self.get_card_printings(output.get("prints_search_uri"))
        return output

    def get_sets(self) -> list:
        """
        Method used to get detailed set information
        :return output: a list sorted by release date with the sets information
        """
        data: HTTPResponse = self.api.request(
            "GET", f"{self.base_url}/sets", preload_content=False
        )
        procesed_data: dict = json.loads(data.data.decode("utf-8"))
        if data.status != 200:
            raise Exception("Card not found try again")
        output = list(filter(allowed_sets, procesed_data))
        output.sort(key=itemgetter("released_at"))
        return output

    def get_card_printings(self, url: str) -> list:
        """
        Method used to get all reprints of a card
        :param url: string with the url with the reprints information
        :return printings: a list with the all reprints of a card
        """
        data: HTTPResponse = self.api.request("GET", url, preload_content=False)
        processed_data: dict = json.loads(data.data.decode("utf-8"))
        card_prints: list = processed_data.get("data", [])
        printings: list = list(set([card.get("set").upper() for card in card_prints]))
        return printings
