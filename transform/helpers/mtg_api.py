import os
import requests
import json
DATASET_PATH = "/".join(os.path.abspath(__file__).split("/")[:-3])+"/data"


def search_real_set(reprints):
    print(reprints)
    legals = load_context("legals")
    legal_reprint = ""
    for reprint in reprints:
        if reprint in legals.keys() or reprint in ["VOW"]:
            legal_reprint = reprint
            break
    try:
        return legals[legal_reprint],legal_reprint
    except:
        return "Innistrad: Crimson Vow",legal_reprint

def get_card_info_by_name(card_name,return_rarity):
    noise_sets = load_context("noised")
    
    all_card_info = requests.get(f"https://api.magicthegathering.io/v1/cards?name={card_name}")
    card_to_export = all_card_info.json()["cards"][0]
    output = {
        "mana_cost":card_to_export.get("manaCost") or "",
        "set":card_to_export["set"],
        "set_name":card_to_export["setName"],
        "re-prints":card_to_export["printings"],
        "cmc":card_to_export["cmc"],
    }
    if card_to_export.get("set") in noise_sets.keys():
        print(card_name)
        output["set_name"], output["set"] = search_real_set(card_to_export.get("printings"))
    if return_rarity:
        output["rarity"] = card_to_export["rarity"]
    export_card(card_to_export)
    return output

def get_sets():
    noised_sets = {}
    legal_sets = {}
    sets =requests.get("https://api.magicthegathering.io/v1/sets")
    sets = sets.json()["sets"]
    for set in sets:
        
        if set.get("type").lower() in ["promo","funny","masterpiece","token","box","duel_deck","vanguard","premium_deck","memorabilia","archenemy","commander","masters","planechase","starter","from_the_vault","arsenal"] or set.get("onlineOnly") or set.get("code") in ["DBL","H1R"]:
            noised_sets[set.get("code")]=set.get("name")
        else:
            legal_sets[set.get("code")]=set.get("name")
    export_set_map(noised_sets,"noised")
    export_set_map(legal_sets,"legals")

def get_formats():
    pass

def export_card(card):
    output_file = open(f"{DATASET_PATH}/market/cards/{card['name'].replace(' ','-').replace('//','')}.json","w+")
    json.dump(card,output_file)
    output_file.close()

def export_set_map(noised_sets,name):
    output_file = open(f"{DATASET_PATH}/context/{name}.json","w+")
    json.dump(noised_sets,output_file)
    output_file.close()

def load_context(context):
    global DATASET_PATH
    file = open(DATASET_PATH+f"/context/{context}.json","r+")
    raw_data = json.load(file)
    file.close()
    return raw_data

get_sets()