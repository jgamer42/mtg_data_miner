import datetime
import urllib3
import json

b = urllib3.PoolManager(num_pools=50, maxsize=100)
now = datetime.datetime.now()

# a = b.request("GET","https://api.scryfall.com/cards/named?fuzzy=fable of the mirror",preload_content=False)
# json.loads(a.data.decode("utf-8"))

a = b.request(
    "GET",
    "https://api.scryfall.com/cards/named?fuzzy=fable of the mirror",
    preload_content=False,
)
# json.loads(a.data.decode("utf-8"))
print(type(a))
