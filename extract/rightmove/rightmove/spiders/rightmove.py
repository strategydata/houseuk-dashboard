import logging
import scrapy
from rightmove.items import RightmoveItem
from rightmove.misc.url_utils import update_param

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RightmoveSpider(scrapy.SitemapSpider):
    name = "rightmove"
    sitemap_urls = ["https://www.rightmove.co.uk/sitemap.xml"]
    sitemap_rules = [
        (r"\/property-for-sale\/([a-zA-Z]+\d+)+\.html", "parse_for_sale"),
        (r"\/property-to-rent\/([a-zA-Z]+\d+)+\.html", "parse_to_rent"),
    ]
    index_number = 0
    # increment = 24  # Number of items to increment for pagination

    def parse_for_sale(self, response):
        # Extract the outcode from the URL
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "www.rightmove.co.uk",
        }

        homes = response.css('[class^="PropertyCard_propertyCardContainer_"]')
        if not homes:
            logger.debug(f"Ignoring no items response for URL: {response.url}")
            return
        for home in homes:
            items = RightmoveItem()
            items["url"] = (
                "https://www.rightmove.co.uk"
                + home.css("a.propertyCard-link::attr(href)").get()
            )
            items["price"] = int(
                home.css('[class^="PropertyPrice_price_"]::text').get()
            )
            items["title"] = home.xpath("//address/text()").get()
            items["date_added"] = home.css(
                '[class^="MarketedBy_joinedText_"]::text'
            ).get()
            items["property_type"] = home.css(
                '[class^="PropertyInformation_propertyType_"]::text'
            ).get()
            items["bedrooms"] = home.css(
                '[class^="PropertyInformation_bedroomsCount_"]::text'
            ).get()
            items["bathooms"] = home.css(
                '[class^="PropertyInformation_bathContainer_"] span::text'
            ).get()
            items["phone"] = home.css(
                '[class^="CallAgent_test_"] > a:nth-child(2) > span:nth-child(1)::text'
            ).get()
            items["address"] = home.css(
                '[class^="PropertyAddress_address_"]::text'
            ).get()
            items["summary"] = home.css(
                '[class^="PropertyCardSummary_summary_"]::text'
            ).get()
            items["email"] = home.css('[class^="Contact_emailLink_"]::attr(href)').get()
            items["catalog_url"] = response.url
            yield items
        total = int(
            response.css('[class^="ResultsCount_resultsCount_"] p span::text').get()
        )
        logger.debug(f"Total properties found: {total}")
        self.index_number=self.index_number+24
        next_page = update_param(response.url, "index",self.index_number )
        
        # next_page = f"{response.url}?index={self.index_number}"
        logger.debug(f"Next page URL: {next_page}")
        logger.debug(f"Next self.index_number: {self.index_number}")
        yield scrapy.Request(
            method="GET",
            url=next_page,
            headers=headers,
            callback=self.parse_for_sale,
        )

    def parse_to_rent(self, response):
        # Extract the outcode from the URL
        pass
