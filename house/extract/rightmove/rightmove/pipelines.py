# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymongo


class RightmovePipeline:
    def __init__(self):
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        self.collection = self.client["rightmove"]["properties"]

    def process_item(self, item, spider):
        query = {
            "_id": item["_id"],
            "price": item["price"],
        }
        if self.collection.find_one(query):
            # If the item already exists, update it
            spider.logger.info(f"Duplicate item found: {item} — skipping.")
        else:
            self.collection.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
