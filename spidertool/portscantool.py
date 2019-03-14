#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import re

import os
import SQLTool
import config
import socket
import traceback

portway = {'sip':'INVITE  world \r\n\r\n','2':'8080','3':'443','4':'22','5':'23'}  

class Portscantool:
    def __init__(self):
        socket.setdefaulttimeout(8)
        self.config = config.Config
        self.socketclient = None

    # portscantask.py中，非正常协议
    # return head, page, keywords, hackinfo, hackresults
    def do_scan(self,head=None,context=None,ip=None,port=None,name=None,productname=None,nmapscript=None):
        keywords = {}
        hackresults = ''
        ans = None
        reply=''
        self.socketclient = None
        try:
            from detection import port_identify
            # port_identify中的函数需要自己补充
            print ("\nportscantool::do_scan(%s:%s)\n"%(ip, port))
            head,ans,keywords,hackresults = port_identify.port_deal(ip=ip,port=port,name=name,productname=productname,head=head,context=context,nmapscript=nmapscript)
	    # 目前都是None
            if ans == None:
                self.socketclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    		self.socketclient.settimeout(15)
    		time.sleep(10)
                self.socketclient.connect((ip,int(port)))
#             message = "GET / HTTP/1.1\r\nHost: oschina.net\r\n\r\n"
                message =portway.get(name,"GET  world \r\n\r\n")
                if self.socketclient:
                    self.socketclient.sendall(message)
                else:
                    self.socketclient=  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socketclient.connect((ip,int(port)))
                reply = self.socketclient.recv(4096)

                return '',reply,keywords,hackresults
#                return 'sock reply info:  ',reply,keywords,hackresults,hackresults
            else:
                return '',ans,keywords,hackresults
#                return 'Sock reply info:  ',ans,keywords,hackresults,hackresults
	except Exception, msg:
            print 'Failed to create socket. Error code: ' + str(msg) + ' Error info: ' + str(traceback.print_exc())
            return str(msg), 'SOCKET Error!',keywords,hackresults
#	    return 'Error info:','Error',keywords,hackresults
        finally:
            if self.socketclient is not None:
                self.socketclient.close()
   
if __name__ == "__main__":
    temp = Portscantool()
    temp.do_scan(ip='118.25.43.205', port='3306')
#     temp.do_scan('218.106.87.35', '110')
