# coding:UTF-8
import hashlib
import os
from pymongo import MongoClient
from pybloom import ScalableBloomFilter
from scrapy.exceptions import DropItem

from HeterEnInfoCrawlSys import settings


class Pipeline(object):
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        pass


class MongoDBPipeline(Pipeline):
    collection = 'defaultCollection'

    def open_spider(self, spider):
        # An important note about collections (and databases) in MongoDB is that they are created lazily
        # none of the above commands have actually performed any operations on the MongoDB server.
        # Collections and databases are created when the first document is inserted into them
        self.client = MongoClient(settings.DB_URL)
        self.db = self.client[settings.DB_NAME]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection].insert_one(dict(item))
        return item


class DuplicateItemFilterPipeline(Pipeline):  # bloomfiler 序列化
    fileName = "DuplicateItemFilter.dat"

    def open_spider(self, spider):
        self.fileName = spider.name+self.fileName
        if os.path.exists(self.fileName):
            with open(self.fileName, 'rb') as f:
                self.sbf = ScalableBloomFilter.fromfile(f)
        else:
            self.sbf = ScalableBloomFilter(mode=ScalableBloomFilter.LARGE_SET_GROWTH)
        pass

    def close_spider(self, spider):
        with open(self.fileName, 'wb') as f:
            self.sbf = self.sbf.tofile(f)
        pass

    def process_item(self, item, spider):  # bloomfiler
        fp = hashlib.sha1()
        for key in item.keys():
            if key not in ['curlDate', 'reference'] \
                    and item[key] is not None:  # 不比较抓取时间，来源url
                fp.update(item[key])
        fpValue = fp.hexdigest()
        if not self.sbf.add(fpValue):
            return item
        else:
            raise DropItem("duplicate item :/n %s" % item)
