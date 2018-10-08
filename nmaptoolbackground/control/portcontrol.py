#!/usr/bin/python
#coding:utf-8
from spidertool import SQLTool ,config
from ..model import ports
import re

limitpage=15
DBhelp=None

# searchroute::detailpage传入page, extra, command='or'
def portabstractshow(ip='',port='',timesearch='',state='',name='',product='',version='',script='',detail='',page='0',extra='',command='and',head='',city='',hackinfo='',hackresults='',disclosure=''):
    localconfig = config.Config()
    table = localconfig.porttable   #snifferdata
    iptable = localconfig.iptable   #ip_maindata
    validresult = False
    request_params = []
    values_params = []

    if ip != '':
        request_params.append(table+'.'+'ip')
        values_params.append(SQLTool.formatstring(ip))
    if port != '':
        request_params.append('port')
        values_params.append(SQLTool.formatstring(port))
    if timesearch != '':
        request_params.append('timesearch')
        values_params.append(SQLTool.formatstring(timesearch))
    if state != '':
        request_params.append(table+'.'+'state')
        values_params.append(SQLTool.formatstring(state))
    if name != '':
        request_params.append('name')
        values_params.append(SQLTool.formatstring(name))
    if product != '':
        request_params.append('product')
        values_params.append(SQLTool.formatstring(product))
    if version != '':
        request_params.append('version')
        values_params.append(SQLTool.formatstring(version))
    if script != '':
        request_params.append('script')
        values_params.append(SQLTool.formatstring(script))
    if detail != '':
        request_params.append('detail')
        values_params.append(SQLTool.formatstring(detail))
    if head != '':
        request_params.append('head')
        values_params.append(SQLTool.formatstring(head))
    if city != '':
        request_params.append('city')
        values_params.append(SQLTool.formatstring(city))
    global DBhelp

    DBhelp=SQLTool.DBmanager()
    DBhelp.connectdb()
    
    content = None
    result = None
    try:
        result,content,count,col=DBhelp.searchtableinfo_byparams([table+' left join ip_maindata on snifferdata.ip=ip_maindata.ip'], ['count(*)'], request_params, values_params,extra=extra,command=command)
    except Exception,e:
        print str(e)+'portcontrol 58'
        if DBhelp is not None:
            DBhelp.closedb()
            DBhelp=None
        return [], 0, 0
    if count>0:
        count= int(result[0]['count(*)'])
    if count == 0:
        pagecount = 0;
    elif count %limitpage> 0:
        pagecount=int((count+limitpage-1)/limitpage) 
    else:
        pagecount = count / limitpage

#     print pagecount
    if pagecount>0:
        limit = ' limit '+str(int(page)*limitpage)+','+str(limitpage)
        try:
            result, content, count, col = DBhelp.searchtableinfo_byparams([table + ' left join ip_maindata on snifferdata.ip=ip_maindata.ip'], [table+'.'+'ip','port','timesearch',table+'.'+'state','name','product','version','script','detail','head','city','hackinfo','hackresults','disclosure'], request_params, values_params,limit=limit,order=table+'.'+'port',extra=extra,command=command)
        except Exception,e:
            print str(e) + 'portcontrol 69'
            if DBhelp is not None:
                DBhelp.closedb()
            return [],0,0
        if DBhelp is not None:
                DBhelp.closedb()
                DBhelp=None
            
        portarray=[]
        if count > 0:
            validresult=True
            import  base64
            for temp in result :
                aport=ports.Port(ip=temp['ip'],port=temp['port'],timesearch=temp['timesearch'],state=temp['state'],name=temp['name'],product=temp['product'],version=temp['version'],script=base64.b64encode(SQLTool.getdecodeproperty(temp,'script')),detail=SQLTool.getdecodeproperty(temp,'detail'),head=SQLTool.getdecodeproperty(temp,'head'),city=temp['city'],hackinfo=SQLTool.getdecodeproperty(temp,'hackinfo'),hackresults=SQLTool.getdecodeproperty(temp,'hackresults'),disclosure=SQLTool.getdecodeproperty(temp,'disclosure'))

