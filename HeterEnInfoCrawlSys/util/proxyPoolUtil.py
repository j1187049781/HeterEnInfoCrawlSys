import random
import urllib2

import re

import gevent
from pymongo import MongoClient
from HeterEnInfoCrawlSys import settings


class ProxyUtil:
    client=None
    @classmethod
    def open(cls):
        if cls.client is None:
            cls.client = MongoClient(settings.DB_URL)
            cls.db = cls.client[settings.DB_NAME]
    def __del__(self):
        self.client.close()

    @classmethod
    def getIp(cls):
        ips=cls.db['ipPool'].find()
        count=ips.count()
        if count !=0:
            index=random.randint(0,count-1)
            return ips[index]['ip']