
import random
import json
import urllib.parse as parse
import requests

FIELDS = ['id', 'managerName', 'artificialPersonName', 'registerNo', 'establishDate', 'managerHasProduct', 'url', 'registerDate', 'registerAddress', 'registerProvince', 'registerCity', 'regAdrAgg', 'fundCount', 'fundScale', 'paidInCapital', 'subscribedCapital', 'hasSpecialTips', 'inBlacklist', 'hasCreditTips', 'regCoordinate', 'officeCoordinate', 'officeAddress', 'officeProvince', 'officeCity', 'primaryInvestType']



class Crawler(object):

    headers = {

        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "76",
        "Content-Type": "application/json",
        "Host": "gs.amac.org.cn",
        "Origin": "http://gs.amac.org.cn",
        "Referer": "http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    def __init__(self):
        self.session = requests.session()
        self._http_method = 'post'
        self._base_api = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager'
        self._response_type = 'json'
        self.write_flag = None
        self.total = 0


    @property
    def csv_fields(self):
        return FIELDS

    @property
    def response_type(self):
        return self._response_type

    @property
    def base_api(self):
        return self._base_api

    @property
    def http_method(self):
        return self._http_method

    def url_join(self,url_params):
        return self.base_api +"?" + parse.urlencode(url_params)


    def parse(self,keyword,primaryInvestType, page, size):
        url_params = {
            'rand': str(random.random())[:18],
            'page': str(page),
            'size': str(size)
        }
        api = self.url_join(url_params)
        post_data = {
            'keyword':keyword,
            'primaryInvestType':primaryInvestType
        }
        response = [-1]
        req = getattr(self.session, self.http_method)(url=api, headers=self.headers,data=json.dumps(post_data))
        if req.status_code == 200:
            response = getattr(req,self.response_type)()
            totalPages = response.get('totalPages',1)
            content = response.get('content',None)
            if content and totalPages >= 1:
                response = (page,size,totalPages,content)
            else:
                response = [-1]
        return response

    def write_csv(self,keyword,primaryInvestType,content):
        import csv
        func = lambda item:[str(item.get(i,'')).replace('<em>','').replace('</em>','') for i in self.csv_fields]
        datas = [func(item) for item in content]
        self.total += len(datas)
        file = keyword+'_'+primaryInvestType.replace('、','').replace(',','') + '.csv'
        print(file)
        if self.write_flag:
            mode = 'a'
        else:
            mode = 'w'
        with open(file,mode,encoding='utf-8') as fw:
            writer = csv.writer(fw)
            if self.write_flag:
                writer.writerows(datas)
            else:
                writer.writerow(self.csv_fields)
                writer.writerows(datas)
                self.write_flag = True



    def crawl(self,keyword,primaryInvestType, page, size):
        response = self.parse(keyword,primaryInvestType, page, size)
        if response[0] >=0:
            page, size, totalPages, content = [response[i] for i in range(4)]
            self.write_csv(keyword,primaryInvestType,content)
            for i in range(page+1,totalPages+1):
                _response = self.parse(keyword, primaryInvestType, i, size)
                if _response[0] >= 0:
                    self.write_csv(keyword, primaryInvestType, response[-1])
        print(keyword,primaryInvestType,self.total)






if __name__ == '__main__':
    citys = ["深圳","北京"]
    for keyword in citys:
        primaryInvestType = "私募证券投资基金管理人"#"私募股权、创业投资基金管理人"
        page, size = 0,10000
        crawler = Crawler()
        datas = crawler.crawl(keyword,primaryInvestType,page,size)


