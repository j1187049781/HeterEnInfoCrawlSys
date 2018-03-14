# coding:utf-8
import multiprocessing
import random
import urllib2

import re

from datetime import datetime

from pymongo import MongoClient

from HeterEnInfoCrawlSys import settings

class ProxyPoolMannt:

    def __del__(self):
        self.closePool()

    def openPool(self):

        self.client = MongoClient(settings.DB_URL,connect=False)
        self.db = self.client[settings.DB_NAME]
        self.db["ipPool"].remove()

    def closePool(self):
        self.client.close()
    def testIp(self, ip,to,turn):
        while turn>0:
            try:
                proxy_handler = urllib2.ProxyHandler({'http': 'http://' + ip, 'https': 'https://' + ip})
                opener = urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)
                req = urllib2.Request('https://www.baidu.com')
                conn = urllib2.urlopen(req,timeout=to)
            except BaseException ,e:
                print "testIp"+e.message
                return False
            finally:
                turn-=1
            return True

    def getIp(self):
        if self.ipPool is not None:
            index = random.randint(0, len(self.ipPool) - 1)
            return self.ipPool[index]

    def crawlIP(cls):
        try:
            req = urllib2.Request("http://www.89ip.cn/apijk/?&tqsl=100&sxa=&sxb=&tta=&ports=&ktip=&cf=1")
            res = urllib2.urlopen(req,timeout=10)
            html = res.read()
            ips = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,6})', html)
            return ips
        except BaseException,e:
            print("crawIP:"+e.message)

    def start(self):
        while True:
            ips = self.crawlIP()
            if ips is not None:
                for ip in ips:
                    if self.testIp(ip,3,3):
                        print ip +' is valid'
                        ipDoc = {"ip": ip,
                                 "genDate": datetime.today()
                                 }
                        self.toDB(ipDoc)

    def toDB(self, ipdoc):
        try:
            query = {"ip": ipdoc['ip']}
            isExist = self.db['ipPool'].find(query)
            if isExist.count()==0:
                self.db['ipPool'].insert_one(ipdoc)
                print ("save ip to db : " + ipdoc['ip'])
        except BaseException, e:
            print "to db"+e.message

    def invalid(self):
        while True:
            try:
                ipDocs = self.db['ipPool'].find()
                for ipDoc in ipDocs:
                    if (datetime.today()-ipDoc['genDate']).total_seconds()>60*3:
                        if not self.testIp(ipDoc['ip'],10,1):
                            self.db['ipPool'].remove(ipDoc)
                            print ("rm ip to db : " + ipDoc['ip'])
            except BaseException,e:
                print "invalid:"+e.message

if __name__=='__main__':
    ipPool=ProxyPoolMannt()
    ipPool.openPool()
    ipPoolStartProcess=multiprocessing.Process(target=ipPool.start)
    ipPoolStartProcess.start()
    ipPoolInvalidProcess=multiprocessing.Process(target=ipPool.invalid)
    ipPoolInvalidProcess.start()