#!/usr/bin/python
#coding:utf-8
import sys;
reload(sys);

sys.setdefaultencoding('utf8');
from elasticsearch_dsl.query import MultiMatch, Match
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer,MultiSearch,Search,Q
from elasticsearch_dsl.connections import connections
import mapping
from logger import initLog
import chardet
logger = initLog('/root/log/detect/logs/elastic.log', 2, True)

import base64

def ipsearch(page='0',dic=None,content=None):
    limitpage=15
    validresult=False
    orderlabel=0
    orderarray = []
    print ("======================ipestool::ipsearch() dic:%s, content:%s======================"%(dict, content))
    if content is not None:
        # MultiMatch(fields=['ip', 'name', 'product', 'script', 'detail', 'head', 'hackresults', 'keywords', 'disclosure'], query=u'database')
        q = Q("multi_match", query=content, fields=['ip', 'city','vendor',
                'isp' ,'region' ,'area', 'country'  ,'updatetime','county' ,'osfamily'  ])
    # GET方式访问/ipsearch传入dict(貌似只有一个ip)
    else:
        searcharray=[]
        keys = dic.keys()
        orderlabel=0

        for key in keys:
            if key=='city':
                searcharray.append(Q('term', city=dic[key]))
            if key=='ip':
                searcharray.append(Q('term', ip=dic[key]))
            if key=='isp':
                searcharray.append(Q('term', isp=dic[key]))
            if key=='region':
                searcharray.append(Q('term', region=dic[key]))
            if key=='area':
                searcharray.append(Q('term', area=dic[key]))
            if key=='order':
                orderarray.append(dic[key])
                orderlabel=1
        q = Q('bool', must=searcharray) # Bool(must=[Term(ip='110.110.110.120')])
    print ("======================elasticsearch Q:======================\n%s\n"%q)

    if orderlabel == 0:
        s = Search(index='datap', doc_type='ip_maindata').query(q)
    else:
        s = Search(index='datap', doc_type='ip_maindata').query(q).sort(orderarray[0])

    s = s[int(page)*limitpage:int(page)*limitpage+limitpage]

    response = s.execute()
    print ("======================elasticsearch results:%s\nresponse::%s======================"%(str(s), str(response)))

    if response.success():
        portarray=[]
        count= response.hits.total
        print '返回的集中率为%d' % count
        if count == 0:
            pagecount = 0;
        elif count % limitpage> 0:
            pagecount=int((count+limitpage-1)/limitpage)
        else:
            pagecount = count / limitpage
        from nmaptoolbackground.model import ipmain
        count=len(response)
        print '返回的实际数量为%d' % count
        from elastictool import getproperty

        if count > 0:
            for temp in response:
                dicc = temp.to_dict()
                print ("\n======================ipestool::showIP======================\n%s"%str(dicc))
                aip = ipmain.Ip(ip=getproperty(dicc,'ip'),vendor=getproperty(dicc,'vendor'),osfamily=getproperty(dicc,'osfamily'),osgen=getproperty(dicc,'osgen'),accurate=getproperty(dicc,'accurate'),state=getproperty(dicc,'state'),hostname=getproperty(dicc,'hostname'),updatetime=getproperty(dicc,'updatetime'),city=getproperty(dicc,'city'),isp=getproperty(dicc,'isp'),county=getproperty(dicc,'county'),country=getproperty(dicc,'country'),region=getproperty(dicc,'region'),area=getproperty(dicc,'area'))
                print ('\n======================ipestool get ip\"s response:======================\n%s\n' % str(aip))
                portarray.append(aip)
        else:
            pass
            portarray.append(ipmain.Ip(ip=dic['ip']))
        return portarray, count, pagecount
    else:
        print '查询失败'
        return [], 0, 0
