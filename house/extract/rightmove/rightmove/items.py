# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join


class RightmoveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    accessibility = scrapy.Field(output_processor=Join())
    bathrooms = scrapy.Field(output_processor=Join())
    bedrooms = scrapy.Field(output_processor=Join())
    council_tax = scrapy.Field(output_processor=Join())
    date_added = scrapy.Field(output_processor=Join())
    description = scrapy.Field(output_processor=Join())
    email = scrapy.Field(output_processor=Join())
    feature = scrapy.Field(output_processor=Join())
    garden = scrapy.Field(output_processor=Join())
    image_urls = scrapy.Field(output_processor=Join())
    let_or_sales = scrapy.Field(output_processor=Join())
    latitude = scrapy.Field(output_processor=Join())
    longitude = scrapy.Field(output_processor=Join())
    parking = scrapy.Field(output_processor=Join())
    phone = scrapy.Field(output_processor=Join())
    price = scrapy.Field(output_processor=Join())
    property_type = scrapy.Field(output_processor=Join())
    size = scrapy.Field(output_processor=Join())
    tenure = scrapy.Field(output_processor=Join())
    title = scrapy.Field(output_processor=Join())
    url = scrapy.Field(output_processor=Join())
