import scrapy
from scrapy.spiders import SitemapSpider
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RightmoveSpider(SitemapSpider):
    name = 'rightmove'
    sitemap_urls = [
        'https://www.rightmove.co.uk/sitemap.xml'
    ]
    sitemap_rules = [
        (r'/property-for-sale/([a-zA-Z]+\d+)+\.html', 'parse_for_sale'),
        (r'/property-to-rent/([a-zA-Z]+\d+)+\.html', 'parse_to_rent'),
    ]

    def parse_for_sale(self, response):
        pass

    def parse_to_rent(self, response):
        pass
