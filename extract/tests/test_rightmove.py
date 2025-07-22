import pytest
import logging
import os
from scrapy.http import HtmlResponse

from extract.rightmove.rightmove.spiders.rightmove import RightmoveSpider

logger = logging.getLogger(__name__)

@pytest.fixture
def html_file():
    filepath = os.path.join(os.path.dirname(__file__), "template","Properties For Sale in W10 _ Rightmove.html")
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
        encoding="utf-8"
    )


def test_parse(spider,response):
    results = list(spider.parse(response))
    assert len(results) == 26
    item=results[0]
    assert item["url"] == "https://www.rightmove.co.uk/properties/163873952#/?channel=RES_BUY"
    assert item["price"] == "£625,000"
    assert item["address"] =="St. Charles Square, London,  W10, W10"
    assert item["bathrooms"] =="1"
    assert item["bedrooms"] =="2"
    assert item["catalog_url"] =="https://www.rightmove.co.uk/property-for-sale/W10.html"
    assert item["let_or_sales"]=="sales"
    assert item["phone"]=="020 3871 3433"
    assert item["property_type"]== "Flat"
    assert item["summary"] =="""A two bedroom flat with a reception room with a bay window. The property is located within 0.5 miles to Ladbroke Grove, Golborne Road, Portobello Road and all the other amenities of Notting Hill."""
    next_request=results[-1]
    assert "index=24" in next_request.url
    