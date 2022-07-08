import pytest
from utils import clean


@pytest.mark.parametrize(
    "str_to_clean,expected",
    [
        ("Creatures(15)", "creatures"),
        ("creatures", "creatures"),
        ("Lands(24)+4 MDFCs", "lands"),
    ],
)
def test_clean_string(str_to_clean: str, expected: str):
    assert clean.clean_str(str_to_clean) == expected


@pytest.mark.parametrize(
    "dict_to_clean,expected",
    [
        (
            {
                "name": "Castle Ardenvale",
                "cuantity": "\n1\n",
                "rarity": "\n1\xa0Rare\n",
                "mana_cost": 0,
            },
            {
                "name": "Castle Ardenvale",
                "cuantity": "1",
                "rarity": "1Rare",
                "mana_cost": 0,
            },
        ),
    ],
)
def test_clean_dict(dict_to_clean: dict, expected: dict):
    assert clean.clean_dict(dict_to_clean) == expected
