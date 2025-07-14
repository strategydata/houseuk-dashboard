import pytest
from rightmove.rightmove.misc.url_utils import update_param


@pytest.mark.parametrize(
    "url, param_name, new_value, expected",
    [
        (
            "https://www.rightmove.co.uk/property-for-sale/BH2.html?index=24",
            "index",
            "123",
            "https://www.rightmove.co.uk/property-for-sale/BH2.html?index=123",
        )
    ],
)
def test_update_param(url, param_name, new_value, expected):
    result = update_param(url, param_name, new_value)
    assert result == expected
