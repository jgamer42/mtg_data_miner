import sys
import json
import requests
from io import TextIOWrapper
from requests.models import Response
sys.path.append("../../")
from utils import export 
from utils.config_helper import configHelper
from typing import *


def search_real_set(reprints:list)->list:
    legals:dict = load_context("legals")
    legal_reprint:str = ""
    for reprint in reprints:
        if reprint in legals.keys() or reprint in ["VOW"]:
            legal_reprint = reprint
            break
    try:
        return [legals[legal_reprint],legal_reprint]
    except:
        return ["Innistrad: Crimson Vow",legal_reprint]

def get_card_info_by_name(card_name:str,return_rarity)->dict:
    config_helper:configHelper = configHelper()
    noise_sets:dict = load_context("noised")
    api_url:str = config_helper.get_mtg_api_card()
    all_card_info:Response = requests.get(f"{api_url}/cards?name={card_name}")
    card_to_export:dict = all_card_info.json()["cards"][0]
    output:dict = {
        "mana_cost":card_to_export.get("manaCost") or "",
        "set":card_to_export["set"],
        "set_name":card_to_export["setName"],
        "re-prints":card_to_export["printings"],
        "cmc":card_to_export["cmc"],
    }
    if card_to_export.get("set") in noise_sets.keys():
        output["set_name"], output["set"] = search_real_set(card_to_export.get("printings",[]))
    if return_rarity:
        output["rarity"] = card_to_export["rarity"]
    clean_card_name:str = card_to_export['name'].replace(' ','-').replace('//','')
    data_market_path:str = config_helper.get_datamarket_path()
    export.export_data(f"{data_market_path}/cards/{clean_card_name}.json",card_to_export)
    return output

def get_sets()->None:
    config_helper:configHelper = configHelper()
    noised_sets:dict = {}
    legal_sets:dict = {}
    api_url:str = config_helper.get_mtg_api_card()
    raw_sets:Response = requests.get(f"{api_url}/sets")
    sets:List[dict] = raw_sets.json()["sets"]
    for set in sets:
        if set.get("type","").lower() in ["promo","funny","masterpiece","token","box","duel_deck","vanguard","premium_deck","memorabilia","archenemy","commander","masters","planechase","starter","from_the_vault","arsenal"] or set.get("onlineOnly") or set.get("code") in ["DBL","H1R"]:
            noised_sets[set.get("code")]=set.get("name")
        else:
            legal_sets[set.get("code")]=set.get("name")
    export_set_map(noised_sets,"noised")
    export_set_map(legal_sets,"legals")

def export_set_map(noised_sets:dict,name:str)->None:
    config_helper:configHelper = configHelper()
    context_path:str = config_helper.get_context_path()
    output_file:str = f"{context_path}/{name}.json"
    export.export_data(output_file,noised_sets)

def load_context(context:str)->dict:
    config_helper:configHelper = configHelper()
    context_path:str = config_helper.get_context_path()
    file:TextIOWrapper = open(f"{context_path}/{context}.json","r")
    raw_data:dict = json.load(file)
    file.close()
    return raw_data

def get_formats():
    pass

if __name__ == "__main__":
    get_sets()