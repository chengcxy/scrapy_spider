#coding:utf-8

import os
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from ygmoive.items import YgmoiveItem,Ygmoive_pages_Item,Ygmoive_info_Item

class YgdySpider(CrawlSpider):
    name = 'ygdy'
    start_urls = ['http://www.ygdy8.com']
    allowed_domains = ['ygdy8.com']
    root_url='http://www.ygdy8.com'
    signs=['/', '\\', ':', '*', '"', '<', '>', '|', '？','?',"'",' ']

    def parse(self, response):
        selector = Selector(response)
        menus = selector.xpath('//div[@id="menu"]/div[@class="contain"]/ul/li[position()<9]/a')
        items=[]
        for menu in menus:
            menu_name = menu.xpath('text()').extract_first()
            menu_url = self.root_url + menu.xpath('@href').extract_first()
            print(menu_name,menu_url)
            if  menu_url.endswith('gndy/index.html'):
                continue
            else:
                item=YgmoiveItem()
                item['menu_name']=menu_name
                item['menu_url'] = menu_url
                items.append(item)
        for item in items:
            yield item
            yield Request(url=item['menu_url'],meta={'item1':item},callback=self.parse_menu)
    def parse_menu(self,response):
        print(response.url)
        item1=response.meta['item1']
        selector=Selector(response)
        menu_pages=selector.xpath('//div[@class="x"]//text()')[1].extract().split('/')[0].replace('共','').replace('页','')
        print(menu_pages)
        menu_id=selector.xpath('//div[@class="x"]//a/@href').extract_first().replace('2.html','')
        print(menu_id)
        page_url = response.url.replace('index',menu_id)
        print('page_url: ',page_url)
        item2 = Ygmoive_pages_Item()
        item2['menu_name'] = item1['menu_name']
        item2['menu_url'] = item1['menu_url']
        item2['menu_id'] = menu_id
        item2['menu_pages'] = menu_pages
        yield item2
        for page in range(1,int(menu_pages)+1):
            req_url = page_url.replace('.html','') + str(page) + '.html'
            print(req_url)
            yield Request(url=req_url,meta={'item3':item2},callback=self.parse_page)

    def parse_page(self,response):
        item3 = response.meta['item3']
        selector = Selector(response)
        menu_name = item3['menu_name']
        moive_urls = selector.xpath('//a[@class="ulink"]/@href').extract()
        for short_moive_url in moive_urls:
            moive_url = self.root_url + short_moive_url
            print(moive_url)
            yield Request(url=moive_url,meta={'menu_name':menu_name},callback=self.parse_detail)


    def parse_detail(self,response):
        menu_name = response.meta['menu_name']
        selector = Selector(response)
        moivename = selector.xpath('//h1/font/text()').extract_first().split('《')[1].split('》')[0]
        for sign in self.signs:
            if sign in moivename:
                moive_name=moivename.replace(sign,'-')
            else:
                moive_name=moivename
        moive_url = response.url
        sources = selector.xpath('//td[@style="WORD-WRAP: break-word"]/a/@href').extract()
        for source in sources:
            if source:
                item4 = Ygmoive_info_Item()
                item4['menu_name']=menu_name
                item4['moive_name']=moive_name
                item4['moive_url']=moive_url
                item4['source']=source
                print(item4)
                yield item4
            else:
                continue