#                 aport=ports.Port(ip=temp[0],port=temp[1],timesearch=temp[2],state=temp[3],name=temp[4],product=temp[5],version=temp[6],script=temp[7])
                portarray.append(aport)
        print str(count)+' '+str(pagecount)
        return portarray,count,pagecount
    return [],0,pagecount

def portshow(ip='',port='',timesearch='',state='',name='',product='',version='',script='',detail='',page='0',extra='',command='and',head='',city='',order='port'):
    validresult=False
    request_params=[]
    values_params=[]

    # 默认ip/page/extra都会传过来(一些端口的限制)
    if ip != '':
        request_params.append('ip')
        values_params.append(SQLTool.formatstring(ip))
    if port != '':
        request_params.append('port')
        values_params.append(SQLTool.formatstring(port))
    if timesearch != '':
        request_params.append('timesearch')
        values_params.append(SQLTool.formatstring(timesearch))
    if state != '':
        request_params.append('state')
        values_params.append(SQLTool.formatstring(state))
    if name != '':
        request_params.append('name')
        values_params.append(SQLTool.formatstring(name))
    if product != '':
        request_params.append('product')
        values_params.append(SQLTool.formatstring(product))
    if version != '':
        request_params.append('version')
        values_params.append(SQLTool.formatstring(version))
    if script != '':
        request_params.append('script')
        values_params.append(SQLTool.formatstring(script))
    if detail != '':
        request_params.append('detail')
        values_params.append(SQLTool.formatstring(detail))
    if head != '':
        request_params.append('head')
        values_params.append(SQLTool.formatstring(head))
    if city != '':
        request_params.append('city')
        values_params.append(SQLTool.formatstring(city))

    global DBhelp
    DBhelp = SQLTool.DBmanager()
    DBhelp.connectdb()
    localconfig = config.Config()
    table = localconfig.porttable #snifferdata
    content = None
    result=None

    try:
        result, content, count, col = DBhelp.searchtableinfo_byparams([table], ['count(*)'], request_params, values_params, extra=extra, command=command)
    except Exception,e:
        print str(e) + 'portcontrol 50'
        if DBhelp is not None:
            DBhelp.closedb()
            DBhelp=None
        return [], 0, 0
    if count > 0:
        count= int(result[0]['count(*)'])

    if count == 0:
        pagecount = 0;
    elif count %limitpage> 0:
#        pagecount = math.ceil(count / limitpage)
        pagecount=int((count+limitpage-1)/limitpage) 
    else:
        pagecount = count / limitpage
#    print pagecount

    if pagecount > 0:
        limit = ' limit ' + str(int(page)*limitpage) + ',' + str(limitpage)
        try:
            result, content, count, col=DBhelp.searchtableinfo_byparams([table], ['ip','port','timesearch','state','name','product','version','script','detail','head','hackinfo','hackresults'], request_params, values_params,limit,order=order,extra=extra,command=command)
        except Exception,e:
            print str(e) + ' portcontrol 69'
            if DBhelp is not None:
                DBhelp.closedb()
            return [],0,0
        if DBhelp is not None:
                DBhelp.closedb()
                DBhelp=None
            
        portarray=[]
        if count > 0:
            validresult=True
            for temp in result :
                aport = ports.Port(ip=SQLTool.getdecodeproperty(temp,'ip'),port=temp['port'],timesearch=temp['timesearch'],state=temp['state'],name=temp['name'],product=temp['product'],version=temp['version'],script=SQLTool.getdecodeproperty(temp,'script'),detail=SQLTool.getdecodeproperty(temp,'detail'),head=SQLTool.getdecodeproperty(temp,'head'),hackinfo=temp['hackinfo'],hackresults=temp['hackresults'])
#                 aport=ports.Port(ip=temp[0],port=temp[1],timesearch=temp[2],state=temp[3],name=temp[4],product=temp[5],version=temp[6],script=temp[7])
                portarray.append(aport)
        return portarray, count, pagecount
    return [], 0, pagecount
