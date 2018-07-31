#!/usr/bin/python
#coding:utf-8


from datetime import datetime
from elasticsearch_dsl import DocType, Text, Date, Integer,MultiSearch,Search,Q
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class snifferdata(DocType):
    ip = Text(analyzer='ik')
    port = Text()
    timesearch = Text(analyzer='ik')
    state = Text(analyzer='ik')
    name = Text(index='not_analyzed')
    product = Text(analyzer='ik')
    version = Text(analyzer='ik')
    script = Text(analyzer='ik')
    detail = Text(analyzer='ik')
    id=Text()
    head = Text(analyzer='ik')
    hackinfo = Text(analyzer='ik')
    keywords = Text(analyzer='ik')
    disclosure = Text(analyzer='ik')
    webtitle  = Text(analyzer='ik')
    webkeywords  = Text(analyzer='ik')

    class Meta:
        index = 'datap'

    def save(self, ** kwargs):
        return super(snifferdata, self).save(** kwargs)
    def initindex(self):
        self.init()

    @classmethod
    def saysomething(self):
        print 'say something'

    @classmethod
    def getdata(cls,**kwargs):
        try:
            data=cls.get(**kwargs)
            print data
            return data
        except Exception, e:
            print "snifferdata.initindex() ", e

class ip_maindata(DocType):
    ip = Text(analyzer='ik')
    vendor = Text(analyzer='ik')
    osfamily = Text(analyzer='ik')
    osgen = Text(analyzer='ik')
    accurate = Text(index='not_analyzed')
    updatetime = Text(analyzer='ik')
    hostname = Text(analyzer='ik')
    state = Text(analyzer='ik')
    mac = Text(index='not_analyzed')
    country=Text()
    country_id = Text(index='not_analyzed')
    area = Text(index='not_analyzed')
    area_id = Text() 
    region = Text(index='not_analyzed') 
    region_id = Text(index='not_analyzed') 
    city = Text(index='not_analyzed') 
    city_id = Text() 
    county = Text(index='not_analyzed') 
    county_id = Text() 
    isp = Text(index='not_analyzed') 
    isp_id = Text() 

    class Meta:
        index = 'datap'

    def save(self, ** kwargs):
        return super(ip_maindata, self).save(** kwargs)
    def initindex(self):
        self.init()
    @classmethod
    def getdata(cls,**kwargs):
        try:
            data=cls.get(**kwargs)
            print data
            return data
        except Exception, e:
            print "ip_maindata().initindex ", e

if __name__ == "__main__":
    snifferdata().initindex()   
    ip_maindata().initindex() 
    print '创建索引成功'  
