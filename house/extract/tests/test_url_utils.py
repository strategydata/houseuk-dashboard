import pytest
from house.extract.rightmove.rightmove.misc.url_utils import update_param


@pytest.mark.parametrize(
    "url, param_name, increment, expected",
    [
        (
            "https://www.rightmove.co.uk/property-for-sale/BH2.html?index=24",
            "index",
            "24",
            "https://www.rightmove.co.uk/property-for-sale/BH2.html?index=48",
        ),
        (
            "https://www.rightmove.co.uk/property-for-sale/BH2.html",
            "index",
            "24",
            "https://www.rightmove.co.uk/property-for-sale/BH2.html?index=24",
        ),
    ],
)
def test_update_param(url, param_name, increment, expected):
    """The function `test_update_param` tests the `update_param` function by comparing its result with an
    expected value.

    Parameters
    ----------
    url
        It seems like you were about to provide the value for the `url` parameter in the
    `test_update_param` function. Please go ahead and provide the URL so that we can continue with the
    function testing.
    param_name
        It seems like you were about to provide more information about the `param_name` parameter in the
    `test_update_param` function. Could you please provide the complete information so that I can assist
    you further?
    new_value
        It seems like you were about to provide the value for the `new_value` parameter in the
    `test_update_param` function. Could you please provide the value that you would like to use for the
    `new_value` parameter in the test case?
    expected
        The `expected` parameter in the `test_update_param` function is the expected result that the
    `update_param` function should return when called with the specified `url`, `param_name`, and
    `new_value` parameters. The test will pass if the result returned by the `update_param` function

    """
    result = update_param(url, param_name, increment)
    assert result == expected
