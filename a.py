import datetime
import urllib3
import json

b = urllib3.PoolManager(num_pools=50, maxsize=100)
now = datetime.datetime.now()

# a = b.request("GET","https://api.scryfall.com/cards/named?fuzzy=fable of the mirror",preload_content=False)
# json.loads(a.data.decode("utf-8"))

a = b.request(
    "GET",
    "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A68954295-54e3-4303-a6bc-fc4547a4e3a3&unique=prints",
    preload_content=False,
)
c = json.loads(a.data.decode("utf-8"))
print(c.keys())
print(c["data"][0]["set"])
print(c["data"][1]["set"])
print(c["data"][3]["set"])
