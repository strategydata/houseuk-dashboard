# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import boto3
import json
import hashlib
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class RightmovePipeline:
    def process_item(self, item, spider):
        return item


class UploadToS3Pipeline:
    def __init__(self, bucket):
        self.bucket = bucket

    @classmethod
    def from_crawler(cls, crawler):
        return cls(bucket=crawler.settings.get("AWS_S3_BUCKET"))

    def process_item(self, item, spider):
        s3_client = boto3.client("s3")
        item_bytes = json.dumps(ItemAdapter(item).asdict())
        item_key = hashlib.md5(item_bytes.encode()).hexdigest()
        s3_client.put_object(
            Body=item_bytes, Bucket=self.bucket, Key=item_key + ".json"
        )
        return item


class RemoveDuplicatesPipeline:
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        item_id = item.get("id")
        if adapter["id"] in self.seen:
            raise DropItem(f"Duplicate item found: {item_id}")
        else:
            self.seen.add(adapter["id"])
            return item
