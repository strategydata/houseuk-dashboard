import pytest
import logging
import os
from scrapy.http import HtmlResponse

from house.extract.rightmove.rightmove.spiders.rightmove import (
    RightmoveSpider,
)

logger = logging.getLogger(__name__)


@pytest.fixture
def html_file():
    filepath = os.path.join(
        os.path.dirname(__file__),
        "template",
        "Properties For Sale in W10 _ Rightmove.html",
    )
    with open(filepath, encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="session")
def spider():
    return RightmoveSpider()


@pytest.fixture
def response(html_file):
    return HtmlResponse(
        url="https://www.rightmove.co.uk/property-for-sale/W10.html",
        body=html_file,
        encoding="utf-8",
    )


def test_parse(spider, response):
    results = spider.parse(response)
    item = next(results)
    assert (
        item["url"]
        == "/properties/150832055#/?channel=RES_BUY"
    )
    assert item["price"] == "£950000"
    assert item["address"] == "Snarsgate Street, London, W10"
    assert item["bathrooms"] == "1"
    assert item["bedrooms"] == "3"
    assert (
        item["catalog_url"] == "https://www.rightmove.co.uk/property-for-sale/W10.html"
    )
    assert item["let_or_sales"] == "rent"
    assert item["phone"] == "02038348331"
    assert item["property_type"] == "Terraced"
    assert (
        item["summary"]
        == """A delightful three bedroom period cottage on a secluded street in the Royal Borough of Kensington & Chelsea."""
    )
