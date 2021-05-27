# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TangshiItem(scrapy.Item):
    dynasty = scrapy.Field()
    poet_name = scrapy.Field()
    poet_url = scrapy.Field()
    poem_name = scrapy.Field()
    poem_url = scrapy.Field()
    contents = scrapy.Field()
    poet_desc = scrapy.Field()
    crawl_url = scrapy.Field()
     
    
