# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item,Field


class YgmoiveItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    menu_name=Field()
    menu_url=Field()


class Ygmoive_pages_Item(Item):
    menu_name = Field()
    menu_url = Field()
    menu_id=Field()
    menu_pages=Field()

class Ygmoive_info_Item(Item):
    menu_name= Field()
    moive_name = Field()
    moive_url=Field()
    source=Field()





