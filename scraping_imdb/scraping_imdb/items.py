# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Modèle de film
class ScrapingImdbItem(scrapy.Item):
        titre = scrapy.Field()
        titre_original = scrapy.Field()
        score = scrapy.Field()
        genre = scrapy.Field()
        annee = scrapy.Field()
        duree = scrapy.Field()
        description = scrapy.Field()
        acteurs_principaux = scrapy.Field()
        public = scrapy.Field()
        pays = scrapy.Field()
        image_url = scrapy.Field()
        cout = scrapy.Field()
