# !/usr/bin/env python
# -*- coding:utf-8 -*-
from spidertool import masscantool,zmaptool,iptask,sniffertask,SQLTool
import random
from datetime import datetime
import taskscontrol, jobcontrol
import objgraph
# import pdb

operator = {'1':'80','2':'8080','3':'443','4':'22','5':'21', '6': '3306', '7':'873', '8':'7547', '9':'9200'}

def test():
    print('Tick! The time is: %s' % datetime.now())

def tick():
    gchelp()
    print("\n\nsniffertask count:%d"%(sniffertask.getObject().get_length()))
#    pdb.set_trace()
    if sniffertask.getObject().get_length()>50:
        print('Too much work: %s' % datetime.now())
        pass
    else:
        num = random.randint(1,9)
        # temp = zmaptool.getObject()
#        print (str(num), "init masscantool object.")
        temp = masscantool.getObject()
#        print ("masscan do scan.")
        temp.do_scan(port=operator.get(str(num)),num='50',needdetail='1')
    print('Tick! The time is: %s' % datetime.now())

def ticknormal():
    num=random.randint(1, 1)
    temp=zmaptool.getObject()
    # temp=masscantool.getObject()
    temp.do_scan(port=operator.get(str(num)),num='30')

def gchelp():
    import gc
    gc.collect()
    print('Tick! The time is: %s' % datetime.now())

def listiptask():
    listitem=iptask.getObject()
    listitem.add_work([('172.20.13.11','172.20.13.12')])
    print '自定义任务已经启动'

def recovertask():
    print '异常恢复任务启动'
    tasks, count, pagecount=taskscontrol.taskshow(tasktatus='1')
    if count>0:
        print '寻找未启动的任务'
        for item in tasks:
            item.setMode(0)
            temp = taskscontrol.createjob(item)

    tasks, count, pagecount=taskscontrol.taskshow(tasktatus='3')
    if count>0:
        print '寻找正在执行的任务'
        for item in tasks:
            item.setMode(0)
            taskscontrol.startjob(item)

def normaltask():
    info = {}

    info['isjob'] = '0'
    info['command'] = 'work'
    listitem=iptask.getObject()
    listitem.add_work([('1.1.1.1','254.254.254.254',info)])

    pass
