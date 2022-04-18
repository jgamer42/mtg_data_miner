import json
import requests

a = requests.get("https://mtg.wtf/format/pioneer")
print(a.json())
