#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
POC Name  : redis未授权访问
Author    : a
mail      :a@lcx.cc
危害及最新利用： 覆盖ssh密钥root登陆、数据库数据泄露、代码执行、敏感信息泄露
详情：http://www.freebuf.com/vuls/85188.html
"""

from ..miniCurl import Curl
from ..t  import T

import socket
from termcolor import cprint

import socket

class P(T):
    def __init__(self):
        T.__init__(self)

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        result = {}
        result['result']=False

        payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'   # *1\n$4\ninfo
        try:
            s = socket.socket()
            s.connect((ip,int(port)))
            s.send(payload)
            recvdata = s.recv(1024)
            if recvdata and 'redis_version' in recvdata:
                output(ip + ':' + str(port), result, '高危(HOLE)')
            s.close()
        except Exception, e:
    	    cprint(str(e).upper(), 'grey')
            pass
        return result

def output(url,result,label):
    info = url + '  redis  Vul '
    result['result']=True
    result['VerifyInfo'] = {}
    result['VerifyInfo']['type']='redis unauth access Vul'
    result['VerifyInfo']['URL'] =url
    result['VerifyInfo']['payload']='redis unauth access Vul'
    result['VerifyInfo']['level']=label
    result['VerifyInfo']['result'] =info
    cprint(url + '存在未授权访问漏洞', 'red')

if __name__ == '__main__':
    print P().verify(ip='http://yunlai.cn:803/sfdsfds/',port='80')

