from typing import Dict


class Domain:
    allowed_formats: tuple = (
        "vintage",
        "modern",
        "pioneer",
        "pauper",
        "standard",
        "legacy",
    )
    allowed_sections: tuple = (
        "enchantments",
        "lands",
        "artifacts",
        "planeswalkers",
        "creatures",
        "companion",
        "spells",
        "creatures",
    )

    basic_lands: tuple = ("plains", "swamp", "mountain", "forest", "island")
    allowed_sets: tuple = ("core", "expansion", "draft_innovation", "commander")
    strategies: tuple = (
        "voltron",
        "sacrifice",
        "reanimator",
        "combo",
        "aggro",
        "ramp",
        "control",
        "stax",
        "tax",
        "tribal",
        "burn",
        "pod",
        "affinity",
        "tempo",
        "weenie",
        "storm",
        "cycling",
    )
    colors_map: Dict[str, str] = {
        "G": "Green",
        "R": "Red",
        "U": "Blue",
        "W": "White",
        "B": "Black",
        "BU": "Dimir",
        "UW": "Azorius",
        "BR": "Rakdos",
        "GR": "Gruul",
        "GW": "Selesnya",
        "BW": "Orzhov",
        "RU": "Izzet",
        "BG": "Golgari",
        "RW": "Boros",
        "GU": "Simic",
        "BUW": "Esper",
        "BUR": "Grixis",
        "BGR": "Jund",
        "RGW": "Naya",
        "GUW": "Bant",
        "BGW": "Abzan",
        "RUW": "Jeskai",
        "BGU": "Sultai",
        "BRW": "Mardu",
        "GRU": "Temur",
        "BRUW": "Yore-Tiller",
        "BGRU": "Glint-Eye",
        "BGRW": "Dune-Brood",
        "GRUW": "Ink-Treader",
        "BGUW": "Witch-Maw",
        "BGRUW": "5 color",
    }
