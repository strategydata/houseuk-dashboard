from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class RightmoveItemLoader(ItemLoader):
    @staticmethod
    def clean_comma(value):
        return value.replace(",", "")

    @staticmethod
    def clean_space(value):
        return value.replace(" ", "")

    default_output_processor = TakeFirst()
    url_in = MapCompose(str.strip)
    price_in = MapCompose(str.strip, clean_comma)
    address_in = MapCompose(str.strip)
    bathrooms_in = MapCompose(str.strip)
    bedrooms_in = MapCompose(str.strip)
    property_type_in = MapCompose(str.strip)
    summary_in = MapCompose(str.strip)
    phone_in = MapCompose(str.strip, clean_space)
    date_added_in = MapCompose(str.strip)
