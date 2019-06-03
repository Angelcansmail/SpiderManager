#!/usr/bin/python
#coding:utf-8
import time
import re
from subprocess import Popen, PIPE
import os
import SQLTool
import config,portscantask
from nmaptoolbackground.control import taskcontrol
from nmaptoolbackground.model import job
import Sqldatatask
import Sqldata
import   trace 
import getLocationTool
import sniffertask

zmapinstance=None

def getObject():
    global zmapinstance
    if zmapinstance is None:
        zmapinstance = Zmaptool()
    return zmapinstance

class Zmaptool:
    def __init__(self):
        self.sqlTool = Sqldatatask.getObject()  # init DB
        self.config = config.Config
        self.portscan = portscantask.getObject()
        self.getlocationtool = getLocationTool.getObject()

    def do_scan(self, port='8080', num='10', needdetail='0'):
        path = os.getcwd()
        locate = os.path.split(os.path.realpath(__file__))[0]
        ip_list = open(locate+"/ip.txt").readlines()

        if True:
            localtime = str(time.strftime("%Y-%m-%d %X", time.localtime()))
            for i in ip_list:
                self.getlocationtool.add_work([str(i).strip()]) # save ip info(get from ip.taobao.com) to ip_maindata

if __name__ == "__main__":
    temp = Zmaptool()
    temp.do_scan(needdetail='1')

