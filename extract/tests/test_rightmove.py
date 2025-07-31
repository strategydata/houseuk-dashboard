import pytest
import logging
import os
from scrapy.http import HtmlResponse

from extract.rightmove.rightmove.spiders.rightmove import RightmoveSpider

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
        == "https://www.rightmove.co.uk/properties/156123512#/?channel=RES_BUY"
    )
    assert item["price"] == "£650000"
    assert item["address"] == "Portobello Square, 334 Portobello Road, W10"
    assert item["bathrooms"] == "1"
    assert item["bedrooms"] == "1"
    assert (
        item["catalog_url"] == "https://www.rightmove.co.uk/property-for-sale/W10.html"
    )
    assert item["let_or_sales"] == "rent"
    assert item["phone"] == "02038347939"
    assert item["property_type"] == "Apartment"
    assert (
        item["summary"]
        == """Book your viewing! Portobello Square is an impressive collection of apartments located in Ladbroke Grove, on the doorstep of the vibrant Portobello Road. Ready to move in early 2025."""
    )
