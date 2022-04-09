import os
import datetime
import requests
import json
DATASET_PATH = "/".join(os.path.abspath(__file__).split("/")[:-3])+"/data"
def get_card_info_by_name(card_name):
    all_card_info = requests.get(f"https://api.magicthegathering.io/v1/cards?name={card_name}")
    card_to_export = all_card_info.json()["cards"][0]
    print(card_name)
    output = {
        "mana_cost":card_to_export.get("manaCost") or "",
        "set":card_to_export["set"],
        "set_name":card_to_export["setName"],
        "re-prints":card_to_export["printings"],
        "cmc":card_to_export["cmc"],
    }
    export_card(card_to_export)
    return output


def export_card(card):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    output_file = open(f"{DATASET_PATH}/market/cards/{card['name'].replace(' ','-').replace('//','')}.json","w+")
    json.dump(card,output_file)
    output_file.close()