#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse

from nmaptoolbackground.control import portcontrol
from spidertool import webtool
from fontsearch.control import mapcontrol

import json
import time
import traceback

from logger import initLog
logger = initLog('/root/log/baozhang/logs/search.log', 1, False)

timeout=60*20

def indexpage(request):
    username = request.COOKIES.get('username','')
    return render_to_response('fontsearchview/search.html', {'data':'','username':username})

def mainpage(request):
    content = request.GET.get('searchcontent','')
    page = request.GET.get('page','0')
    username = request.COOKIES.get('username','')
    content = content.replace(' ','%20')
    return render_to_response('fontsearchview/searchdetail.html', {'content':content,'page':page,'username':username})

# 展示详细结果界面, 主机位置链接跳转
def detailmapview(request):
    username = request.COOKIES.get('username', '')
    ip = request.GET.get('ip', '')
    return render_to_response('fontsearchview/detailmapview.html', {'data': '', 'username': username,'ip':ip})

# fontsearch首页搜索查询信息结果
def detailpage(request):
    from spidertool import redistool, webtool
    content = request.POST.get('content', '')
    page = request.POST.get('page','0')
    username = request.COOKIES.get('username','')
    userrole = request.COOKIES.get('role', '')
    response_data = {}
    response_data['result'] = '0'
    jsoncontent = None
    ports=None

    try:
        jsonmsg = '{' + content + '}'
        jsoncontent = json.loads(jsonmsg)
    except Exception, e:
        logger.error(str(traceback.print_exc()))
        pass

    logger.debug('Search %s', str(jsoncontent))
#   content: "ip":"110.110.110.120" --> jsoncontent: {u'ip': u'110.110.110.120'}
#   normal search
    if jsoncontent is None:
        logger.debug('Into normal search.')
        if content != '' and len(content) > 0:
            logger.debug('Content not null, into EL search')
#         extra='    or   script  like \'%'+content+'%\' or detail  like \'%'+content+'%\'  or timesearch like ' +'\'%'+content+'%\' or head like \'%' +content+'%\') and  snifferdata.ip=ip_maindata.ip '
#         ports,portcount,portpagecount = portcontrol.portabstractshow(ip=content,port=content,timesearch=content,state=content,name=content,product=content,version=content,page=page,extra=extra,command='or')
            try:
                item = webtool.md5('sch_'+str(content)+'page'+str(page))
                redisresult = redistool.get(str(item))

                if redisresult:
                    logger.debug('Get data from redis.')
                    try:
                        response_data['ports'] = redisresult['ports']
                        response_data['portslength'] = redisresult['portslength']
                        response_data['portspagecount'] = redisresult['portspagecount']
                        response_data['portspage'] = redisresult['portspage']
                    except Exception,e:
                        import sys
                        sys.path.append("..")
                        from elasticsearchmanage import elastictool
                        ports, portcount, portpagecount = elastictool.search(page=page, dic=None, content=content)

                        redisdic = {}
                        redisdic['ports'] = ports
                        redisdic['portslength'] = portcount
                        redisdic['portspagecount'] = portpagecount
                        redisdic['portspage'] = page

                        redistool.set(item, redisdic)
                        redistool.expire(item, timeout)

                        response_data['ports'] = ports
                        response_data['portslength'] = portcount
                        response_data['portspagecount'] = portpagecount
                        response_data['portspage'] = page
                else:
                    logger.debug('Get data from EL.')
                    import sys
                    sys.path.append("..")
                    from elasticsearchmanage import elastictool
                    ports, portcount, portpagecount = elastictool.search(page=page,dic=None,content=content)

                    redisdic = {}
                    redisdic['ports'] = ports
                    redisdic['portslength'] = portcount
                    redisdic['portspagecount'] = portpagecount
                    redisdic['portspage'] = page

                    redistool.set(item, redisdic)
                    redistool.expire(item, timeout)

                    response_data['ports'] = ports
                    response_data['portslength'] = portcount
                    response_data['portspagecount'] = portpagecount
                    response_data['portspage'] = page
            except Exception,e:
                # 连接失败
                logger.warning('EL Search Error:%s. Use Fuzzy search in DB', str(traceback.print_exc()))
                try:
                    # 模糊检索 match against
                    extra = ' where match(version,product,head,detail,script,hackinfo,hackresults,disclosure,keywords,name,webkeywords,webtitle) against(\'' + content + '\' in Boolean mode) '
                    ports, portcount, portpagecount = portcontrol.portabstractshow(page=page,extra=extra,command='or')
                    # ports, portcount, portpagecount = getattr(portcontrol, 'portabstractshow', 'portabstractshow')(**jsoncontent)
                    response_data['ports'] = ports
                    response_data['portslength'] = portcount
                    response_data['portspagecount'] = portpagecount
                    response_data['portspage'] = page
                except Exception,e:
                    logger.error("detailpage Normal EL search Error:%s", str(traceback.print_exc()))
            logger.debug('Finish Search %s.', content)
            response_data['result'] = '1'
            response_data['keywords'] = content.split()
            response_data['username'] = username
            response_data['userrole'] = userrole
