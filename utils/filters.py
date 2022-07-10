import sys

sys.path.append("/home/user/Escritorio/code/mtg_data_miner")
import helpers
import re


def remove_basic_lands(card: dict) -> bool:
    domain_helper: helpers.Domain = helpers.Domain()
    cards_to_avoid: tuple = domain_helper.basic_lands
    return card.get("name", "").lower() not in cards_to_avoid


def allowed_sets(set_info: dict) -> bool:
    domain_helper: helpers.Domain = helpers.Domain()
    return set_info.get("set_type", "").lower() in domain_helper.allowed_sets


def find_price_in_str(raw_str: str) -> str:
    clean = re.findall(r"\$\d+.\d+|\$NaN", raw_str)
    return clean[0]
