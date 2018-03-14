# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnchiancnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    corpName = scrapy.Field()  # 名字
    corpUrl=scrapy.Field() #网址
    product = scrapy.Field()  # 产品
    corpLoc = scrapy.Field()  # 产地
    staffNum = scrapy.Field()  # Number of Staff;
    brand = scrapy.Field()  # 品牌名称
    curlDate =scrapy.Field() #抓取时间
    reference=scrapy.Field() #来源url

class SbggItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    detail= scrapy.Field()  # 一条记录
    curlDate =scrapy.Field() #抓取时间

class ZhaopinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    detail= scrapy.Field()  # 一条记录
    curlDate =scrapy.Field() #抓取时间