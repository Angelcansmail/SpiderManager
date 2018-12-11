#!/usr/bin/python
#coding:utf-8
import sys;
reload(sys);

sys.setdefaultencoding('utf8');
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, MultiSearch, Search, Q
from elasticsearch_dsl.query import MultiMatch, Match
from elasticsearch_dsl.connections import connections
import mapping
from logger import initLog
logger = initLog('logs/elastic.log', 1, True)

import chardet
import traceback

# Define a default Elasticsearch client
connections.create_connection(hosts=['192.168.229.132'])
import base64

def decodestr(msg):
    chardit1 = chardet.detect(msg)
    try:
        # print chardit1['encoding'],msg.decode('gbk')
        if chardit1['encoding']=='utf-8' :
            return msg
        else:
            if  chardit1['encoding']=='ISO-8859-2':
                return msg.decode('gbk')
            else:
                if 'charset=gbk' in msg:

                    return msg.decode('gbk')
                else:
                    return msg.decode(chardit1['encoding']).encode('utf-8')
    except Exception,e:
        return str(msg)

def getproperty(dic,property):
    return decodestring(str(dic.get(property,' ')))

def decodestring(msg):
    item=msg
    if str==type(msg):
        try:
            try:
                item=msg.decode('string_escape').decode('string_escape')
            except Exception,e:
                item=msg.decode('string_escape')
                logger.error(e)
            
        except Exception,e:
	    logger.error(e)
        return decodestr(item)
    else:
        return ' '

# 调用mapping.py下的_cls_name(一个表名)函数，返回该表初始化对象
def get_table_obj(_cls_name):
    obj = getattr(mapping, _cls_name)
    return obj 

# set value to instance's key
def setvalue(instance,key,value):
	setattr(instance, key, value)
# data = mapping.snifferdata.getdata(id='116.13.94.6:80')
# data.delete()

def default():
    print 'there is error'

def inserttableinfo_byparams(table,select_params,insert_values, extra='', updatevalue=None,primarykey=1):
    instanceins = None
    instanceitem=None

    if table == 'snifferdata':
        primarykey = 2

    for item in insert_values:
        eachitem = None
        if type(item).__name__ == 'str':
            eachitem=tuple(item)
        else:
            eachitem=item
        # 表对象
        logger.info('elastictool::inserttableinfo_byparams::get_table_obj->%s', table)
        instanceins = get_table_obj(table)
#        logger.info('get each insert: %s', eachitem)
        # 有额外内容（ on duplicate key update xxx=aaa,yyy=bbb...
        if extra or updatevalue:
            instanceitem = instanceins.getdata(id=':'.join(eachitem[:primarykey]))
            logger.info("inserttableinfo_byparasm::instanceitem::%s", instanceitem)

            if instanceitem is None:
                logger.debug('找不到该数据，创建数据')
                instanceins = get_table_obj(table)
                instanceitem = instanceins(meta={'id': ':'.join(eachitem[:primarykey])})
        else:
            instanceitem = instanceins(meta={'id': ':'.join(eachitem[:primarykey])})

	update_data = ''
        for i in xrange(0,len(select_params)):
	    update_data += select_params[i] + '\t'
#	    update_data += select_params[i] + '=' + decodestr(str(eachitem[i])) + '\t'
            setvalue(instanceitem, select_params[i], decodestr(str(eachitem[i])))
#            logger.info('更新数据%s :%s',select_params[i], decodestr(str(eachitem[i])))
        logger.info('更新nmap tcp/udp \n%s', update_data)
        try:
            res = instanceitem.save()
        except Exception,e:
            logger.error("%s %s", str(e), str(traceback.print_exc()))
        else:
            logger.info('insert success')

def replaceinserttableinfo_byparams(table,select_params,insert_values,primarykey=1):
    inserttableinfo_byparams(table,select_params,insert_values,primarykey=primarykey)
# inserttableinfo_byparams('snifferdata', ['ip','port','product'], [('1','2','http')],primarykey=2)


def search(page='0',dic=None, content=None):
    limitpage=15
    validresult=False
    orderlabel=0
    orderarray = []
    print ("======================elastictool::search dic:%s content:%s======================"%(str(dic), str(content)))

    if content is not None:
        q = Q("multi_match", query=content, fields=['ip', 'name','product',
                'script' ,'detail' ,'head', 'hackinfo', 'hackresults','keywords' ,'disclosure'])
    # 当按照条件检索的时候，dic是将content转为json格式的内容，content为None
    else:
        searcharray=[]
        keys = dic.keys()
        orderlabel=0

        for key in keys:
            if key=='name':
                searcharray.append(Q('term', name=dic[key]))
            if key=='ip':
                searcharray.append(Q('term', ip=dic[key]))
            if key=='port':
                searcharray.append(Q('term', port=dic[key]))
            if key=='state':
                searcharray.append(Q('term', state=dic[key]))
            if key=='timesearch':
                searcharray.append(Q('match', timesearch=dic[key]))                 
            if key=='keywords':
                searcharray.append(Q('match', keywords=dic[key]))                     
            if key=='product':
                searcharray.append(Q('match', product=dic[key]))                       
            if key=='version':
                searcharray.append(Q('match', version=dic[key]))                   
            if key=='script':
                searcharray.append(Q('match', script=dic[key]))               
            if key=='hackinfo':
                searcharray.append(Q('match', hackinfo=dic[key]))
            if key=='hackresults':
                searcharray.append(Q('match', hackresults=dic[key]))
            if key=='head':
                searcharray.append(Q('match', head=dic[key]))                
            if key=='detail':
                searcharray.append(Q('match', detail=dic[key]))                
            if key=='disclosure':
                searcharray.append(Q('match', disclosure=dic[key]))
            if key == 'webtitle':
                searcharray.append(Q('match', webtitle=dic[key]))
            if key == 'webkeywords':
                searcharray.append(Q('match', webkeywords=dic[key]))
            if key=='order':
                orderarray.append(dic[key])
                orderlabel=1
        # MultiMatch(fields=['ip', 'name', 'product', 'script', 'detail', 'head', 'hackinfo', 'hackresults', 'keywords', 'disclosure'], query=u'mysql')
        q = Q('bool', must=searcharray)
    print ("======================elasticsearch::Q:\n%s\n"%q)
    # elasticsearch检索数据库信息
    if orderlabel == 0:
        s = Search(index='datap', doc_type='snifferdata').query(q)
    else:
        s = Search(index='datap', doc_type='snifferdata').query(q).sort(orderarray[0])
