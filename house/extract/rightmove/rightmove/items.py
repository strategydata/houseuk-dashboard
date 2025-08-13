# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Identity, MapCompose
import re


def extract_id(url):
    """Extracts the ID from a URL."""
    match = re.search(r"/properties/(\d+)", url)
    return match[1] if match else None


class RightmoveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field(input_processor=MapCompose(extract_id))
    accessibility = scrapy.Field(output_processor=TakeFirst())
    bathrooms = scrapy.Field(output_processor=TakeFirst())
    bedrooms = scrapy.Field(output_processor=TakeFirst())
    council_tax = scrapy.Field(output_processor=TakeFirst())
    date_added = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    email = scrapy.Field(output_processor=TakeFirst())
    feature = scrapy.Field(output_processor=TakeFirst())
    garden = scrapy.Field(output_processor=TakeFirst())
    image_urls = scrapy.Field(output_processor=Identity())
    let_or_sales = scrapy.Field(output_processor=TakeFirst())
    latitude = scrapy.Field(output_processor=TakeFirst())
    longitude = scrapy.Field(output_processor=TakeFirst())
    parking = scrapy.Field(output_processor=TakeFirst())
    phone = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    property_type = scrapy.Field(output_processor=TakeFirst())
    size = scrapy.Field(output_processor=TakeFirst())
    tenure = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
