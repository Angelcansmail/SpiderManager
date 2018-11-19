#!/usr/bin/env python
# encoding: utf-8

from spidertool import Sqldatatask,Sqldata,SQLTool
import spidertool.config as config

import time
# islocalwork=config.Config.islocalwork

def storedata(ip='',port='',hackresults=None):
    sqlTool = Sqldatatask.getObject()
    localtime = str(time.strftime("%Y-%m-%d %X", time.localtime()))
    insertdata = []
#     if islocalwork==0:
#         work=[]
#         dic={"table":config.Config.iptable,"select_params": ['ip','vendor','osfamily','osgen','accurate','updatetime','hostname','state'],"insert_values": [(temphosts,tempvendor,temposfamily,temposgen,tempaccuracy,localtime,temphostname,tempstate)]}
#         tempdata={"func":'replaceinserttableinfo_byparams',"dic":dic}
#         jsondata=uploaditem.UploadData(url=self.webconfig.upload_ip_info,way='POST',params=tempdata)
#         work.append(jsondata)
#         self.uploadwork.add_work(work)
#     else:

    disclosure = ''
    for ip_port in hackresults:
    	disinfo_list = hackresults[ip_port]
	for disinfo in disinfo_list:
	    disclosure += str(disinfo) + '\\n '
#	    disinfo_list.remove(disinfo)
    disclosure = SQLTool.escapewordby(disclosure)
#    hackresults = SQLTool.escapewordby(str(hackresults))
    extra=' on duplicate key update  disclosure=\''+disclosure+'\' , timesearch=\''+localtime+'\''

    insertdata.append((str(ip),port,disclosure,str(port)))

    sqldatawprk=[]
    dic={"table":config.Config.porttable,"select_params":['ip','port','disclosure','portnumber'],"insert_values":insertdata,"extra":extra}

    tempwprk = Sqldata.SqlData('inserttableinfo_byparams',dic)
    sqldatawprk.append(tempwprk)
    sqlTool.add_work(sqldatawprk)

    print 'fuzz 转poc检测'
    from ..vuldect import pocsearchtask
    temp = pocsearchtask.getObject()
    # head,context,ip,port,productname,keywords,nmapscript,protocol
    temp.add_work([(None,None,ip,port,None,None,hackresults,None)])
    print 'fuzz 数据存储调用'
    pass


