#!/usr/bin/python
#coding:utf-8
import traceback

try:
    # 定义的plugins都需要自己补充
    import component_func, port_func
    from plugins import port_template
    from vuldect import pocsearchtask
    from httpdect.webdection import getgeoipinfo
except Exception,e:
    print traceback.print_exc()

def port_deal(ip='',port='',name='',productname='',head=None,context=None,nmapscript=None):
    head=None
    ans=None
    keywords=name
    hackresults=''
    # mysql/rsync/ssh2/ftpdeal 有内容
    # port:3306:mysql 873:rsync 22:ssh2 21:ftpdeal有内容
    port_function = getFunc(name,port,productname)
    if port_function != None:
    	# head=''/ans=None/keywords=func's name/hackresults='xx password' or 'Exception info'
        head, ans, keywords, hackresults = port_function(ip=ip,port=port,name=name,productname=productname)
    else:
        temp = pocsearchtask.getObject()
        temp.add_work([(head, context, ip, port, productname, keywords, nmapscript, name)])

    keyword={}
    keyword['ip'] = [ip]

    from spidertool import redistool
    redisresult = redistool.get(ip)
    if redisresult:
        print '从redids读取位置信息'
        keyword = redisresult
    else:
        keyword = getgeoipinfo.getGeoipinfo(ip)
        redistool.set(ip, keyword)
        print '从redids写入位置信息'
    keyword['keywords'] = keywords
    return head, ans, keyword, hackresults


def getFunc(name,port,productname):
    func=None
    print ("detection::port_identify::getFunc() name:%s port:%s"%(name, port))
    if name !='' and name != None:
        func = component_func.componentFunc.get(name,None)
    if str(port) !='':
        func = port_func.portFunc.get(str(port),None)
    else:
        func= None
    #检测对应产品，使用payload检测漏洞        
    return func


