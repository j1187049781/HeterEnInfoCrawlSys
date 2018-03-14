# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from HeterEnInfoCrawlSys.core.pipelines import MongoDBPipeline


class PersistencePipeline(MongoDBPipeline):
    def process_item(self, item, spider):
        collection=spider.name
        self.db[collection].insert_one(dict(item))
        return item
