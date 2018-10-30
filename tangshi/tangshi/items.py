# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class TangshiItem(Item):
    chaodai = Field()
    poemer = Field()
    zuopins_total = Field()
    poemer_url = Field()


class PoemZuopin(Item):
    poemer = Field()
    poemer_url = Field()
    zuopin_name = Field()
    name_words = Field()
    zuopin_content = Field()
    zuopin_words = Field()
    zuopin_url = Field()
