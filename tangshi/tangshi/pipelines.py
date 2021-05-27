# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import json

from twisted.enterprise import adbapi



TO_DB = "spider".strip()
TO_TABLE = "poem".strip()
TO_DB_TYPE = "mysql".strip()
TO_APP = "rds-local".strip()
CONF_KEY = TO_APP + "_" + TO_DB


class ConfigParseException(Exception):
    pass

class TangshiPipeline:
   
    def __init__(self, dbpool):
        self.dbpool = dbpool
    
    @classmethod
    def from_settings(cls,settings):
        config_file = settings.get('CONFIG_FILE')
        with open(config_file) as fr:
            configs = json.load(fr)
        config = configs["from"].get(TO_DB_TYPE,{}).get(CONF_KEY,{})
        if not config:
            raise ConfigParseException("from %s get %s is None" % (TO_DB_TYPE,CONF_KEY))
        dbpool = adbapi.ConnectionPool('pymysql', **config)
        return cls(dbpool)
    
    
    #如果对数据要处理 使用这个函数进行处理
    def handle_data(self,data):
        return data

    def process_item(self, item, spider):
        data = dict(item)
        #需要处理数据时候调用handle_data
        #data = self.handle_data(data)
        query = self.dbpool.runInteraction(self.save_data, data)
        query.addErrback(self.handle_error, item)
       
       
    
    def handle_error(self, failure, item):
        print('插入数据失败，原因:%s，item:%s' % (failure, item))
    

    def save_data(self, cursor,data):
        try:
            _fields = list(data.keys())
            base_sql = 'insert into {to_db}.{table}  ({fields}) values({_str})'
            values = [data.get(i, None) for i in _fields]
            sql = base_sql.format(to_db=TO_DB,table=TO_TABLE, fields=','.join(_fields), _str=','.join(['%s' for i in _fields]))
            cursor.execute(sql, values)
        except Exception as e:
            print(e)
    
    def close_spider(self, spider):
        self.dbpool.close()
       
    
        
