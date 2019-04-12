#!/usr/bin/env python
# encoding: utf-8
from spidertool import Sqldatatask,Sqldata,SQLTool
import spidertool.config as config

import time
import datetime
import smtplib

from termcolor import cprint
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.163.com"
mail_user = "gangzhanhui"
mail_pass = "Angel123"

sender = "gangzhanhui@163.com"
receivers = ['gangzhanhui@163.com']

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

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

    # hackinfo = ' '
#     if isinstance(hackresults,str):
# 	hackinfo = hackresults
#     else:
#     	for hack in hackresults:
# #    	    print '\n\nstoredata', type(hack), str(hack)
#     	    if isinstance(hack,dict):
# # 有的结果没有存储result，所以使用type进行归类
# 		hacks = hack["VerifyInfo"]
# 		print '\n\nstoredata', hacks
# 		if "result" in hacks.keys() and len(hacks["result"]) < 150:
# 		    hackinfo += str({"level":hacks["level"], "result": hacks["result"]}) + '\\n'
# 		else:
# 		    hackinfo += str({"level":hacks["level"], "result": hacks["type"]}) + '\\n'
# 	    else:
# 	    	print '\n\nhack is a list but not a dict!!', type(hack)
# 	        hackinfo += str({"level":"NOTE", "result":str(hack)}) + '\\n'
# 	print '\n\nhackinfo',hackinfo
#     hackinfo = SQLTool.escapewordby(hackinfo.strip('\\n'))
    hackresults = SQLTool.escapewordby(str(hackresults))
    extra=' on duplicate key update hackresults=\''+hackresults+'\' , timesearch=\''+localtime+'\''

    insertdata.append((str(ip),port,hackresults,str(port)))

    sqldatawprk=[]
    dic={"table":config.Config.porttable,"select_params":['ip','port','hackresults','portnumber'],"insert_values":insertdata,"extra":extra}

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

# def sendemail(level, mail_msg=''):
def sendemail(host_loc='', mail_msg=''):
    message = MIMEText(mail_msg, 'html', 'utf-8')   # 内容, 格式, 编码
    message['From'] = Header("网络资产安全性探测系统", 'utf-8')
    message['To'] =  Header('XX安全实验室', 'utf-8')
    subject = now_time + ' ' + host_loc + ' 风险预警'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        cprint('Send Email Success.', 'green')
    except smtplib.SMTPException as e:
        cprint('Error: Send Email Failed.' + str(e), 'grey')
