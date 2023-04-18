import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SeriesSpiderSpider(CrawlSpider):
    name = "series_spider"
    allowed_domains = ["www.imdb.com"]
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    rules = (Rule(LinkExtractor(restrict_css=".titleColumn a"), callback="parse_item", follow=False),)
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250', headers={
            'User-Agent': self.user_agent
        })

    def parse_item(self, response):
        titre = response.css('.sc-afe43def-1::text').get()
        
        yield {
            "titre" :titre
        }
