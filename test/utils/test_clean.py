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
