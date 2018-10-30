
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from soybase.items import SoybaseItem
from datetime import datetime


class SoybaseSpider(CrawlSpider):
    name = 'soybase'
    allowed_domains = ['www.soybase.org']
    start_urls = ['http://www.soybase.org/search/qtllist_by_symbol.php/']
    base_url = 'https://www.soybase.org'

    def parse(self,response):
        items = []
        infos = response.xpath('//td/a')
        for info in infos:
            item = {}
            item['first_url'] = self.base_url + info.xpath('@href').extract_first()
            item['first_name'] = info.xpath('text()').extract_first()
            yield Request(url=item['first_url'],callback=self.second_site,meta={'item':item})

    def second_site(self,response):
        url = response.xpath('//table[@id="beantable"]/tr[2]/th[3]/a/@href').extract_first()
        item = response.meta['item']
        item2 = {}
        second_url = self.base_url + response.xpath('//table[@id="beantable"]/tr[2]/th[3]/a/@href').extract_first()
        item2['first_url'] = item['first_url']
        item2['first_name'] = item['first_name']
        item2['second_url'] = second_url
        yield Request(url=second_url,callback=self.third_site,meta={'item2':item2})

    def third_site(self,response):
        item2 = response.meta['item2']
        tr_infos = response.xpath('//tr[position()>1]')
        for tr in tr_infos:
            item3 = {}
            item3['first_url'] = item2['first_url']
            item3['first_name'] = item2['first_name']
            item3['second_url'] = item2['second_url']
            QTL_url = tr.xpath('td[1]/a/@href').extract_first()
            if QTL_url:
                item3['QTL_url'] = self.base_url + QTL_url
                item3['QTL_name'] = tr.xpath('td[1]/a/text()').extract_first()
                item3['create_time'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
                yield Request(url=item3['QTL_url'], callback=self.fourth_site, meta={'item3': item3})
            else:
                pass
    def fourth_site(self,response):
        item3 = response.meta['item3']
        item4={}
        item4.update(item3)
        item4['parent1'] = response.xpath('//table[1]//tr[1]/td[2]/text()').extract_first()
        item4['parent2'] = response.xpath('//table[1]//tr[2]/td[2]/text()').extract_first()
        refers = response.xpath('//table[4]//tr[1]/td[2]/a/text()').extract()
        item4['reference_title'] = refers[0] if refers else None
        item4['reference_magzine'] = refers[1] if len(refers)>1 else None
        item4['mark_url'] = response.xpath('//table[5]//tr[2]/td[5]/a/@href').extract_first()
        if not item4['mark_url']:
            item4['mark_url'] = response.xpath('//table[4]//tr[2]/td[5]/a/@href').extract_first()
        if item4['mark_url'] and item4['mark_url'].startswith('/SeqMapSearch'):
            item4['mark_url'] = self.base_url + item4['mark_url']
            yield Request(url=item4['mark_url'], callback=self.fifth_site, meta={'item4': item4})
        else:
            item4['mark_url'] = None
            item4['mark_3'] = None
            item4['mark_5'] = None
            yield item4

    def fifth_site(self,response):
        item4 = response.meta['item4']
        item5 = SoybaseItem()
        item5.update(item4)

        marks = response.xpath('//div[@class="sb_middle"]/div[@class="sb_main"]/text()').extract()
        if marks:
            mark_1 = [x.split(':')[1].strip() for x in marks if x.startswith('\xa0\xa0\xa0\xa0\xa0name')]
            if mark_1:
                if len(mark_1)>=2:
                    item5['mark_3'] = mark_1[0]
                    item5['mark_5'] = mark_1[1]
                else:
                    item5['mark_3'] = mark_1[0]
                    item5['mark_5'] = None
            else:
                item5['mark_3'] = None
                item5['mark_5'] = None

        else:
            item5['mark_3'] = None
            item5['mark_5'] = None
        yield item5
