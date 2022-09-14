from telethon.tl.types import PeerChannel
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetInlineBotResultsRequest
from telethon.tl.functions.messages import SendInlineBotResultRequest
import functools

"""api_id = "10695897"
api_hash = "11b26c1d85ab1f7d15362211b2f08b62"

api_hash = str(api_hash)
phone = "+573145373048"
username = "@jgamer42"
client = TelegramClient(username, api_id, api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))
    user_input_channel = "https://t.me/crinto_automation"
    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)
    bot_results = await client(GetInlineBotResultsRequest(
    "@MTGStocksBot ", my_channel, 'llanowar elves',""
    ))
    id_message = vars(bot_results.results[0]).get("id")
    await client(SendInlineBotResultRequest(my_channel,bot_results.query_id,id_message))

with client:
    client.loop.run_until_complete(main(phone))"""


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


class Test:
    api_id = "10695897"
    api_hash = "11b26c1d85ab1f7d15362211b2f08b62"
    api_hash = str(api_hash)
    phone = "+573145373048"
    username = "@jgamer42"
    client = TelegramClient(username, api_id, api_hash)

    def __init__(self):
        self.client = self.client
        self.login()

    @async_handler(client=client)
    async def login(self):
        print("Client Created")
        if await self.client.is_user_authorized() == False:
            await self.client.send_code_request(self.phone)
            try:
                await self.client.sign_in(self.phone, input("Enter the code: "))
            except SessionPasswordNeededError:
                await self.client.sign_in(password=input("Password: "))

    @async_handler(client=client)
    async def send_price_message(self, card_name):
        user_input_channel = "test"
        if user_input_channel.isdigit():
            entity = PeerChannel(int(user_input_channel))
        else:
            entity = user_input_channel

        my_channel = await self.client.get_entity(entity)
        bot_results = await self.client(
            GetInlineBotResultsRequest("@MTGStocksBot ", my_channel, card_name, "")
        )
        id_message = vars(bot_results.results[0]).get("id")
        await self.client(
            SendInlineBotResultRequest(my_channel, bot_results.query_id, id_message)
        )
        return 5


a = Test()
print(a.send_price_message("sol ring"))
