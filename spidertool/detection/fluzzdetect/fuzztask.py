#!/usr/bin/python
#coding:utf-8
import datetime
import time
from lib.logger import initLog
from spidertool import config, webconfig
from spidertool.TaskTool import TaskTool, ThreadTool
import objgraph
import gc
from fuzzdetect import InfoDisScanner 
fuzzinstance=None

def getObject():
    global fuzzinstance
    if fuzzinstance is None:
        fuzzinstance = FuzzTask(1)
    return fuzzinstance

fuzzlog=None
def getloghandle():
    global fuzzlog
    if fuzzlog is None:
        fuzzlog=initLog('logs/fuzzDect.log', 2, True)
    return fuzzlog

class FuzzTask(TaskTool):
    def __init__(self, isThread=2, deamon=False):
        TaskTool.__init__(self,isThread,deamon=deamon)
        self.set_deal_num(15)
        self.logger = getloghandle()
        self.fuzzscan = InfoDisScanner(logger=self.logger)

    def task(self,req,threadname):
        self.logger and self.logger.info('%sFUZZ检测任务启动%s', threadname,str(datetime.datetime.now()))
        head='' if req[0] is None else req[0]
        context='' if req[1] is None else req[1]
        ip='' if req[2] is None else req[2]
        port='' if req[3] is None else req[3]
        productname='' if req[4] is None else req[4]
        keywords='' if req[5] is None else req[5]
        nmapscript='' if req[6] is None else req[6]
        protocol='' if req[7] is None else req[7]
        print 'poc   未启动内存增长状况'
        gc.collect()
        objgraph.show_growth()
        temp = default.PocController(logger=logger)
        self.logger and self.logger.info('FUZZ检测:   %s:%s,%s',ip,port,protocol)
        self.fuzzscan.scanvul(ip=ip,port=port,protocal=protocol)

#        self.pocscan.detect(head=head, context=context, ip=ip, port=port, productname=productname, keywords=keywords, hackinfo=nmapscript)
        self.logger and self.logger.info('%sFUZZ检测任务结束%s', threadname,str(datetime.datetime.now()))
        print 'poc   内存增长状况'
        gc.collect()
        objgraph.show_growth()
        print 'objgraph.by_type:',objgraph.by_type('dict')
#         chain =objgraph.find_backref_chain(objgraph.by_type('dict')[-1],inspect.ismodule)
#         objgraph.show_chain(chain,filename='chain.png')
        ans=''
        
        return ans

if __name__ == "__main__":
    fuz = getObject()

