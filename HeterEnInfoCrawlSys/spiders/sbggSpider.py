# -*- coding: utf-8 -*-
import json

import scrapy
import re

from datetime import datetime
from scrapy import Request

from scrapy_redis.spiders import RedisSpider

from HeterEnInfoCrawlSys.items import SbggItem
from HeterEnInfoCrawlSys.util.reqUtil import params_post_toStr


class SbggSpider(RedisSpider):
    name = 'sbgg'

    #url : post http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearchDG.html
    # param      名称: 值
    #             page: 1
    #             rows: 20
    #             annNum: 1580
    latestTerm=1593
    url = 'http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearchDG.html'
    header={
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    def start_requests(self):# 从第1期到latestTerm

        for annNum in xrange(1085,self.latestTerm+1):
            body = {
                'page': '1',
                'rows': '1000000',#默认每期没有超过1000000个
                'annNum': str(annNum)
            }
            yield Request(url=self.url,method='POST',headers=self.header,
                          body=params_post_toStr(body), callback=self.parse)
    def parse(self, response):

        # detail   # 一条记录
        # curlDate   # 抓取时间
        jsn=response.text
        jsnObj=json.loads(jsn)
        if jsnObj:
            for obj in jsnObj['rows']:
                item = SbggItem()
                item['detail']=obj
                item['curlDate'] = datetime.today()  # 抓取时间
                yield item