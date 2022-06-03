import os
import sys

sys.path.append("../")
from datetime import datetime
from utils.config_helper import configHelper
from utils.context_helper import contextHelper
from utils import clean, input_output


def load_decks(decks_to_load: str) -> object:
    for deck in decks_to_load:
        loaded_deck = input_output.load_json(deck)
        yield loaded_deck


def rarity_of_cards(cards: list, prename: str = "") -> dict:
    output = {
        f"{prename}rare": 0,
        f"{prename}comm": 0,
        f"{prename}unc": 0,
        f"{prename}mythic": 0,
    }
    for card in cards:
        clean_rarity: str = card.get("rarity").replace(".", "")
        output[f"{prename}{clean_rarity.lower()}"] += int(card.get("cuantity"))
    return output


def domain_collection(cards: list) -> str:
    collections: dict = {}
    for card in cards:
        if card.get("set_name") in collections.keys():
            collections[card.get("set_name")] += 1
        else:
            collections[card.get("set_name")] = 1
    if collections:
        return max(collections, key=collections.get)
    else:
        return None


def mana_wave(cards: list, prename: str = ""):
    output = {
        f"{prename}wave_0": 0,
        f"{prename}wave_1": 0,
        f"{prename}wave_2": 0,
        f"{prename}wave_3": 0,
        f"{prename}wave_4": 0,
        f"{prename}wave_5": 0,
        f"{prename}wave_6": 0,
        f"{prename}wave_7": 0,
    }
    for card in cards:
        cmc = int(card.get("cmc"))
        if cmc >= 5:
            output[f"{prename}wave_5"] += 1
        else:
            output[f"{prename}wave_{cmc}"] += 1
    return output


def sections_detailed_info(cards: dict):
    output: dict = {}
    context_helper: contextHelper = contextHelper()
    posible_sections: list = context_helper.get_posible_card_sections()
    for section in posible_sections:
        formated_section_name: str = f"{section}_"
        if section in cards.keys():
            output[f"domain_in_{section}"] = domain_collection(cards[section])
            output.update(mana_wave(cards[section], formated_section_name))
            output.update(rarity_of_cards(cards[section], formated_section_name))

        else:
            output[f"domain_in_{section}"] = None
            output.update(mana_wave([], formated_section_name))
            output.update(rarity_of_cards([], formated_section_name))
    return output


if __name__ == "__main__":
    output = []
    config_helper: configHelper = configHelper()
    args: dict = config_helper.args_constraint(
        {"source": {"required": True, "help": "Specific website to filter"}}
    )
    format: str = args.get("format")
    source: str = args.get("source")
    decks_path: str = config_helper.get_clean_decks_path()
    decks: list = [
        decks_path + deck
        for deck in os.listdir(decks_path)
        if format in deck and source in deck
    ]
    deck_loader: object = load_decks(decks)
    date: str = datetime.now().strftime("%Y-%m-%d")
    for deck in deck_loader:
        data_to_export = {
            "name": deck.get("name"),
            "format": deck.get("format", format),
            "deck_percentage": deck.get("format_info").get("percentage")
            if deck.get("format_info")
            else None,
            "count": deck.get("format_info").get("count")
            if deck.get("format_info")
            else None,
            "strategy": deck.get("strategy"),
            "date": date,
        }
        cards: list = clean.dict_list_2_list(deck["sections"])
        data_to_export.update(rarity_of_cards(cards))
        data_to_export.update(mana_wave(cards))
        data_to_export["domain_collection"] = domain_collection(cards)
        data_to_export.update(sections_detailed_info(deck["sections"]))
        output.append(data_to_export)
    input_output.export_csv(
        f"{config_helper.get_dataset_path()}/{source}_decks_{format}_{date}.csv", output
    )
