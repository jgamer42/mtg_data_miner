import sys

sys.path.append("../")
import re
from datetime import datetime
from utils import clean, input_output, filters
from extract.API import mtg_api
from utils.config_helper import configHelper
from utils.context_helper import contextHelper


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


def clean_section_name(raw_text: str) -> str:
    aux = re.compile("(\([0-9]+\))(\+[0-9]? MDFCs)?")
    clean = aux.sub("", raw_text)
    return clean.strip()


def export_data(data_to_export: dict, format: str = "") -> None:
    config_helper: configHelper = configHelper()
    data_market_path: str = config_helper.get_datamarket_path()
    date: str = datetime.now().strftime("%Y-%m-%d")
    deck_name: str = data_to_export["name"].replace(" ", "-")
    output_file: str = (
        f"{data_market_path}/decks/goldfish_{format}_{deck_name}_{date}.json"
    )
    input_output.export_json(output_file, data_to_export)


def clean_sections(section: dict, format: str) -> dict:
    context_helper: contextHelper = contextHelper()
    posible_sections: list = context_helper.get_posible_card_sections()
    sections: dict = {}
    for s in section:
        section_name: str = clean_section_name(s)
        cleaned_cards = []
        if section_name in posible_sections:
            for card in section[s]:
                clean_card: dict = clean_cards(card, format)
                cleaned_cards.append(clean_card)
            sections[section_name] = cleaned_cards
            if section_name.lower() == "lands":
                sections[section_name] = list(
                    filter(filters.remove_basic_lands, cleaned_cards)
                )
    return sections


def clean_cards(noise_card: dict, format: str) -> dict:
    output: dict = {"name": noise_card["name"], "cuantity": noise_card["cuantity"]}
    context_helper: contextHelper = contextHelper()
    if output.get("name", "").lower() not in context_helper.get_basic_lands():
        clean_rarity_data: list = re.findall(r"[0-9]?", noise_card.get("rarity", "1"))
        clean_rarity: str = (
            noise_card["rarity"].replace(clean_rarity_data[0], "").replace(".", "")
        )
        aditional_fields: dict = mtg_api.get_card_info_by_name(
            output["name"], True if not clean_rarity else False
        )
        output["rarity"] = clean_rarity
        output.update(aditional_fields)
        set_info: dict = search_real_set(output.get("re-prints", []), format)
        output.update(set_info)
    return output


def search_real_set(reprints: list, format: str) -> dict:
    context_helper: contextHelper = contextHelper()
    legals: dict = context_helper.get_format_information(format)
    allowed_reprints: list = []
    for reprint in reprints:
        if reprint in legals.keys() or reprint in ["VOW"]:
            allowed: dict = legals[reprint]
            allowed.update({"code": reprint})
            allowed_reprints.append(allowed)
    allowed_reprints = sorted(
        allowed_reprints,
        key=lambda rep: datetime.strptime(rep.get("release"), "%m/%d/%Y").date(),
    )
    try:
        return {
            "set_name": allowed_reprints[0].get("name"),
            "set": allowed_reprints[0].get("code"),
        }
    except:
        return {"set_name": "Innistrad: Crimson Vow", "set": "VOW"}


if __name__ == "__main__":
    config_helper: configHelper = configHelper()
    args: dict = config_helper.args_constraint()
    format: str = args.get("format", "")
    path_of_file: str = config_helper.get_dataset_path() + f"/{format}.json"
    raw_data: dict = input_output.load_json(path_of_file)
    for data in raw_data:
        clean_raw_data(data)
        if data.get("format_info") is not None:
            percentage = metagame_percentage(data.get("format_info"))
            total_aparations_in_meta = total_counts_in_metagame(data.get("format_info"))
            data["format_info"] = {
                "percentage": percentage,
                "count": total_aparations_in_meta,
            }
        data["sections"] = clean_sections(data.get("sections"), format)
        export_data(data, format)
