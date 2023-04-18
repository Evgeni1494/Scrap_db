import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from ..items import ScrapingImdbItem



class FilmsSpiderSpider(CrawlSpider):
    
    custom_settings = {
    "ITEM_PIPELINES": {"scraping_imdb.pipelines.ScrapingFilmsPipeline": 300}
    }

    name = "films_spider"
    allowed_domains = ["www.imdb.com"]
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    rules = (Rule(LinkExtractor(restrict_css=".titleColumn a"), callback="parse_item", follow=False),)
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })


    def parse_item(self, response):
        items = ScrapingImdbItem()
        items['titre'] = response.css('.sc-afe43def-1::text').get()
        items['titre_original'] = response.css('.sc-afe43def-3::text').get()
        items['score'] = response.css('.sc-bde20123-1::text').get()
        items['genre'] = response.css('a span.ipc-chip__text::text').extract()
        items['annee'] = response.css('.sc-afe43def-4 li:nth-of-type(1) a::text').get()
        items['duree'] = response.css('.sc-afe43def-4 li:nth-of-type(3)::text').get()
        items['description'] = response.css('.sc-5f699a2-2::text').get()
        items['acteurs_principaux'] = response.css('.sc-52d569c6-3 .ipc-metadata-list-item--link a.ipc-metadata-list-item__list-content-item::text').extract()
        items['public'] = response.css('.sc-afe43def-4 li:nth-of-type(2) a::text').get()
        items['pays'] = response.css("[data-testid='title-details-origin'] a::text").get()
        
        
        if items['titre_original']:
            items['titre_original'] = items['titre_original'].split(":")[-1].strip()
        
        if items['duree']:
            match = re.match(r'^(\d+)h\s*(\d+)m$', items['duree'].strip())
            if match:
                heures, minutes = match.groups()
                heures = int(heures)
                minutes = int(minutes)
                if heures >= 0 and minutes >= 0:
                    items['duree'] = heures*60 + minutes
                else:
                    items['duree'] = None
            else:
                items['duree'] = None
        
    
        return items
    
    
