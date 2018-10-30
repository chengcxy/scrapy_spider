# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



import pymysql
class SoybasePipeline(object):

    def __init__(self):
        self.MYSQLCONFIG = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '密码',
            'db': '数据库',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**self.MYSQLCONFIG)
        self.cursor = self.conn.cursor()

    @property  # 方法变属性
    def fields(self):
        sql = 'select * from soybase limit 1'
        self.cursor.execute(sql)
        # 数据表字段的描述
        description = self.cursor.description
        # 数据库字段 由于数据库字典加了主键自增id 抓取的数据里 并没有这个 因此切片从索引1开始
        fields = [x[0] for x in description][1::]
        return fields
    #建表
    def create_table(self):
        create_sql = '''
CREATE TABLE `soybase` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id自增',
  `first_url` varchar(255) DEFAULT NULL COMMENT '第一层url',
  `first_name` varchar(255) DEFAULT NULL COMMENT '第一层名称',
  `second_url` varchar(255) DEFAULT NULL COMMENT '第二层url',
  `QTL_url` varchar(255) DEFAULT NULL COMMENT 'QQTL_url',
  `QTL_name` varchar(255) DEFAULT NULL COMMENT 'QTL_name',
  `parent1` varchar(255) DEFAULT NULL COMMENT 'parent1',
  `parent2` varchar(255) DEFAULT NULL COMMENT 'parent2',
  `reference_title` varchar(255) DEFAULT NULL COMMENT 'reference_title',
  `reference_magzine` varchar(255) DEFAULT NULL COMMENT 'reference_magzine',
  `mark_url` varchar(255) DEFAULT NULL COMMENT 'mark_url',
  `mark_3` varchar(255) DEFAULT NULL COMMENT 'mark_3',
  `mark_5` varchar(255) DEFAULT NULL COMMENT 'mark_5',
  `create_time` varchar(255) DEFAULT NULL COMMENT '抓取时间',
  PRIMARY KEY (`id`),
  KEY `QTL_name` (`QTL_name`),
  KEY `create_time` (`create_time`)
) ENGINE=InnoDB AUTO_INCREMENT=314 DEFAULT CHARSET=utf8 COMMENT='soybase爬虫';
'''
        self.cursor.execute(create_sql)
        self.conn.commit()
        info = 'soybase表创建成功!'
        return info


    def process_item(self, item, spider):

        print('item---',item)
        fields = self.fields
        fields_num = len(fields)
        # 字段列表 转字符串 用于拼接sql
        str_fields = ','.join(fields)
        # %s占位符列表转字符串 根据字段列表长度 生成 用于拼接sql
        str_fields_num = ','.join(['%s' for i in range(fields_num)])
        insert_sql = 'insert into soybase({}) values({})'.format(str_fields, str_fields_num)
        # 插入数据库
        self.cursor.execute(insert_sql, (\
        item['first_url'], item['first_name'], item['second_url'], item['QTL_url'], item['QTL_name'],\
        item['parent1'],item['parent2'],item['reference_title'],item['reference_magzine'], \
        item['mark_url'],item['mark_3'],item['mark_5'],item['create_time']))
        self.conn.commit()


