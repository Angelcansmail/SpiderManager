#!/usr/bin/env python
# encoding: utf-8
from spidertool import Sqldatatask,Sqldata,SQLTool
import spidertool.config as config

import time
# islocalwork=config.Config.islocalwork

def storedata(ip='',port='',hackresults=None):
    sqlTool=Sqldatatask.getObject()
    localtime=str(time.strftime("%Y-%m-%d %X", time.localtime()))
    insertdata=[]
#     if islocalwork==0:
#         work=[]
#         dic={"table":config.Config.iptable,"select_params": ['ip','vendor','osfamily','osgen','accurate','updatetime','hostname','state'],"insert_values": [(temphosts,tempvendor,temposfamily,temposgen,tempaccuracy,localtime,temphostname,tempstate)]}
#         tempdata={"func":'replaceinserttableinfo_byparams',"dic":dic}
#         jsondata=uploaditem.UploadData(url=self.webconfig.upload_ip_info,way='POST',params=tempdata)
#         work.append(jsondata)
#         self.uploadwork.add_work(work)
                    
#     else:

    hackinfo = ''
    if isinstance(hackresults,str):
	hackinfo = hackresults
    else:
    	for hack in hackresults:
#    	    print '\n\nstoredata', type(hack), str(hack)
    	    if isinstance(hack,dict):
# 有的结果没有存储result，所以使用type进行归类
		hacks = hack['VerifyInfo']
		if 'result' in hacks.keys() and len(hacks['result']) < 150:
		    hackinfo += str({'level':hacks['level'], 'result': hacks['result']}) + '\n '
		else:
		    hackinfo += str({'level':hacks['level'], 'result': hacks['type']}) + '\n '
	    else:
	    	print '\n\nhack is a list but not a dict!!', type(hack)
	        hackinfo += str({'level':'NOTE', 'result':str(hack)}) + '\n '
#	print '\n\nhackinfo',hackinfo
    hackinfo = SQLTool.escapewordby(hackinfo.strip('\n '))
    hackresults = SQLTool.escapewordby(str(hackresults))
    extra=' on duplicate key update hackinfo=\''+hackinfo+'\' , hackresults=\''+hackresults+'\' , timesearch=\''+localtime+'\''

    insertdata.append((str(ip),port,hackinfo,hackresults,str(port)))

    sqldatawprk=[]
    dic={"table":config.Config.porttable,"select_params":['ip','port','hackinfo','hackresults','portnumber'],"insert_values":insertdata,"extra":extra}

    tempwprk=Sqldata.SqlData('inserttableinfo_byparams',dic)
    sqldatawprk.append(tempwprk)
    sqlTool.add_work(sqldatawprk)
    pass

def storeresult(result=None):
    for i in result:
        print '----------------------------------------'
        print '发现漏洞'
        print '位置:'+i['VerifyInfo']['URL']
        print '类型:'+i['VerifyInfo']['type']
        print 'payload:'+i['VerifyInfo']['payload']
    
    return True

