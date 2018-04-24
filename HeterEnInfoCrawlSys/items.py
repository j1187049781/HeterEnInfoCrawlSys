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

class BossZhiPinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    corpName = scrapy.Field()  # 名字
    corpIconUrl=scrapy.Field() # icon网址

    economyScale=scrapy.Field() # 经济规模
    staffNum = scrapy.Field()  # Number of Staff;
    serviceType = scrapy.Field()  # 公司服务类型

    brief = scrapy.Field()  # 简介

    LegalRepresentative = scrapy.Field()  # 法人代表
    registeredCapital = scrapy.Field()  # 注册资本
    foundingTime = scrapy.Field()  # 成立时间
    corpTpye = scrapy.Field()  # 企业类型
    managementStat = scrapy.Field()  # 经营状态
    registeredLoc = scrapy.Field()  # 注册地址
    unifiedCreditCode = scrapy.Field()  # 统一信用代码
    serviceDomain = scrapy.Field()  # 经营范围
    corpLoc = scrapy.Field()  # 公司地址



    curlDate =scrapy.Field() #抓取时间
    reference=scrapy.Field() #来源url

class QiChaChaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    corpName = scrapy.Field()  # 名字
    corpIconUrl=scrapy.Field() # icon网址

    staffNum = scrapy.Field()  # Number of Staff;

    LegalRepresentative = scrapy.Field()  # 法人代表
    registeredCapital = scrapy.Field()  # 注册资本
    foundingTime = scrapy.Field()  # 成立时间
    corpTpye = scrapy.Field()  # 企业类型
    managementStat = scrapy.Field()  # 经营状态
    registeredLoc = scrapy.Field()  # 注册地址
    unifiedCreditCode = scrapy.Field()  # 统一信用代码
    serviceDomain = scrapy.Field()  # 经营范围

    tel=scrapy.Field()  # 电话
    mail=scrapy.Field() # 邮箱
    website=scrapy.Field() # 官网
    paidCapital=scrapy.Field() # 实缴资本

    curlDate =scrapy.Field() #抓取时间
    reference=scrapy.Field() #来源url