import functools
import math
import os
import sys
from operator import itemgetter

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetInlineBotResultsRequest

from utils.filters import find_price_in_str

sys.path.append(os.getenv("MTG_PROJECT_ROOT_PATH", ""))
from observability.execution_time import check_execution_time

load_dotenv()


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance: MtgStocks = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def async_handler(client, *args, **kwargs):
    def handler(method, *args, **kwargs):
        @functools.wraps(method)
        def real_handler(*args, **kwargs):
            output = None
            with client:
                output = client.loop.run_until_complete(method(*args, **kwargs))
            return output

        return real_handler

    return handler


class MtgStocks(metaclass=Singleton):
    api_id: str = os.getenv("TELEGRAM_API_ID", "")
    api_hash: str = os.getenv("TELEGRAM_API_HASH", "")
    phone: str = os.getenv("TELEGRAM_PHONE_NUMBER", "")
    username: str = os.getenv("TELEGRAM_USER", "")
    client: TelegramClient = TelegramClient(username, api_id, api_hash)

    def __init__(self):
        self.login()

    @async_handler(client=client)
    async def login(self):
        if await self.client.is_user_authorized() == False:
            await self.client.send_code_request(self.phone)
            try:
                await self.client.sign_in(self.phone, input("Enter the code: "))
            except SessionPasswordNeededError:
                await self.client.sign_in(password=input("Password: "))

    @async_handler(client=client)
    async def get_prices(self, card_name) -> dict:
        list_prices: list = []
        chanel: str = "test"
        my_channel: object = await self.client.get_entity(chanel)
        bot_results: TelegramClient = await self.client(
            GetInlineBotResultsRequest("@MTGStocksBot ", my_channel, card_name, "")
        )
        prices: list = bot_results.results
        for price in prices:
            aux: dict = {"name": price.title, "id": price.id}
            price_data: str = vars(price.send_message).get("message", "-\n")
            aux["price"] = self.process_message(price_data)
            list_prices.append(aux)
        max_price: dict = max(list_prices, key=lambda x: x["price"])
        min_price: dict = min(list_prices, key=lambda x: x["price"])
        try:
            list_prices.remove(max_price)
        except:
            pass
        try:
            list_prices.remove(min_price)
        except:
            pass
        list_prices.sort(key=itemgetter("price"))
        try:
            avg_price = sum(
                [a["price"] for a in list_prices if not math.isnan(a["price"])]
            ) / len(list_prices)
        except ZeroDivisionError:
            avg_price = 0
        return {"max": max_price["price"], "min": min_price["price"], "avg": avg_price}

    def process_message(self, message_data: str) -> float:
        price: float = float(find_price_in_str(message_data).replace("$", "").strip())
        return price
