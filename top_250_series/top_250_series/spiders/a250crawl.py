import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class Series250(CrawlSpider):
    name = '250crawl'
    allowed_domains = ['imdb.com']
    # start_urls = ['https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250', headers={
            'User-Agent': self.user_agent
        })

    series_links = LinkExtractor(restrict_css='.titleColumn a')
    # le_next = LinkExtractor(restrict_css='.next > a')  # next_button
    # le_cats = LinkExtractor(restrict_css='.side_categories > ul > li > ul > li a')  # Categories

    rule_book_details = Rule(series_links, callback='parse_item', follow=False)
    # rule_next = Rule(le_next, follow=True)
    # rule_cats = Rule(le_cats, follow=True)

    rules = (
        rule_book_details,
        # rule_next,
        # rule_cats
    )    
    def parse_item(self, response):
        
        
        title = response.css('.sc-afe43def-1::text').get()
        original_title= response.css('.sc-afe43def-3::text').get()
        score = response.css('.sc-bde20123-1::text').get()
        genre = response.css('.ipc-chip__text::text').get()
        annee = response.css('.sc-afe43def-4 li:nth-of-type(2) a::text').get()
        duree = response.css(".ipc-inline-list--show-dividers li:nth-of-type(4)::text").get()
        description = response.css('span.sc-5f699a2-2::text').get()
        acteurs = response.css('a.sc-bfec09a1-1::text').extract()
        public = response.css('.sc-afe43def-4 li:nth-of-type(3) a::text').get()
        pays = response.css('[data-testid="title-details-origin"] a::text').get()
        
        
        if original_title:
                original_title = original_title.split(": ")[-1].strip()
        
           
        if duree:
            match = re.match(r'^(\d+)h\s(\d+)m$', duree.strip())
            if match:
                heures, minutes = match.groups()
                heures = int(heures)
                minutes = int(minutes)
                if heures >= 0 and minutes >= 0:
                    duree_minutes = heures*60 + minutes
                    duree = f"{duree_minutes}m"
                elif heures == 1:
                    duree_minutes = heures*60
                    duree = f"{duree_minutes}m"
            else:
                try:
                    duree_minutes = int(duree.strip())
                    if duree_minutes >= 0:
                        if duree_minutes == 60:
                            duree_minutes = 60
                            duree = f"{duree_minutes}m"
                        else:
                            duree = f"{duree_minutes}m"
                except ValueError:
                    pass
            
            # match = re.match(r'^(\d+)h\s(\d+)m$', duree.strip())
            # if match:
            #     heures, minutes = match.groups()
            #     heures = int(heures)
            #     minutes = int(minutes)
            #     if heures >= 0 and minutes >= 0:
            #         duree = heures*60 + minutes
            #     else:
            #         pass
            # else:
            #     pass
        
        
        
        yield {
            'Title': title,
            'Titre Originale': original_title,
            'Score': score,
            'Genre': genre,
            'Année': annee,
            'Durée': duree,
            'Description': description,
            'Acteurs': acteurs,
            'Public': public,
            'Pays': pays,
        }  
        