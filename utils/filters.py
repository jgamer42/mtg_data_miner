import helpers


def remove_basic_lands(card: dict) -> bool:
    domain_helper: helpers.Domain = helpers.Domain()
    cards_to_avoid: tuple = domain_helper.basic_lands
    return card.get("name", "").lower() not in cards_to_avoid


def allowed_sets(set_info: dict) -> bool:
    domain_helper: helpers.Domain = helpers.Domain()
    return set_info.get("set_type", "").lower() in domain_helper.allowed_sets
