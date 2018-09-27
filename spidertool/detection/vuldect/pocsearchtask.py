#!/usr/bin/python
#coding:utf-8

from spidertool.ThreadTool import ThreadTool
import datetime
import time
from lib.logger import initLog
from spidertool import config,webconfig
from spidertool.TaskTool import TaskTool
import objgraph
import gc
from plugins import default 

pocscantaskinstance=None

def getObject():
    global pocscantaskinstance
    if pocscantaskinstance is None:
        pocscantaskinstance = PocsearchTask(1)
    return pocscantaskinstance

POClog=None

def getloghandle():
    global POClog
    if POClog is None:
        POClog=initLog('logs/POCDect.log', 2, True)
    return POClog

class PocsearchTask(TaskTool):
    def __init__(self,isThread=1,deamon=False):
        TaskTool.__init__(self,isThread,deamon=deamon)
        logger = getloghandle()
        self.set_deal_num(20)
        self.pocscan = default.PocController(logger=logger)

    def task(self,req,threadname):
        print threadname+'POC检测任务启动'+str(datetime.datetime.now())

        head='' if req[0] is None else req[0]
        context='' if req[1] is None else req[1]
	# 202.108.143.152
        ip='' if req[2] is None else req[2]
	# 80
        port='' if req[3] is None else req[3]
	# Apache Tomcat/Coyote JSP engine
        productname='' if req[4] is None else req[4]
	# getgeoipinfo获取到的位置信息
        keywords='' if req[5] is None else req[5]
	# {'http-server-header': 'Apache-Coyote/1.1', 'http-title': '\\xE9\\xA6\\x96\\xE9\\xA1\\xB5--\\xE5\\x8F\\xA4\\xE9\\x9F\\xB5\\xE6\\xAD\\xA3\\xE5\\xA3\\xB0'}
        nmapscript='' if req[6] is None else req[6]
	# http
        protocol='' if req[7] is None else req[7]

        productinfo={}
        productinfo['productname'] = productname
        productinfo['protocol'] = protocol

        print 'POC   未启动内存增长状况'
        gc.collect()
        objgraph.show_growth()
    	# 已经初始化了为啥还要执行？
	# temp = default.PocController(logger=logger)
    	# 为传入defaultpoc参数？
        self.pocscan.detect(head=head, context=context, ip=ip, port=port, productname=productinfo, keywords=keywords, hackinfo=nmapscript)

        print threadname+'POC检测任务结束'+str(datetime.datetime.now())
        print 'POC   内存增长状况'
        gc.collect()
        objgraph.show_growth()
#         print 'objgraph.by_type:',objgraph.by_type('dict')
#         chain = objgraph.find_backref_chain(objgraph.by_type('dict')[-1],inspect.ismodule)
#         objgraph.show_chain(chain,filename='chain.png')
        ans=''

        return ans

if __name__ == "__main__":
    pass




