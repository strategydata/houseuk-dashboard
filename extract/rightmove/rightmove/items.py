# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RightmoveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    tenure = scrapy.Field()
    address = scrapy.Field()
    size = scrapy.Field()
    bedrooms = scrapy.Field()
    bathooms = scrapy.Field()
    property_type = scrapy.Field()
    council_tax_band = scrapy.Field()
    energy_performance_certificate = scrapy.Field()
    listing_type = scrapy.Field()
    image_urls = scrapy.Field()
    date_added = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    catalog_url = scrapy.Field()
