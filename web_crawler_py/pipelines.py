# -*- coding: utf-8 -*-
import json
import pymongo
import boto3


class WebCrawlerPyPipeline(object):
    collection_name = 'news'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.dynamo = boto3.resource('dynamodb')
        self.table = self.dynamo.Table('news')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Insert On MongoDB
        self.db[self.collection_name].insert(dict(item))

        # Insert on DynamoDB
        self.table.put_item(
            Item=dict(item)
        )
        return item
