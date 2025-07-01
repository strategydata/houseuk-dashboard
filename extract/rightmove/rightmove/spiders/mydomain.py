import scrapy
from scrapy.spiders import SitemapSpider
import logging

from rightmove.items import RightmoveItem

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MydomainSpider(SitemapSpider):
    name = "mydomain"
    sitemap_urls = [
        'https://www.rightmove.co.uk/sitemap.xml'
    ]
    sitemap_rules = [
        (r"\/property-for-sale\/([a-zA-Z]+\d+)+\.html", 'parse_for_sale'),
        (r"\/property-to-rent\/([a-zA-Z]+\d+)+\.html", 'parse_to_rent'),
    ]
    index_number = 0
    increment = 24  # Number of items to increment for pagination
    def parse_for_sale(self, response):
        # Extract the outcode from the URL
        headers={
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'www.rightmove.co.uk',
        }
        
        homes = response.css("[class^=\"PropertyCard_propertyCardContainer_\"]")
        for home in homes:
            items = RightmoveItem()
            items["url"]=f"https://www.rightmove.co.uk"+home.css("a.propertyCard-link::attr(href)").get()
            items["price"] = home.css("[class^=\"PropertyPrice_price_\"]::text").get()
            items["title"]=home.xpath("//address/text()").get()
            items["date_added"]=home.css("[class^=\"MarketedBy_joinedText_\"]::text").get()
            items["property_type"] = home.css("[class^=\"PropertyInformation_propertyType_\"]::text").get()
            items["bedrooms"] = home.css("[class^=\"PropertyInformation_bedroomsCount_\"]::text").get()
            items["bathooms"] = home.css("[class^=\"PropertyInformation_bathContainer_\"] span::text").get()
            items["phone"] = home.css("[class^=\"CallAgent_test_\"] > a:nth-child(2) > span:nth-child(1)::text").get()
            items["address"]= home.css("[class^=\"PropertyAddress_address_\"]::text").get()
            items["summary"]= home.css("[class^=\"PropertyCardSummary_summary_\"]::text").get()
            items["email"]= home.css("[class^=\"Contact_emailLink_\"]::attr(href)").get()
            yield items
        next_page = f"{response.url}?index={self.index_number}"
        logger.debug(f"Next page URL: {next_page}")
        if self.index_number < 1100:
            self.index_number += self.increment
            yield scrapy.Request(
                method='GET',
                url=next_page,
                headers=headers,
                callback=self.parse
            )
    
    def parse_to_rent(self, response):
        # Extract the outcode from the URL
        pass