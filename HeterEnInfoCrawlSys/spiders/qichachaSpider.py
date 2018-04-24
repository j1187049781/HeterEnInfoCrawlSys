# coding: utf-8
import json

import re

from datetime import datetime
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from HeterEnInfoCrawlSys.items import BossZhiPinItem, QiChaChaItem


class qichachaSpider(RedisSpider):
    name = 'qichacha'
    chinese_to_eng_dict = {
        u'人员规模': 'staffNum',
        u'注册资本': 'registeredCapital',
        u'实缴资本': 'paidCapital',
        u'核准日期': 'foundingTime',
        u'所属行业': 'corpTpye',
        u'经营状态': 'managementStat',
        u'企业地址': 'registeredLoc',
        u'统一社会信用代码': 'unifiedCreditCode',
        u'经营范围': 'serviceDomain',
    }

    def start_requests(self):
        url_base = 'http://www.qichacha.com/g_SC_{}.html'
        max_page_num=500
        for i in range(1,max_page_num+1):
            url=url_base.format(i)
            yield Request(url=url, callback=self.pasre_company_list, dont_filter=True)
            break


    def pasre_company_list(self, response):
        url_base='http://www.qichacha.com'
        company_url_elem_list=response.xpath('//section[@class="panel panel-default"]/a/@href')
        company_url_list=[url_base+e.extract() for e in company_url_elem_list]
        for url in company_url_list:
            url='http://www.qichacha.com/firm_2a20f3d2817fbd7d518065df616c0068.html'
            yield Request(url=url,callback=self.pasre_company_info) # filter
    def pasre_company_info(self,response):
        '''corpName   名字
            corpIconUrl icon网址

            staffNum    Number of Staff;

            LegalRepresentative   法人代表
            registeredCapital    注册资本
            foundingTime    成立时间
            corpTpye   企业类型
            managementStat    经营状态
            registeredLoc   注册地址
            unifiedCreditCode  统一信用代码
            serviceDomain     经营范围

            tel   电话
            mail  邮箱
            website 官网
            paidCapital  实缴资本

            curlDate 抓取时间
            reference 来源url'''

        # this website for banning spider ,will return the <script/> randomly
        # <script>window.location.href=url;</script>
        if response.text.startswith('<script>'):
            yield Request(url=response.url, callback=self.pasre_company_info, dont_filter=True)

        else:

            item=QiChaChaItem()
            name=response.xpath('//div[@class="content"]/div/h1/text()').extract_first()
            if name is None:
                name=response.xpath('//div[@class="content"]/div/text()').extract_first()
            item['corpName']=name

            item['tel']=response.xpath('//div[@class="content"]/div[2]/span[@class="cvlu"]/span/text()').extract_first()
            item['mail']=response.xpath('//div[@class="content"]/div[3]/span[@class="cvlu"]/a/text()').extract_first()
            item['website']=response.xpath('string(//div[@class="content"]/div[3]/span[4])').extract_first()
            item['corpIconUrl']=response.xpath('//div[@class="logo"]/div[@class="imgkuang"]/img/@src').extract_first()

            item['LegalRepresentative']=response.xpath('//a[@class="bname"]/text()').extract_first()
            if item['LegalRepresentative'] is None:
                item['LegalRepresentative']=response.xpath('//a[@class="bcom"]/text()').extract_first()
            tb_elem_list=response.xpath('//section[@id="Cominfo"]/table[2]//td[@class="tb"]')

            # at below is the tabel containing company information
            info_tabel={e.xpath('./text()').extract_first().replace(u":",u'').replace(u"：",u'').strip():
                        e.xpath('./following-sibling::td[1]/text()').extract_first()
                        for e in tb_elem_list}

            for k,v in self.chinese_to_eng_dict.iteritems():
                try:
                    item[v]=info_tabel[k]
                except Exception:
                    item[v]=''

            item['reference'] = response.url  # 来源url
            item['curlDate'] = datetime.today()  # 抓取时间
            yield item




