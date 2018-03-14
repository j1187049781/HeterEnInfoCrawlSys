# -*- coding: utf-8 -*-
import json

import re

from datetime import datetime
from scrapy import Request

from scrapy_redis.spiders import RedisSpider

from HeterEnInfoCrawlSys.items import SbggItem, ZhaopinItem
from HeterEnInfoCrawlSys.util.reqUtil import params_post_toStr, params_get_toStr


class zhaopinSpider(RedisSpider):
    name = 'zhaopin'

    #url : get http://zhaopin.baidu.com/api/quanzhiasync?
    # sort_type=1&city=%E6%88%90%E9%83%BD&detailmode=close&rn=20&pn=20

    # http://zhaopin.baidu.com/api/xzzwmidasync?
    # sort_type=1&city=%E6%88%90%E9%83%BD&detailmode=close&rn=20&pn=20

    # http://zhaopin.baidu.com/api/jzzwmidasync?
    # sort_type=1&city=%E6%88%90%E9%83%BD&detailmode=close&rn=20&pn=20
    urlLoaction='http://zhaopin.baidu.com'
    apiList = ['http://zhaopin.baidu.com/api/quanzhiasync',
            'http://zhaopin.baidu.com/api/xzzwmidasync',
            'http://zhaopin.baidu.com/api/jzzwmidasync'
            ]
    header={
        'Content-Type': '*/*'
    }
    rn=760 # 最多有760条数据
    pn=0 # 从第一条开始
    citysSet = set()

    def start_requests(self):
            yield Request(url=self.urlLoaction,headers=self.header,
                          callback=self.parse)
    def parse(self, response): # get all citys
        html=response.text
        p=re.compile('<a href="\?city=.*?">(.*?)</a>',re.S)
        citys=re.findall(p,html)
        for city in citys:
            self.citysSet.add(city)
        for url in self.apiList:
            for city in self.citysSet:
                params={
                    'sort_type':'1',
                    'city':city,
                    'detailmode':'close',
                    'rn':self.rn,
                    'pn':self.pn
                }
                yield Request(url=params_get_toStr(url,params),headers=self.header,
                              callback=self.parseItem)

    def parseItem(self, response):
        # detail   # 一条记录
        # curlDate   # 抓取时间
        # reference   # 来源url
        jsn = response.text
        jsnObj = json.loads(jsn)
        list=jsnObj['data']['main']['data']['disp_data']
        if list:
            for obj in list:
                item = ZhaopinItem()
                item['detail'] = obj
                item['curlDate'] = datetime.today()  # 抓取时间
                yield item