#   search by condition
    else:
        logger.debug('Into condition search.')
        action = jsoncontent.keys()
#	what's the use of use
        if 'use' in action or 'city' in action:
            if 'use' in action:
                del jsoncontent['use']

            jsoncontent['page'] = page

            if 'all' in action:
                extra = ' where match(version,product,head,detail,script,hackinfo,hackresults,disclosure,keywords) against(\''+jsoncontent['all']+'\' in Boolean mode)  '
                ports,portcount,portpagecount = portcontrol.portabstractshow(page=page,extra=extra,command='or')
            else:
                ports, portcount, portpagecount = getattr(portcontrol, 'portabstractshow','portabstractshow')(**jsoncontent)

            response_data['ports']=ports
            response_data['portslength']=portcount
            response_data['portspagecount']=portpagecount
            response_data['portspage']=page
        else:
            if len(content)==0:
                return HttpResponse(json.dumps(response_data,skipkeys=True,default=webtool.object2dict), content_type="application/json")  
            logger.debug('Into condition elasticsearch special keywords match.')
            try:
                item = str(webtool.md5('sch_' + str(jsoncontent) + '_page' + str(page)))
                redisresult = redistool.get(item)

                if redisresult:
                    logger.debug('Get data from redis.')
                    try:
                        response_data['ports'] = redisresult['ports']
                        response_data['portslength'] = redisresult['portslength']
                        response_data['portspagecount'] = redisresult['portspagecount']
                        response_data['portspage'] = redisresult['portspage']
                    except Exception,e:
                        import sys
                        sys.path.append("..")
                        from elasticsearchmanage import elastictool
                        ports, portcount, portpagecount = elastictool.search(page=page, dic=jsoncontent, content=None)

                        response_data['ports'] = ports
                        response_data['portslength'] = portcount
                        response_data['portspagecount'] = portpagecount
                        response_data['portspage'] = page

                        redisdic = {}
                        redisdic['ports'] = ports
                        redisdic['portslength'] = portcount
                        redisdic['portspagecount'] = portpagecount
                        redisdic['portspage'] = page
                        redistool.set(item, redisdic)
                        redistool.expire(item, timeout)
                else:
                    logger.debug('Get data from EL.')
                    import sys
                    sys.path.append("..")
                    from elasticsearchmanage import elastictool
                    ports,portcount,portpagecount = elastictool.search(page=page,dic=jsoncontent,content=None)

                    response_data['ports'] = ports
                    response_data['portslength'] = portcount
                    response_data['portspagecount'] = portpagecount
                    response_data['portspage'] = page

                    redisdic = {}
                    redisdic['ports'] = ports
                    redisdic['portslength'] = portcount
                    redisdic['portspagecount'] = portpagecount
                    redisdic['portspage'] = page

                    logger.debug('Save %s search results to redis.'%content)

                    redistool.set(item, redisdic)
                    redistool.expire(item, timeout)

                    logger.debug('Save to redis Done.')

            except Exception,e:
                logger.error("detailpage condition search Error:%s"%str(traceback.print_exc()))
                ports, portcount, portpagecount = getattr(portcontrol, 'portabstractshow', 'portabstractshow')(**jsoncontent)
                response_data['ports']=ports
                response_data['portslength']=portcount
                response_data['portspagecount']=portpagecount
                response_data['portspage']=page

            response_data['result'] = '1'
            response_data['keywords'] = jsoncontent.values()
            response_data['username']=username
	    response_data['userrole'] = userrole
    try:
        return HttpResponse(json.dumps(response_data,skipkeys=True,default=webtool.object2dict), content_type="application/json")
    except Exception,e:
        logger.error("Searchdetail Error:%s", str(e))
        return HttpResponse(json.dumps(response_data,skipkeys=True,default=webtool.object2dict,encoding='latin-1'), content_type="application/json")

        # return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict, encoding='GB2312'),
        #             content_type="application/json")

