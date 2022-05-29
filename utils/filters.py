from utils.context_helper import contextHelper


def remove_basic_lands(card: dict):
    context_helper: contextHelper = contextHelper()
    cards_to_avoid: list = context_helper.get_basic_lands()
    return card.get("name").lower() not in cards_to_avoid
