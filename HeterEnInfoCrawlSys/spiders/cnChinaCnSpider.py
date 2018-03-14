# -*- coding: utf-8 -*-
import scrapy
import re

from datetime import datetime

from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from HeterEnInfoCrawlSys.items import CnchiancnItem


class CnchinacnSpider(RedisSpider):
    name = 'cnChinaCn'
    url='https://cn.china.cn/company/'
    def start_requests(self):
            yield Request(url=self.url, callback=self.parse)

    def parse(self, response):  # get all hrefs of companys
        html = response.text
        pattern = re.compile(r'<a href="(.*?t=\d*)">')  # 得到所有链接到企业列表的url
        hrefs = pattern.findall(html)
        for href in hrefs:
            yield scrapy.Request(href, callback=self.parseCompanys)

    def parseCompanys(self, response):  # this page has a list of companys
        item = CnchiancnItem()
        dic = {u'主营产品': 'product',
               u'所在地': 'corpLoc',
               u'员工人数': 'staffNum',
               u'品牌名称': 'brand'
               }

        selector = response.selector
        corpinfolist = selector.xpath('//div[@class="corpinfo"]')
        for corpinfo in corpinfolist:
            corpNname = corpinfo.xpath('.//a/text()').extract_first()
            corpUrl = corpinfo.xpath('.//@href').extract_first()
            item['corpName'] = corpNname  # 名字
            item['corpUrl'] = corpUrl  # 网址
            pList = corpinfo.xpath('.//p')
            for p in pList:
                key = p.xpath('.//span/text()').extract_first()
                value = p.xpath('./text()').extract_first()
                if dic.has_key(key):
                    item[dic[key]] = value;
            item['curlDate'] = datetime.today()  # 抓取时间
            item['reference'] = response.url  # 来源url
            yield item
        # turn to next page
        pageArea = selector.xpath('//div[@class="pagearea"]//@href').extract()
        for page in pageArea:
            yield scrapy.Request(page, callback=self.parseCompanys, dont_filter=False)  # filter the same url
