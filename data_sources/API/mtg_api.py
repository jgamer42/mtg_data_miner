import sys

sys.path.append("/home/user/Escritorio/code/mtg_data_miner")
import requests
from requests.models import Response
from observability.execution_time import check_execution_time
import logging


class MtgApi(object):
    """
    Class used as integration to mtg API
    """

    def __init__(self):
        self.base_url: str = "https://api.magicthegathering.io"
        self.version: int = 1
        self.session: requests.Session = requests.session()

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
        data: Response = self.session.get(
            f"{self.base_url}/v{self.version}/cards?name={card_name}{filters}"
        )
        if data.status_code != 200:
            raise Exception("Card not found")
        return data.json()["cards"][0]

    @check_execution_time
    def get_card_info_by_id(self, card_id: str) -> dict:
        """
        Method used to get detailed card information
        :param card_id: Str with the multiverse id from the card
        :return output: dict with the card information
        """
        data: Response = self.session.get(
            f"{self.base_url}/v{self.version}/cards/{card_id}"
        )
        if data.status_code != 200:
            raise Exception("Card not found")
        return data.json()["card"]