#     s = Search.from_dict({"query": {
#     "bool":{
#             "must":[               
#                 {
#                     "term":{"name":"http"},
#                     "term":{"port":"80"},
#                 },
#                 {
#                     "match":{"head":"manager"},
#                      "match":{"head":"200"},
#                 }
#                 ]
#         }
# }
# })
    s = s[int(page)*limitpage:int(page)*limitpage+limitpage]

    # elasticsearch_dsl/search.py
    response = s.execute()
    print ("======================elasticsearch results:%s, response::%s======================"%(str(s), str(response)))

    if response.success():
        portarray=[]
        count = response.hits.total
        print '返回的集中率为%d' % count
        if count == 0:
            pagecount = 0;
        elif count % limitpage> 0:
            pagecount=int((count+limitpage-1)/limitpage) 
        else:
            pagecount = count / limitpage

        from nmaptoolbackground.model import ports
        count = len(response)
        print '返回的实际数量为%d' % count 
        if count > 0:
            for temp in response :
                dic=temp.to_dict()
                # 只获取snifferdata中的数据，没有位置信息，这里将city赋为空作用和在，后面用了city判断，直接用
#                print ("elastictool::search() index:count[%s]'s dic keys:%s"%(str(count), str(dic.keys())))
                aport = ports.Port(ip=getproperty(dic,'ip'),port=getproperty(dic,'port'),timesearch=getproperty(dic,'timesearch'),state=getproperty(dic,'state'),name=getproperty(dic,'name'),product=getproperty(dic,'product'),version=getproperty(dic,'version'),script=base64.b64encode(str(getproperty(dic,'script'))),detail=getproperty(dic,'detail'),head=getproperty(dic,'head'),city='',hackinfo=getproperty(dic,'hackinfo'),hackresults=getproperty(dic,'hackresults'),disclosure=getproperty(dic,'disclosure'),keywords=getproperty(dic,'keywords'),webtitle=base64.b64encode(str(getproperty(dic,'webtitle'))),webkeywords=getproperty(dic,'webkeywords'))
                # ip=getproperty(dic,'ip')
                # port=getproperty(dic,'port')
                # timesearch=getproperty(dic,'timesearch')
                # state=getproperty(dic,'state')
                # name=getproperty(dic,'name')
                # product=getproperty(dic,'product')
                # version=getproperty(dic,'version')
                # script=base64.b64encode(getproperty(dic,'script'))
                # detail=getproperty(dic,'detail')
                # head=getproperty(dic,'head')
                # city=''
                # hackresults=getproperty(dic,'hackresults')
                # disclosure=getproperty(dic,'disclosure')
                portarray.append(aport)
        return portarray, count, pagecount
    else:
        print '查询失败'
        return [],0,0


# print ":".join(map(str, item[:3]))
# data = default.getdata(id='12')
# data.delete()
# Display cluster health
# print(connections.get_connection().cluster.health())

#search

# ms = MultiSearch(index='datap',doc_type='snifferdata')
# searcttext='http'
# s=Search().query(Q("match", IP=searcttext) | 
# # 											Q("match", Port=(int(searcttext) if searcttext.isdigit() else 0)) | 
# # 											Q("match", Timesearch=searcttext) | 
# # 											Q("match", State=searcttext) | 
# 											Q("match", Name=searcttext) | 
# 											Q("match", Product=searcttext) | 
# # 											Q("match", Version=searcttext) | 
# 											Q("match", Script=searcttext) | 
# 											Q("match", Detail=searcttext) | 
# 											Q("match", Head=searcttext) | 
# 											Q("match", Hackinfo=searcttext) | 											
# 											Q("match", Keywords=searcttext) | 											
# 											Q("match", Disclosure=searcttext)  											
# )
# ms=ms.add(s)
# responses = ms.execute()
# 
# 
# 
# 
# 
# for response in responses:
#     print("Results for query %r." % response.search.query)
#     try:
#         for hit in response:
#             print hit.doc_types
#     except Exception,e:
#         print e







# 
# c=Search().query('match',Timesearch='2012-03-00')
# c.execute()
# d=list(c)
# print len(d)
# for hit in d:
#     print hit
#     
    
    
if __name__ == '__main__':
    # print search(page='0', dic=None, content='218.28.144.77')
    print '\xD6\xD0\xB9\xFA\xD1\xCC\xB2\xDD\xC5\xE0\xD1\xB5\xCD\xF8'.decode('gbk')
