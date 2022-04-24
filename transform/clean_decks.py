import sys

sys.path.append("../")
import re
import json
import argparse
from datetime import datetime
from io import TextIOWrapper
from utils import export, clean
from extract.API import mtg_api
from utils.config_helper import configHelper
from utils.context_helper import contextHelper


def load_raw_data(format: str) -> dict:
    config_helper: configHelper = configHelper()
    path_of_file: str = config_helper.get_dataset_path() + f"/{format}.json"
    file: TextIOWrapper = open(path_of_file, "r")
    raw_data = json.load(file)
    file.close()
    return raw_data


def clean_raw_data(data: dict) -> None:
    for key in data.keys():
        if type(data[key]) == dict:
            clean.clean_dict(data[key])
        elif type(data[key]) == list:
            clean.clean_list(data[key])
        elif type(data[key]) == str:
            data[key] = data[key].replace("\n", "").strip()
            data[key] = data[key].replace("\xa0", "").strip()


def metagame_percentage(raw_text: str) -> str:
    match: list = re.findall(r"[0-9]+\.[0-9]+%", raw_text)
    return match[0].strip()


def total_counts_in_metagame(raw_text: str) -> str:
    match: list = re.findall(r"\([0-9]+\)", raw_text)
    return match[0].replace("(", "").replace(")", "").strip()


def export_data(data_to_export: dict) -> None:
    config_helper: configHelper = configHelper()
    data_market_path: str = config_helper.get_datamarket_path()
    date: str = datetime.now().strftime("%Y-%m-%d")
    deck_name: str = data_to_export["name"].replace(" ", "-")
    output_file: str = f"{data_market_path}/decks/goldfish_{deck_name}_{date}.json"
    export.export_data(output_file, data_to_export)


def clean_sections(section: dict, format: str) -> dict:
    context_helper: contextHelper = contextHelper()
    posible_sections: list = context_helper.get_posible_card_sections()
    sections: dict = {}
    for s in section:
        cleaned_cards = []
        for p in posible_sections:
            if p in s:
                for card in section[s]:
                    clean_card: dict = clean_cards(card)
                    cleaned_cards.append(clean_card)
                sections[p] = cleaned_cards
    return sections


def clean_cards(noise_card: dict) -> dict:
    output: dict = {"name": noise_card["name"], "cuantity": noise_card["cuantity"]}
    context_helper: contextHelper = contextHelper()
    if output.get("name", "").lower() not in context_helper.get_basic_lands():
        clean_rarity_data: list = re.findall(r"[0-9]?", noise_card.get("rarity", "1"))
        clean_rarity: str = noise_card["rarity"].replace(clean_rarity_data[0], "")
        aditional_fields: dict = mtg_api.get_card_info_by_name(
            output["name"], True if not clean_rarity else False
        )
        output["rarity"] = clean_rarity
        output.update(aditional_fields)
    return output


def main(format: str) -> None:
    raw_data: list = load_raw_data(format)
    for data in raw_data:
        clean_raw_data(data)
        if data.get("format_info") is not None:
            percentage = metagame_percentage(data.get("format_info"))
            total_aparations_in_meta = total_counts_in_metagame(data.get("format_info"))
            data["format_info"] = {
                "percentage": percentage,
                "count": total_aparations_in_meta,
            }
        data["sections"] = clean_sections(data.get("sections"), data.get("format"))
        export_data(data)


def get_args() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--format",
        required=True,
        help="The format to clean",
    )
    return vars(parser.parse_args())


if __name__ == "__main__":
    format: dict = get_args().get("format")
    main(format)
