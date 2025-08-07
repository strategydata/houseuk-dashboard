import logging
import scrapy
import scrapy.spiders
from urllib.parse import urlparse, parse_qs
from house.extract.rightmove.rightmove.itemsloaders import (
    RightmoveItemLoader,
)
from house.extract.rightmove.rightmove.items import RightmoveItem
from house.extract.rightmove.rightmove.misc.url_utils import update_param

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RightmoveSpider(scrapy.spiders.SitemapSpider):
    """
    rightmove
    """

    name = "rightmove"
    sitemap_urls = ["https://www.rightmove.co.uk/sitemap.xml"]
    sitemap_rules = [
        (r"\/property-for-sale\/([a-zA-Z]+\d+)+\.html", "parse"),
        (r"\/property-to-rent\/([a-zA-Z]+\d+)+\.html", "parse"),
    ]

    # increment = 24  # Number of items to increment for pagination
    def parse(self, response):
        # Extract the outcode from the URL
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "www.rightmove.co.uk",
        }
        let_or_sales = "sales" if "property-to-rent" in response.url else "rent"
        homes = response.css('[class^="PropertyCard_propertyCardContainer_"]')
        if not homes:
            logger.debug(f"Ignoring no items response for URL: {response.url}")
            return
        for home in homes:
            loader = RightmoveItemLoader(item=RightmoveItem(), selector=home)
            loader.add_css("url", "a.propertyCard-link::attr(href)")
            loader.add_css("price", '[class^="PropertyPrice_price_"]::text')
            loader.add_xpath("title", ".//address/text()")
            loader.add_css("date_added", '[class^="MarketedBy_joinedText_"]::text')
            loader.add_css(
                "property_type", '[class^="PropertyInformation_propertyType_"]::text'
            )
            loader.add_css(
                "bedrooms", '[class^="PropertyInformation_bedroomsCount_"]::text'
            )
            loader.add_css(
                "bathrooms", '[class^="PropertyInformation_bathContainer_"] span::text'
            )
            loader.add_css(
                "phone",
                '[class^="CallAgent_test_"] > a:nth-child(2) > span:nth-child(1)::text',
            )
            loader.add_css("address", '[class^="PropertyAddress_address_"]::text')
            loader.add_css("summary", '[class^="PropertyCardSummary_summary_"]::text')
            loader.add_css("email", '[class^="Contact_emailLink_"]::attr(href)')
            loader.add_value("catalog_url", response.url)
            loader.add_value("let_or_sales", let_or_sales)
            yield loader.load_item()
        total = int(
            response.css('[class^="ResultsCount_resultsCount_"] p span::text')
            .get()
            .replace(",", "")
        )
        logger.debug(f"Total properties found: {total}")
        current_index = (
            int(parse_qs(urlparse(response.url).query).get("index", [None])[0]) + 24
            if "index" in response.url
            else 24
        )
        next_page = update_param(response.url, "index", current_index)
        logger.debug(f"Next page URL: {next_page}")
        yield scrapy.Request(
            method="GET",
            url=next_page,
            headers=headers,
            callback=self.parse,
        )
