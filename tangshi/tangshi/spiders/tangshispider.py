#coding:utf8
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from tangshi.items import TangshiItem,PoemZuopin

class TangShiSpider(CrawlSpider):
    name = 'tangshispider'
    start_urls = ['http://www.shicimingju.com/category/tangdaishiren/page/1']
    base_url = 'http://www.shicimingju.com/category/tangdaishiren/page/{}'
    allowed_domains = ['www.shicimingju.com']

    def parse(self,response):
        total_page = response.xpath('//div[@class="yema"]/text()').extract_first().split('/')[1].replace('共', '').replace('页)', '')
        print(total_page)
        for i in range(1, int(total_page) + 1):
            poem_page_url = self.base_url.format(str(i))
            yield Request(url=poem_page_url,callback=self.parse_poem_page)

    def parse_poem_page(self, response):
        print('parse_poem_page函数解析--->%s' % response.url)
        poems = response.xpath('//div[@class="shirenlist"]//a')
        for poem in poems:
            poemer_item = TangshiItem()
            poemer_url = 'http://www.shicimingju.com' + poem.xpath('@href').extract_first()
            poemer = poem.xpath('text()').extract_first()
            poemer_item['poemer_url'] = poemer_url
            poemer_item['poemer'] = poemer
            yield Request(url=poemer_url,callback=self.parse_poem,meta={'item':poemer_item})

    def parse_poem(self,response):
            poemer_item = response.meta['item']
            # 得到诗人作品集的总作品数 构建分页
            zuopins_total = response.xpath('//div[@class="num"]/b/text()').extract_first()
            poemer_item['chaodai'] = '唐朝'
            poemer_item['zuopins_total'] = zuopins_total

            yield poemer_item
            # 根据 得到诗人作品集的总作品数   得到诗人作品集的每一页请求
            zuopin_page_base_url = poemer_item['poemer_url'].replace('.html', '') + '_{}.html'
            divmod_num = [i for i in divmod(int(zuopins_total), 40)]
            pages = divmod_num[0] if divmod_num[1] == 0 else divmod_num[0] + 1
            for page in range(1, int(pages) + 1):
                zuopin_page_url = zuopin_page_base_url.format(page)
                yield Request(url=zuopin_page_url,callback=self.parse_page_zuopin)

    def parse_page_zuopin(self, response):
        zuopin_pages = response.xpath('//div[@class="shicilist"]/ul/li[1]/a')
        poemer_url = 'http://www.shicimingju.com' + response.xpath('//div[@class="shicilist"]/ul/li[2]/a[2]/@href').extract_first()
        poemer = response.xpath('//div[@class="shicilist"]/ul/li[2]/a[2]/em/text()').extract_first()
        for zuopin_page in zuopin_pages:
            item2 = {}
            zuopin_url = 'http://www.shicimingju.com' + zuopin_page.xpath('@href').extract_first()
            zuopin_name = zuopin_page.xpath('text()').extract_first()
            print('作者:%s,作者url:%s,作品==>%s,作品url==>%s' % (poemer, poemer_url, zuopin_name, zuopin_url))
            item2['poemer_url'] = poemer_url
            item2['poemer'] = poemer
            item2['zuopin_url'] = zuopin_url
            item2['zuopin_name'] = zuopin_name
            yield Request(url=zuopin_url,callback=self.parse_zuopin_detail,meta={'item2':item2})
            # 解析作品详情页

    def parse_zuopin_detail(self, response):
        item=response.meta['item2']
        print('parse_zuopin_detail函数解析--->%s' % item['zuopin_url'])
        zuopin_item = PoemZuopin()
        zuopin_item['poemer'] = item['poemer']
        zuopin_item['poemer_url'] = item['poemer_url']
        zuopin_item['zuopin_name'] = item['zuopin_name']
        zuopin_item['name_words'] = len(item['zuopin_name'])
        zuopin_item['zuopin_url'] = item['zuopin_url']
        try:
            zuopin_content = response.xpath('//div[@class="shicineirong"]//text()').extract()
            zuopin_item['zuopin_content'] = ''.join([x.strip() for x in zuopin_content])
            zuopin_item['zuopin_words'] = len(zuopin_item['zuopin_content'].replace('，', '').replace('。', ''))
        except:
            zuopin_item['zuopin_content'] = '抓取失败无数据'
            zuopin_item['zuopin_words'] = 0
        print(zuopin_item)
        yield zuopin_item
