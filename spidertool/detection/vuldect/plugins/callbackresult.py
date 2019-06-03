#!/usr/bin/env python
# encoding: utf-8
from spidertool import Sqldatatask,Sqldata,SQLTool
import spidertool.config as config

import time
import datetime

from termcolor import cprint

import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.163.com"
mail_user = "wlzctc"
mail_pass = "scaneye666"

sender = "wlzctc@163.com"
receivers = ['wlzctc@163.com;18612885987@163.com']
# receivers = ['gangzhanhui@163.com','18612885987@163.com','1751583392@qq.com']

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

# islocalwork=config.Config.islocalwork

def storedata(ip='',port='',hackresults=None):
    sqlTool=Sqldatatask.getObject()
    localtime=str(time.strftime("%Y-%m-%d %X", time.localtime()))
    insertdata=[]
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

def sendemail(host_loc='', mail_msg=''):
    mail_msg += """<br /><br /><p>祝工作、生活愉快！<br/>刚占慧<br />gangzhanhui@163.com</p>"""
    message = MIMEText(mail_msg, 'html', 'utf-8')   # 内容, 格式, 编码
    # message['From'] = Header("网络资产安全性检测系统", 'utf-8')
    # message['To'] =  Header('XX安全实验室', 'utf-8')
    message['From'] = 'wlzctc@163.com'
    message['To'] =  'wlzctc@163.com;18612885987@163.com'
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
