# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import os
from dotenv import load_dotenv


class ScrapingFilmsPipeline(object):

    collection_name = 'films'

    def __init__(self, mongo_uri, mongo_db):
        
        load_dotenv()
        ATLAS_KEY = os.getenv("ATLAS_KEY")
        self.conn = pymongo.MongoClient(ATLAS_KEY)
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        db = self.conn['IMDBscrap']
        self.collection = db['films']
        
        
    @classmethod
    def from_crawler(cls, crawler):
        
        load_dotenv()
        ATLAS_KEY = os.getenv("ATLAS_KEY")
    
        return cls(
            mongo_uri=ATLAS_KEY,
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


class ScrapingSeriesPipeline(object):

    collection_name = 'series'

    def __init__(self, mongo_uri, mongo_db):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        
        db = self.conn['IMDBscrap']
        self.collection = db['series']
        
    @classmethod
    def from_crawler(cls, crawler):
        
        load_dotenv()
        ATLAS_KEY = os.getenv("ATLAS_KEY")
    
        return cls(
            mongo_uri=ATLAS_KEY,
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


