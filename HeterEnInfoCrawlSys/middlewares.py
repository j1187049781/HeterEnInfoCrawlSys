# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import hashlib
import logging

import time
from scrapy import signals
from settings import proxyPass, proxyServer, proxyUser, orderno, secret, ip_port


class HetereninfocrawlsysSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ABuYunProxyMiddleware(object):
    """cover scrapy's HttpProxyMiddleware.

       if 'proxy' in request.meta, HttpProxyMiddleware don't do anything.

     """
    proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass)

    def process_request(self, request, spider):


        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = self.proxyAuth


class XunDaiLiProxyMiddleware(object):
    """cover scrapy's HttpProxyMiddleware.

       if 'proxy' in request.meta, HttpProxyMiddleware don't do anything.

     """

    def process_request(self, request, spider):
        timestamp = str(int(time.time()))  # 计算时间戳
        s = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

        md5_string = hashlib.md5(s).hexdigest()  # 计算sign
        sign = md5_string.upper()  # 转换成大写
        auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
        # proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}

        request.meta["proxy"] = "http://" + ip_port
        request.headers["Proxy-Authorization"] = auth