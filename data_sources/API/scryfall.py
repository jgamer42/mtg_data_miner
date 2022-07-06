import requests
from requests.models import Response


class Scryfall:
    """
    Class used as integration to scryfall API
    """

    def __init__(self):
        self.base_url: str = "https://api.scryfall.com"

    def get_card_info_by_name(self, card_name: str) -> dict:
        """
        Method used to get detailed card information
        :param card_name: Str with the name of the card to find
        :return output: dict with the card information
        """
        data: Response = requests.get(f"{self.base_url}/cards/named?fuzzy={card_name}")
        if data.status_code != 200:
            print(data.status_code, data.text)
            raise Exception("Card not found try again")
        return data.json()
