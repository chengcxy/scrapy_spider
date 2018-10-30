# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class SoybaseItem(Item):
    #第一层url 名称
    first_url = Field()
    first_name = Field()

    #第二层url
    second_url =Field()

    #第三层url 数据
    QTL_url = Field()
    QTL_name = Field()
    #抓取时间
    create_time = Field()

    parent1 = Field()
    parent2 = Field()
    reference_title = Field()
    reference_magzine = Field()
    mark_url = Field()
    mark_3 = Field()
    mark_5 = Field()



