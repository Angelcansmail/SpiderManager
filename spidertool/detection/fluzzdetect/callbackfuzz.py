#!/usr/bin/env python
# encoding: utf-8

from spidertool import Sqldatatask,Sqldata,SQLTool
import spidertool.config as config

import time,datetime
from termcolor import cprint

import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.163.com"
mail_user = "wlzctc"
mail_pass = "scaneye666"

sender = "wlzctc@163.com"
receivers = ['wlzctc@163.com;18612885987@163.com']
# islocalwork=config.Config.islocalwork

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

def storedata(ip='',port='',disclosures=None):
    sqlTool = Sqldatatask.getObject()
    localtime = str(time.strftime("%Y-%m-%d %X", time.localtime()))
    insertdata = []
     # {'223.223.187.90:8080': [{'status': 200, 'url': '223.223.187.90:8080/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd'}, {'status': 200, 'url': '223.223.187.90:8080/file/Placard/upload/Imo_DownLoadUI.php?cid=1&uid=1&type=1&filename=/../../../../etc/passwd'}, {'status': 200, 'url': '223.223.187.90:8080/resin-doc/resource/tutorial/jndi-appconfig/test?inputFile=/etc/passwd'}, {'status': 200, 'url': '223.223.187.90:8080/wp-config.php~'}, {'status': 200, 'url': '223.223.187.90:8080/'}]}
    # 现在是依次遍历list集合拼接，是否可以直接返回list集合，像hackresults一样
    disclosure = ''
    # for ip_port in disclosures:
    # 	disinfo_list = disclosures[ip_port]
	# for disinfo in disinfo_list:
	#     disclosure += str(disinfo) + '\\n '
#	    disinfo_list.remove(disinfo)

#    print "fuzzey detect callbackfuzz: ", type(disclosures), str(disclosures)   # a dict
    disclosure = SQLTool.escapewordby(str(disclosures))
    extra=' on duplicate key update  disclosure=\''+disclosure+'\' , timesearch=\''+localtime+'\''

    insertdata.append((str(ip),port,disclosure,str(port)))

    sqldatawprk=[]
    dic={"table":config.Config.porttable,"select_params":['ip','port','disclosure','portnumber'],"insert_values":insertdata,"extra":extra}

    tempwprk = Sqldata.SqlData('inserttableinfo_byparams',dic)
    sqldatawprk.append(tempwprk)
    sqlTool.add_work(sqldatawprk)

    from ..vuldect import pocsearchtask
    temp = pocsearchtask.getObject()
    # head,context,ip,port,productname,keywords,nmapscript,protocol
    temp.add_work([(None,None,ip,port,None,None,disclosures,None)])
    pass


def sendemail(host_loc='', mail_msg=''):
    mail_msg += """<br /><br /><p>祝工作、生活愉快！<br/>刚占慧<br />gangzhanhui@163.com</p>"""
    message = MIMEText(mail_msg, 'html', 'utf-8')   # 内容, 格式, 编码
    message['From'] = 'wlzctc@163.com'
    message['To'] =  'wlzctc@163.com;18612885987@163.com'
    subject = now_time + ' ' + host_loc + ' 路径风险预警'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        cprint('Send Email Success.', 'green')
    except smtplib.SMTPException as e:
        cprint('Error: Send Email Failed.' + str(e), 'grey')
