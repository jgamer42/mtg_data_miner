import helpers
def remove_basic_lands(card: dict) -> bool:
    domain_helper: helpers.Domain = helpers.Domain()
    cards_to_avoid: list = domain_helper.basic_lands
    return card.get("name", "").lower() not in cards_to_avoid
