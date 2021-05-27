

# 数据库初始化表

```
# 1.1 poem表 
CREATE TABLE `poem` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `dynasty_id` bigint(20) DEFAULT NULL,
  `dynasty` varchar(255) DEFAULT NULL,
  `poet_name` varchar(255) DEFAULT NULL COMMENT '诗人',
  `poet_url` varchar(255) DEFAULT NULL COMMENT '诗人url',
  `poem_name` varchar(255) DEFAULT NULL COMMENT '作品名称',
  `poem_url` varchar(255) DEFAULT NULL COMMENT '作品url',
  `contents` text COMMENT '诗歌内容',
  `poet_desc` text COMMENT '诗人简介',
  `crawl_url` varchar(500) NOT NULL DEFAULT '' COMMENT '抓取URL',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '抓取入库时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '抓取更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_poet_name` (`poet_name`),
  KEY `idx_dynasty` (`dynasty`),
  KEY `idx_poem_name` (`poem_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='唐诗宋词';


# 1.2 poeters表

CREATE TABLE `poeters` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `dynasty_id` varchar(255) DEFAULT NULL COMMENT '朝代id',
  `poeter_id` bigint(20) DEFAULT NULL COMMENT '诗人id',
  `poeter_name` varchar(255) DEFAULT NULL COMMENT '诗人',
  `poeter_desc` text COMMENT '诗人简介',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '抓取入库时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '抓取更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_poeter_id` (`poeter_id`),
  KEY `idx_dynasty_id` (`dynasty_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='诗人';

# 1.3  dynastys 朝代表

CREATE TABLE `dynastys` (
  `id` int(2) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `dynasty_id` bigint(20) DEFAULT NULL COMMENT '朝代id',
  `dynasty` varchar(255) DEFAULT NULL COMMENT '朝代',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '抓取入库时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '抓取更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_dynasty` (`dynasty`),
  UNIQUE KEY `idx_dynasty_id` (`dynasty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COMMENT='朝代列表';

# 1.4 china_poems表

CREATE TABLE `china_poems` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `poem_id` bigint(20) DEFAULT NULL,
  `poem_name` varchar(255) DEFAULT NULL COMMENT '作品名称',
  `dynasty_id` bigint(20) DEFAULT NULL,
  `poeter_id` varchar(255) DEFAULT NULL COMMENT '诗人',
  `contents` text COMMENT '诗歌内容',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '抓取入库时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '抓取更新时间',
  PRIMARY KEY (`id`),
  index `idx_dynasty_id`(`dynasty_id`),
  index `idx_poeter_id`(`poeter_id`),
  UNIQUE KEY `idx_poem_id` (`poem_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='唐诗宋词';

# 1.5 更新dynastys表
insert into dynastys(dynasty,dynasty_id)values
("先秦",72057594037927936),
("汉代",144115188075855872),
("三国两晋",216172782113783808),
("南北朝",288230376151711744),
("隋代",360287970189639680),
("唐代",432345564227567616),
("宋代",504403158265495552),
("元代",576460752303423488),
("明代",648518346341351424),
("清代",720575940379279360),
("近现代",792633534417207296);



#1.6 更新dynasty_id
update poem as m
join dynastys as q on m.dynasty=q.dynasty
set m.dynasty_id=q.dynasty_id

#1.7 初始化poeters表数据 诗人表
insert into poeters(dynasty_id,poeter_name,poeter_id,poeter_desc)
select a.dynasty_id,a.poet_name as poeter_name,replace(poet_url,"https://www.shi-ci.com/poet/","") as poeter_id,a.poet_desc as poeter_desc
from poem as a
group by dynasty_id,poet_name,replace(poet_url,"https://www.shi-ci.com/poet/",""),poet_desc

#1.8 初始化china_poems表数据 诗人表
insert into china_poems(poem_id,poem_name,dynasty_id,poeter_id,contents)
select replace(a.poem_url,"https://www.shi-ci.com/poem/","") as poem_id,a.poem_name,a.dynasty_id,b.poeter_id,a.contents
from poem as a
left join poeters as b on a.dynasty_id=b.dynasty_id and a.poet_name=b.poeter_name
```

# 运行爬虫

```
修改config/db_global.json下 password以后运行爬虫

scrapy crawl crawler_tangshi
```

# 不跑爬虫直接导入数据库
```
导入 data/data.sql 

```


