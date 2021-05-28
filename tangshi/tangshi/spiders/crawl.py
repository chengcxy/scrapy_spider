
import copy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from tangshi.items import TangshiItem


class Spider(CrawlSpider):
    name = "crawler_tangshi"
    def start_requests(self):
        dynastys = {
            "先秦": "https://www.shi-ci.com/dynasty/72057594037927936", 
            "汉代": "https://www.shi-ci.com/dynasty/144115188075855872", 
            "三国两晋": "https://www.shi-ci.com/dynasty/216172782113783808", 
            "南北朝": "https://www.shi-ci.com/dynasty/288230376151711744", 
            "隋代": "https://www.shi-ci.com/dynasty/360287970189639680", 
            "唐代": "https://www.shi-ci.com/dynasty/432345564227567616",
            "宋代": "https://www.shi-ci.com/dynasty/504403158265495552", 
            "元代": "https://www.shi-ci.com/dynasty/576460752303423488", 
            "明代": "https://www.shi-ci.com/dynasty/648518346341351424",
            "清代": "https://www.shi-ci.com/dynasty/720575940379279360", 
            "近现代": "https://www.shi-ci.com/dynasty/792633534417207296",
        }
        for k,url in dynastys.items():
            yield Request(url,meta={"item":k},callback=self.parse_dynasty)
    
    def parse_dynasty(self,response):
        dynasty = response.meta["item"]
        nodes = response.xpath('//div[@class="poem-preview"]')
        for node in nodes:
            poet_name = node.xpath("a/text()").extract_first()
            poet_url =  "https://www.shi-ci.com" + node.xpath("a/@href").extract_first()
            item = {
                "dynasty":dynasty,
                "poet_name":poet_name,
                "poet_url":poet_url
            }
            yield Request(poet_url,meta={"item":item},callback=self.parse_poet)
    
    def parse_poet(self,response):
        item = response.meta["item"]
        nodes = response.xpath('//div[@class="poem-preview"]')
        for node in nodes:
            poem_name = node.xpath("a/text()").extract_first()
            poem_url = "https://www.shi-ci.com" + node.xpath("a/@href").extract_first()
            _item = copy.deepcopy(item)
            _item["poem_name"] = poem_name
            _item["poem_url"] = poem_url
            yield Request(poem_url,meta={"item":_item},callback=self.parse_poem)
    
    def parse_poem(self,response):
        _item = response.meta["item"]
        data = response.xpath('//div[@id="poem"]/div[1]/p/text()').extract()
        contents = "\n".join(data)
        poet_desc = response.xpath('//div[@class="uk-width-1-3"]/div[1]/p/text()').extract_first()
        item = TangshiItem()
        for k,v in _item.items():
            item[k] = v
        item["contents"] = contents
        item["poet_desc"] = poet_desc
        item["crawl_url"] = response.url
        yield item





           
			
				
			
			

            
   
