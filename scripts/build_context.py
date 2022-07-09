import os
import sys
import json
import logging

sys.path.append(os.getcwd())
from scrapy import signals
from data_sources.API import Scryfall
from data_sources.spiders import MtgWtf
from scrapy.crawler import CrawlerProcess, Crawler

logging.getLogger("scrapy").propagate = False
logging.getLogger("filelock").propagate = False
API: Scryfall = Scryfall()
SETS: list = API.get_sets()
CONTEXT: dict = {
    "vintage": SETS,
    "pauper": SETS,
    "legacy": SETS,
    "standard": [],
    "modern": [],
    "pioneer": [],
}


def handle_scrapped_item(item: dict) -> None:
    global CONTEXT, SETS
    for data in item.get("data", []):
        allowed_set = list(filter(lambda x: x.get("name") == data, SETS))
        CONTEXT.get(item.get("format", ""), []).append(allowed_set)


process = CrawlerProcess()
for form in ["standard", "modern", "pioneer"]:
    crawler = Crawler(MtgWtf)
    crawler.signals.connect(handle_scrapped_item, signal=signals.item_scraped)
    process.crawl(crawler, format=form)
process.start()

for format in CONTEXT.keys():
    data = {}
    for set in CONTEXT[format]:
        if type(set) == list and set:
            data[set[0]["code"].upper()] = {
                "released": set[0]["released_at"],
                "name": set[0]["name"],
            }
        elif type(set) == dict:
            data[set["code"].upper()] = {
                "released": set["released_at"],
                "name": set["name"],
            }
    with open(
        f"/home/user/Escritorio/code/mtg_data_miner/helpers/context/{format}.json", "w+"
    ) as file:
        json.dump(data, file)
        file.close()
