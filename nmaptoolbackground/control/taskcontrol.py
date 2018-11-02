#!/usr/bin/python
# -*- encoding: utf-8 -*-

from spidertool import sniffertask, scapytask
import schedule
from datetime import datetime
import time
import logging
import random

logging.basicConfig()#日志基础配置
nmaptask = None
mainschedule = None

#实例化函数
def getObject():
    global nmaptask
    if nmaptask is None:
        nmaptask = sniffertask.snifferTask(1)
        nmaptask.set_deal_num(5)
    return nmaptask

#获取可利用任务
def getavailwork():
    global nmaptask
    if nmaptask is None:
        nmaptask=sniffertask.snifferTask(1)
        nmaptask.set_deal_num(5)
        return ''
    else:
        nmaptask.get_work()

#任务初始化函数
def taskinit():
    global  nmaptask 
    nmaptask= sniffertask.snifferTask(0)
    nmaptask.set_deal_num(5)

#任务添加函数
def taskadd(array):
    global nmaptask 
    if nmaptask is None:
        nmaptask =sniffertask.snifferTask(0)
    nmaptask.add_work(array)

#定时任务添加函数
def addschedule(event, day_of_week='0-6', hour='11',minute='57' ,second='0',id=''):
    global mainschedule
    if mainschedule is None:
        mainschedule = schedule.schedulecontrol()
    mainschedule.addschedule(event,day_of_week,hour,minute,second,id=id)

#定时任务初始化函数
def scheduleinit():
    from spidertool import scapytool 
    import taskitem
#    scapyitem = scapytask.ScapyTask()#被动嗅探
    global mainschedule
    mainschedule = schedule.schedulecontrol()
    # mainschedule.addschedule(event=taskitem.recovertask,type='date')  # 异常宕机恢复
    # mainschedule.addschedule(event=taskitem.normaltask,type='date')  # 后台异步任务

#    mainschedule.addschedule(taskitem.listiptask,'0-6','*/21','13','0',id='listiptask')#自定义扫描段任务器
    mainschedule.addschedule(taskitem.tick,'0-6','02','47','0',id='nmap')#nmap定时任务器
#    mainschedule.addschedule(taskitem.ticknormal,'0-6','0','48','0',id='zmap')#zmap定时任务器
#    mainschedule.addschedule(taskitem.gchelp,'0-6','0-23','0','0',id='gc')#gc collect   
#    mainschedule.addschedule(taskitem.test,'0-6','0-23','34','0',id='test')#gc collect   

    print 'init schedule'


