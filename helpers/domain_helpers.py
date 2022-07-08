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
