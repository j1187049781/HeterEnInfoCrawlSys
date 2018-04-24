# coding: utf-8
import json

import re

from datetime import datetime
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from HeterEnInfoCrawlSys.items import BossZhiPinItem


class bossszhipinSpider(RedisSpider):
    name = 'bosszhipin'
    province_name = '四川'
    sichuan_citys = []

    chinese_to_eng_dict = {u'法人代表': 'LegalRepresentative',
                           u'注册资本': 'registeredCapital',
                           u'成立时间': 'foundingTime',
                           u'企业类型': 'corpTpye',
                           u'经营状态': 'managementStat',
                           u'注册地址': 'registeredLoc',
                           u'统一信用代码': 'unifiedCreditCode',
                           u'经营范围': 'serviceDomain', }

    def start_requests(self):
        url = 'https://www.zhipin.com/common/data/city.json'
        yield Request(url=url, callback=self.pasre_location_id, dont_filter=True)

    def pasre_location_id(self, response):
        '''
        city.json :
        --> location : (id,location name)
        '''
        data = json.loads(response.text)
        privinces_list = data['data']['cityList']

        for province in privinces_list:
            if province['name'] == self.province_name:
                city_list = province['subLevelModelList']
                self.sichuan_citys = [(city['code'], city['name']) for city in city_list]
        # crawl from https://www.zhipin.com/job_detail/?scity=101271900
        url_base = 'https://www.zhipin.com/job_detail/?scity={}'
        for id, _ in self.sichuan_citys:
            url = url_base.format(id)
            yield Request(url=url, callback=self.parse_wanted_list, dont_filter=True)

    def parse_wanted_list(self, response):
        '''
        parse the list of position
        :param response:
        :return: [url of position,...]
        '''
        url_base = 'https://www.zhipin.com'
        job_div_list = response.xpath('//div[@class="job-primary"]')
        # in below is getting the url of company
        job_url_list = [url_base + job_div.xpath(
            './/div[@class="info-primary"]/h3[@class="name"]/a/@href')
            .extract_first()
                        for job_div in job_div_list]
        for url in job_url_list:
            yield Request(url=url, callback=self.parse_company_info_url)  # need filter

        # next page
        url_next_page_suffix = response.xpath('//div[@class="page"]/a[@class="next"]/@href').extract_first()
        if url_next_page_suffix is not None:
            url_next_page = url_base + url_next_page_suffix
            print url_next_page
            yield Request(url=url_next_page, callback=self.parse_wanted_list, dont_filter=True)

    def parse_company_info_url(self, response):
        '''
        get company_info_url from seeing all
        e.g:
        <div class="job-sec">
                            <h3>工商信息</h3>
                            <div class="name">博彦科技股份有限公司</div>
                            <div class="level-list">
                                <li><span>法人代表：</span>王斌</li>
                                <li><span>注册资金：</span>52637.550000万人民币</li>
                                <li class="res-time"><span>成立时间：</span>1995-04-17</li>
                                <li class="company-type"><span>企业类型：</span>股份有限公司(中外合资、上市)</li>
                                <li class="manage-state"><span>经营状态：</span>开业</li>
                            </div>
                            <a ka="job-cominfo" href="/gongsi/247788.html" target="_blank" class="look-all">查看全部</a>
                        </div>
        --> /gongsi/247788.html
        '''
        url_base = 'https://www.zhipin.com'
        p = u'''
        .*?<div class="job-sec">.*?<h3>工商信息</h3>.*?<a.*?href="(.*?)".*?>查看全部</a>'''
        company_info_url_list = re.findall(p, response.text, re.S)
        company_info_url = url_base + company_info_url_list[0] if company_info_url_list else ''
        if company_info_url:
            yield Request(url=company_info_url, callback=self.parse_company_info)  # need filter
        else:
            raise ValueError('compyany info url notis right: {}'.format(company_info_url))

    def parse_company_info(self, response):
        '''
        get company_info from tiyancha
        item:
        corpName  # 名字 not empty
        corpIconUrl # icon网址
        economyScale # 经济规模
        staffNum   # Number of Staff;
        serviceType   # 公司服务类型
        brief   # 简介
        LegalRepresentative  # 法人代表 not empty
        registeredCapital   # 注册资本 not empty
        foundingTime   # 成立时间 not empty
        corpTpye   # 企业类型 not empty
        managementStat   # 经营状态 not empty
        registeredLoc   # 注册地址 not empty
        unifiedCreditCode   # 统一信用代码 not empty
        serviceDomain # 经营范围 not empty
        corpLoc  # 公司地址
        curlDate  #抓取时间
        reference #来源url
        :param response:
        :return:
        '''
        item = BossZhiPinItem()
        item['corpName'] = response.xpath('//div[@class="info-primary"]/h1/text()').extract_first()

        try:
            item['corpIconUrl'] = response.xpath('//div[@class="company-logo"]/img/@src').extract_first()
        except BaseException, err:
            item['corpIconUrl'] = ''

        sub_title_str = response.xpath('//div[@class=info-primary]/p/text()').extract_first()
        if sub_title_str:
            try:
                economyScale, staffNum, economyScale = sub_title_str.split()
                item['economyScale'] = economyScale
                item['staffNum'] = economyScale
                item['serviceType'] = economyScale
            except BaseException, err:
                item['economyScale'] = ''
                item['staffNum'] = ''
                item['serviceType'] = ''

        brief_text_elem_list = response.xpath('//div[@class="job-sec"]/div[@class="text fold-text"]/text()')
        brief_text_list = [e.extract() for e in brief_text_elem_list]
        item['brief'] = u'\n'.join(brief_text_list)

        li_list = response.xpath(
            '//div[@class="job-sec company-business"]/div[@class="business-detail"]/ul/li')
        # parse li_list,to table
        info_table_dict = {li.xpath('./span/text()').extract_first().replace(':', '').replace('：', '')
                           : li.xpath('./text()').extract_first()
                           for li in li_list}
        for k, v in info_table_dict.iteritems():
            item[self.chinese_to_eng_dict[k]] = v

        try:
            text_elem_addr_list = response.xpath('//div[@class="location-address"]/text()')
            item['corpLoc'] = [addr.extract() for addr in text_elem_addr_list]
        except BaseException, err:
            item['corpLoc'] = []

        item['reference'] = response.url  # 来源url
        item['curlDate'] = datetime.today()  # 抓取时间
        yield item