# 获得该ip信息 
def ipinfo(request):
    ip = request.POST.get('ip','')
    response_data = {}
    response_data['result'] = '0'
    data={}
    data['ip']=ip

    try:
        import sys
        sys.path.append("..")
        from elasticsearchmanage import ipestool
        ips, ipcount, ippagecount = ipestool.ipsearch(dic=data)

        response_data['result'] = '1'
        response_data['ips'] = ips
        response_data['iplength'] = ipcount
        response_data['ippagecount'] = ippagecount
    except Exception,e:
        logger.error("ipestool.ipsearch Error:%s", str(e))
        pass
    try:
        return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict),
                        content_type="application/json")
    except Exception,e:
        logger.error("ipestool.ipsearch Error:%s", str(e))
        return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict, encoding='latin-1'),
                            content_type="application/json")

def map(request):
    username = request.COOKIES.get('username', '')
    latitude = request.GET.get('latitude', '')
    longitude = request.GET.get('longitude', '')
    return render_to_response('fontsearchview/map.html', {'data': '', 'username': username,'latitude':latitude,'longitude':longitude})

def mapsearchmain(request):
    username = request.COOKIES.get('username', '')
    return render_to_response('fontsearchview/mapsearchmain.html',{'username':username})

def mapsearch(request):
    from spidertool import redistool,webtool
    content = request.POST.get('content', '')
    username = request.COOKIES.get('username', '')
    response_data = {}
    response_data['result'] = '0'
    jsoncontent = None
    ports = None
    import json
    try:
        jsonmsg = '{' + content + '}'
        jsoncontent = json.loads(jsonmsg)
    except Exception, e:
        logger.error(e)
        pass

    if jsoncontent is None or jsoncontent =={}:
        redisresult = redistool.get(content)

        if redisresult:
	    logger.debug('Get data from redis.')
            response_data['result'] = '1'

            response_data['ports'] = redisresult['ports']
            response_data['portslength'] = redisresult['portslength']
            response_data['resultsize'] = redisresult['resultsize']
        else:
	    logger.debug('No results in redis.')
            # ports has name and value
            ports, portcount, resultsize = mapcontrol.mapshow(searchcontent=content, isdic=0)

            redisdic={}
            redisdic['ports'] = ports
            redisdic['portslength'] = portcount
            redisdic['resultsize'] = resultsize
            redistool.set(content, redisdic)

            response_data['result'] = '1'
            response_data['ports'] = ports
            response_data['portslength'] = portcount
            response_data['resultsize'] = resultsize

        response_data['username'] = username
    else:
        action = jsoncontent.keys()

        if len(content) == 0:
            return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict),
                                    content_type="application/json")

        redisresult = redistool.get(webtool.md5(str(jsoncontent.__str__)))
        if redisresult:
            logger.debug('Get data from redis.')

            response_data['result'] = '1'
            response_data['ports'] = redisresult['ports']
            response_data['portslength'] = redisresult['portslength']
            response_data['resultsize'] = redisresult['resultsize']
        else:
            ports, portcount, portpagecount = getattr(mapcontrol, 'mapshow', 'mapshow')(**jsoncontent)
            redisdic = {}
            redisdic['ports'] = ports
            redisdic['portslength'] = portcount
            redisdic['resultsize'] = portpagecount
            redistool.set(webtool.md5(str(jsoncontent.__str__)), redisdic)
            response_data['result'] = '1'
            response_data['ports'] = ports
            response_data['portslength'] = portcount
            response_data['resultsize'] = portpagecount

        response_data['username'] = username
    try:
        return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict),
                            content_type="application/json")
    except Exception, e:
        print e
        return HttpResponse(json.dumps(response_data, skipkeys=True, default=webtool.object2dict, encoding='latin-1'),
                            content_type="application/json")



