import sys
import json

sys.path.append("/home/user/Escritorio/code/mtg_data_miner")

from observability.execution_time import check_execution_time
import urllib3
from urllib3.response import HTTPResponse


class MtgApi(object):
    """
    Class used as integration to mtg API
    """

    def __init__(self):
        self.base_url: str = "https://api.magicthegathering.io"
        self.version: int = 1
        self.api = urllib3.PoolManager(num_pools=50, maxsize=100)

    @check_execution_time
    def get_card_info_by_name(
        self, card_name: str, additional_filters: dict = {}
    ) -> dict:
        """
        Method used to get detailed card information
        :param card_name: Str with the name of the card to find
        :return output: dict with the card information
        """
        filters: str = ""
        if additional_filters:
            for k in additional_filters.keys():
                filters += f"&{k}={additional_filters[k]}"
        data: HTTPResponse = self.api.request(
            "GET",
            f"{self.base_url}/v{self.version}/cards?name={card_name}{filters}",
            preload_content=False,
        )
        if data.status != 200:
            raise Exception("Card not found")
        output: dict = json.loads(data.data.decode("utf-8"))
        return output["cards"][0]

    @check_execution_time
    def get_card_info_by_id(self, card_id: str) -> dict:
        """
        Method used to get detailed card information
        :param card_id: Str with the multiverse id from the card
        :return output: dict with the card information
        """
        data: HTTPResponse = self.api.request(
            "GET",
            f"{self.base_url}/v{self.version}/cards/{card_id}",
            preload_content=False,
        )
        if data.status != 200:
            raise Exception("Card not found")
        output: dict = json.loads(data.data.decode("utf-8"))
        return output["card"]
