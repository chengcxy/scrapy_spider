# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from ygmoive.items import YgmoiveItem,Ygmoive_pages_Item,Ygmoive_info_Item
import pymysql
import requests

class YgmoivePipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, YgmoiveItem):
            menu_name=item['menu_name']
            abs_dir = os.path.abspath(__file__)
            menu_dir = os.path.join(os.path.dirname(os.path.dirname(abs_dir)), menu_name)
            if os.path.isdir(menu_dir):
                pass
            else:
                os.mkdir(menu_dir)
            # menu_url=item['menu_url']
            # post_data={
            #     'menu_name':menu_name,
            #     'menu_url':menu_url
            # }
            # html=requests.post('http://10.10.1.193/moive/',data=post_data).text
            # print(html)

        elif isinstance(item, Ygmoive_pages_Item):
            menu_name=item['menu_name']
            abs_dir=os.path.abspath(__file__)
            menu_dir = os.path.join(os.path.dirname(os.path.dirname(abs_dir)), menu_name)
            if os.path.isdir(menu_dir):
                pass
            else:
                os.mkdir(menu_dir)
            file_name=os.path.join(menu_dir,menu_name + '.txt')

            with open(file_name,'w',encoding='utf-8') as file:
                file.write(menu_name + '-' + item['menu_url'] + '-' + item['menu_id'] + '-' + item['menu_pages'])


        elif isinstance(item, Ygmoive_info_Item):
            menu_name = item['menu_name']
            moive_name=item['moive_name']
            abs_dir = os.path.abspath(__file__)
            menu_dir = os.path.join(os.path.dirname(os.path.dirname(abs_dir)), menu_name)
            if os.path.isdir(menu_dir):
                pass
            else:
                os.mkdir(menu_dir)
            file_name = os.path.join(menu_dir, moive_name + '.txt')
            with open(file_name, 'a+', encoding='utf-8') as file:
                file.write(menu_name + '-' +  moive_name + '-' + item['moive_url'] + '-' + item['source'] + '\n')
        else:
            pass





