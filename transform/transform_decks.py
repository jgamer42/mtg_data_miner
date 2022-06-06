import os
import sys
import re

sys.path.append("../")
from datetime import datetime
from utils.config_helper import configHelper
from utils.context_helper import contextHelper
from utils import clean, input_output
from typing import Union, Generator


def load_decks(decks_to_load: list) -> Generator:
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
            collections[card.get("set_name")] += card.get("cuantity")
        else:
            collections[card.get("set_name")] = card.get("cuantity")
    if collections:
        return max(collections)
    else:
        return ""


def match_color(raw_color: str) -> str:
    match: list = re.findall(r"[WUBRG]", raw_color)
    return "".join(list(set(match))).strip()


def color_info(cards: list) -> dict:
    context: contextHelper = contextHelper()
    unique_colors: str = ""
    colors: dict = {}
    for card in cards:
        color: str = match_color(card.get("mana_cost"))
        unique_colors += color
        color_name: str = context.get_color_name(color)
        if color_name in colors.keys():
            colors[color_name] += card.get("cuantity")
        else:
            colors[color_name] = card.get("cuantity")

    real_deck_color: str = "".join(list(set(unique_colors)))
    deck_color: str = context.get_color_name(real_deck_color)
    return {"color": deck_color, "domain": max(colors)}


def mana_wave(cards: Union[dict, list], prename: str = "") -> dict:
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
    if type(cards) == dict:
        for section in cards.keys():
            if section.lower() not in ["lands", "companion"]:
                for card in cards.get(section, []):
                    cmc = int(card.get("cmc"))
                    if cmc >= 5:
                        output[f"{prename}wave_5"] += 1
                    else:
                        output[f"{prename}wave_{cmc}"] += 1
    else:
        for card in cards:
            cmc = int(card.get("cmc"))
            if cmc >= 5:
                output[f"{prename}wave_5"] += 1
            else:
                output[f"{prename}wave_{cmc}"] += 1
    return output


def sections_detailed_info(cards: dict) -> dict:
    output: dict = {}
    context_helper: contextHelper = contextHelper()
    posible_sections: list = context_helper.get_posible_card_sections()
    for section in posible_sections:
        formated_section_name: str = f"{section}_"
        if section in cards.keys():
            output[f"domain_in_{section}"] = domain_collection(cards[section])
            output.update(rarity_of_cards(cards[section], formated_section_name))
            if section.lower() not in ["lands", "companion"]:
                output.update(mana_wave(cards[section], formated_section_name))
                output[f"color_in_{section}"] = color_info(cards[section]).get("domain")
        else:
            output[f"domain_in_{section}"] = None
            output[f"color_in_{section}"] = None
            output.update(mana_wave([], formated_section_name))
            output.update(rarity_of_cards([], formated_section_name))

    return output


def get_deck_strategie(deck_name: str) -> str:
    context_helper: contextHelper = contextHelper()
    output: str = ""
    allow_strategies: list = context_helper.get_strategies()
    for strategi in allow_strategies:
        if strategi in deck_name.lower():
            output = strategi
    return output


if __name__ == "__main__":
    output: list = []
    config_helper: configHelper = configHelper()
    args: dict = config_helper.args_constraint(
        {"source": {"required": True, "help": "Specific website to filter"}}
    )
    format: str = args.get("format", "")
    source: str = args.get("source", "")
    decks_path: str = config_helper.get_clean_decks_path()
    decks: list = [
        decks_path + deck
        for deck in os.listdir(decks_path)
        if format in deck and source in deck
    ]
    deck_loader: Generator = load_decks(decks)
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
            "strategy": deck.get("strategy") or get_deck_strategie(deck.get("name")),
            "date": date,
        }
        cards: list = clean.dict_list_2_list(deck["sections"])
        data_to_export.update(rarity_of_cards(cards))
        data_to_export.update(mana_wave(deck["sections"]))
        data_to_export["domain_collection"] = domain_collection(cards)
        data_to_export.update(sections_detailed_info(deck["sections"]))
        data_to_export.update(color_info(cards))
        output.append(data_to_export)

    input_output.export_csv(
        f"{config_helper.get_dataset_path()}/{source}_decks_{format}_{date}.csv", output
    )
