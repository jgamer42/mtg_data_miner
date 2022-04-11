import os
import re
import json 
import datetime
from helpers import mtg_api
DATASET_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])+"/data"

def load_raw_data():
    global DATASET_PATH
    file = open(DATASET_PATH+"/salida.json","r+")
    raw_data = json.load(file)
    file.close()
    return raw_data

def clean(data):
    for key in data.keys():
        if type(data[key]) == dict:
            clean_dict(data[key])
        elif type(data[key]) == list:
            clean_list(data[key])
        elif type(data[key]) == str:
            data[key] = data[key].replace("\n","").strip()
            data[key] = data[key].replace("\xa0","").strip() 

def clean_dict(data):
    for key in data.keys():
        if type(data[key]) == dict:
            clean_dict(data[key])
        elif type(data[key]) == list:
            clean_list(data[key])
        elif type(data[key]) == str:
            data[key] = data[key].replace("\n","").strip()
            data[key] = data[key].replace("\xa0","").strip()


def clean_list(data):
    for element in data:
        try:
            if type(element) == dict:
                clean_dict(element)
            elif type(element) == list:
                clean_list(element)
            elif type(element) == str:
                element = element.replace("\n","").strip()
                element = element.replace("\xa0","").strip()
        except:
            continue

def metagame_percentage(raw_text):
    match = re.findall(r"[0-9]+\.[0-9]+%",raw_text)
    return match[0].strip()

def total_counts_in_metagame(raw_text):
    match = re.findall(r"\([0-9]+\)",raw_text)
    return match[0].replace("(","").replace(")","").strip()

def export_data(data_to_export):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    output_file = open(f"{DATASET_PATH}/market/decks/goldfish_decks_{data_to_export['name'].replace(' ','-')}_{date}.json","w+")
    json.dump(data_to_export,output_file)
    output_file.close()

def clean_sections(section):
    posible_sections = ["Spells","Artifacts","Lands","Enchantments","Creatures","Planeswalkers"]
    sections = {}
    for s in section:
        cleaned_cards = []
        for p in posible_sections:
            if p in s:
                for card in section[s]:
                    clean_card = clean_cards(card)
                    cleaned_cards.append(clean_card)
                sections[p] = cleaned_cards
    return sections

def clean_cards(noise_card):
    output = {
        "name":noise_card["name"],
        "cuantity":noise_card["cuantity"]

    }
    if output.get("name").lower() not in ["swamp","plains","forest","island","mountain"]:
        clean_rarity = re.findall(r"[0-9]?",noise_card.get("rarity","1"))
        clean_rarity = noise_card["rarity"].replace(clean_rarity[0],"")
        aditional_fields = mtg_api.get_card_info_by_name(output["name"],True if not clean_rarity else False)
        output["rarity"] = clean_rarity
        output.update(aditional_fields)
    return output


if __name__ == '__main__':
    raw_data = load_raw_data()
    for data in raw_data:
        clean(data)
        if data["format_info"] is not None:
            percentage = metagame_percentage(data["format_info"])
            total_aparations_in_meta = total_counts_in_metagame(data["format_info"])
            data["format_info"] = {
                "percentage":percentage,
                "count":total_aparations_in_meta
            }   
        data["sections"] = clean_sections(data["sections"])

        export_data(data)
        break

       