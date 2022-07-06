from dataclasses import dataclass


class Domain:
    allowed_formats: tuple = (
        "vintage",
        "modern",
        "pioneer",
        "pauper",
        "standard",
        "legacy",
    )
