# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from tangshi.items import TangshiItem,PoemZuopin

class TangshiPipeline(object):
    def __init__(self):
        self.MYSQL_CONFIG = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '密码',
            'db': 'local_db',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**self.MYSQL_CONFIG)

    def process_item(self, item, spider):
        if isinstance(item,TangshiItem):
            poemers = ['chaodai', 'poemer', 'zuopins_total', 'poemer_url']
            poemers_base_sql = 'insert into poemers ({}) values(%s,%s,%s,%s)'
            poemers_sql = poemers_base_sql.format(','.join(poemers))
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(poemers_sql,(item['chaodai'], item['poemer'], item['zuopins_total'], item['poemer_url']))
            conn.commit()

        elif isinstance(item, PoemZuopin):
            zuopins = ['poemer', 'poemer_url', 'zuopin_name', 'name_words', 'zuopin_content', 'zuopin_words',
                       'zuopin_url']
            zuopin_base_sql = 'insert into poem_zuopin ({}) values(%s,%s,%s,%s,%s,%s,%s)'
            zuopin_sql = zuopin_base_sql.format(','.join(zuopins))
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(zuopin_sql,(item['poemer'], item['poemer_url'], item['zuopin_name'], item['name_words'],item['zuopin_content'], item['zuopin_words'], item['zuopin_url']))
            conn.commit()