##count为返回结果行数，col为返回结果列数,count,pagecount都为int型

def portadd(port):
    ip=port.getIP()
    port=port.getVendor()
    timesearch=port.getOsfamily()
    state=port.getState()
    name=port.getOsgen()
    product=port.getUpdatetime()
    version=port.getAccurate()
    script=port.getHostname()

    request_params=[]
    values_params=[]
    if ip != '':
        request_params.append('ip')
        values_params.append(SQLTool.formatstring(ip))
    if port != '':
        request_params.append('port')
        values_params.append(SQLTool.formatstring(port))
        request_params.append('portnumber')
        values_params.append(SQLTool.formatstring(port))
    if timesearch != '':
        request_params.append('timesearch')
        values_params.append(SQLTool.formatstring(timesearch))
    if state != '':
        request_params.append('state')
        values_params.append(SQLTool.formatstring(state))
    if name != '':
        request_params.append('name')
        values_params.append(SQLTool.formatstring(name))
    if product != '':
        request_params.append('product')
        values_params.append(SQLTool.formatstring(product))
    if version != '':
        request_params.append('version')
        values_params.append(SQLTool.formatstring(version))
    if script != '':
        request_params.append('script')
        values_params.append(SQLTool.formatstring(script))
    if detail != '':
        request_params.append('detail')
        values_params.append(SQLTool.formatstring(detail))  
    if head != '':
        request_params.append('head')
        values_params.append(SQLTool.formatstring(head))      
    table=localconfig.porttable
    DBhelp=SQLTool.DBmanager()
    DBhelp.connectdb()
    tempresult=None
    try:
        tempresult=DBhelp.replaceinserttableinfo_byparams(table, request_params, [tuple(values_params)])
    except Exception,e:
        print str(e)
    finally:
        if DBhelp is not None:
            DBhelp.closedb()
    return tempresult

def divided(ports, params='port'):
    if ports == '':
        return ''
    sql = ' and ( '
    array = ports.split(',')

    for i in range(len(array)-1):
        resulto = re.match(r"^(\d*)\-(\d*)$",array[i]) 

        if resulto:  
            p = re.compile(r'\d+')
            port_list = p.findall(array[i])
            sql += params + ' between ' + SQLTool.formatstring(port_list[0]) + ' and ' + SQLTool.formatstring(port_list[1]) + ' or '
        else:
            p = re.compile(r'\d+$')
            port_list = p.findall(array[i])
            sql += params + '=' + SQLTool.formatstring(port_list[0]) + ' or '
    temp = array[len(array)-1]
    resulto = re.match(r"^(\d*)\-(\d*)$", temp) 

    if resulto: 
        p = re.compile(r'\d+')
        port_list = p.findall(temp)
        sql += params+' between ' + SQLTool.formatstring(port_list[0]) + ' and ' + SQLTool.formatstring(port_list[1])+')'
    else:
        p = re.compile(r'\d+$')
        port_list = p.findall(temp)
        sql += params + '=' + SQLTool.formatstring(port_list[0]) + ')'
    return sql

def port_info_upload(temphosts,tempvendor,temposfamily,temposgen,tempaccuracy,localtime,temphostname,tempstate):
#     sqldatawprk=[]
#     dic={"table":self.config.iptable,"select_params": ['ip','vendor','osfamily','osgen','accurate','updatetime','hostname','state'],"insert_values": [(temphosts,tempvendor,temposfamily,temposgen,tempaccuracy,localtime,temphostname,tempstate)]}
#     tempwprk=Sqldata.SqlData('replaceinserttableinfo_byparams',dic)
#     sqldatawprk.append(tempwprk)
#     self.sqlTool.add_work(sqldatawprk)
    pass 
    
#             print 'there is no any thing match'
if __name__ == "__main__":   
    sql=divided('120-234,t765,t4')
    print sql

    
    
