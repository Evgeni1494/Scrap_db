# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Imports nécessaires à l'exécution du projet
import pymongo
import os
from dotenv import load_dotenv


# Pipeline pour l'extraction des données sur les films
class ScrapingFilmsPipeline(object):

    collection_name = 'films'

    def __init__(self, mongo_uri:str, mongo_db:str) -> None:
        """
        Initialise la connexion à la base de données MongoDB
        
        Params : 
        mongo_uri : l'URI de connexion à la base de données MongoDB
        mongo_db : le nom de la base de données MongoDB à utiliser
        """
        
        load_dotenv()
        ATLAS_KEY = os.getenv("ATLAS_KEY")
        self.conn = pymongo.MongoClient(ATLAS_KEY)
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        db = self.conn['IMDBscrap']
        self.collection = db['films']
        
        
    @classmethod
    def from_crawler(cls, crawler):
        """Récupère les paramètres de configuration de la base de données

        Args:
            crawler: l'instance de crawler

        Returns:
            l'instance de pipeline
        """
        
        load_dotenv()
        ATLAS_KEY = os.getenv("ATLAS_KEY")
    
        return cls(
            mongo_uri=ATLAS_KEY,
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider) -> None :
        """
        Initialise la connexion à la base de données lors de l'ouverture du spider

        Args:
            spider : l'instance du spider
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider)-> None:
        """
        Ferme la connexion à la base de données lors de la fermeture du spider

        Args:
            spider : l'instance de spider
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        Enregistre l'élément dans la base de données MongoDB.

        Args:
            item : élément récupéré par le spider
            spider : l'instance du spider

        Returns:
            l'élément récupéré
        """
        self.db[self.collection_name].insert_one(dict(item))
        return item

# Pipeline pour l'extraction des données sur les séries
class ScrapingSeriesPipeline(object):

    collection_name = 'series'

    def __init__(self, mongo_uri:str, mongo_db:str) -> None :
        """
        Initialise la connexion à la base de données MongoDB
        
        Params : 
        mongo_uri : l'URI de connexion à la base de données MongoDB
        mongo_db : le nom de la base de données MongoDB à utiliser
        """
        load_dotenv()
        ATLAS_KEY = os.getenv("ATLAS_KEY")
        self.conn = pymongo.MongoClient(ATLAS_KEY)
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        
        db = self.conn['IMDBscrap']
        self.collection = db['series']
        
    @classmethod
    def from_crawler(cls, crawler):
        """Récupère les paramètres de configuration de la base de données

        Args:
            crawler: l'instance de crawler

        Returns:
            l'instance de pipeline
        """
        
        load_dotenv()
        ATLAS_KEY = os.getenv("ATLAS_KEY")
    
        return cls(
            mongo_uri=ATLAS_KEY,
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider) -> None :
        """
        Initialise la connexion à la base de données lors de l'ouverture du spider

        Args:
            spider : l'instance du spider
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider) -> None :
        """
        Ferme la connexion à la base de données lors de la fermeture du spider

        Args:
            spider : l'instance de spider
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        Enregistre l'élément dans la base de données MongoDB.

        Args:
            item : élément récupéré par le spider
            spider : l'instance du spider

        Returns:
            l'élément récupéré
        """
        self.db[self.collection_name].insert_one(dict(item))
        return item


