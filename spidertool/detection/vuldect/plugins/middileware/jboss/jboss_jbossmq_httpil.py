#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
CVE-2017-7504
'''
import sys
import requests
from ..t import T
from termcolor import cprint

class P(T):
    def __init__(self):
        T.__init__(self)

    def verify(self,head='',context='',ip='',port='8080',productname={},keywords='',hackresults=''):
        timeout=3
        target_url = 'http://'+ip+':'+port
        result = {}
        result['result'] = False

        vul_url = target_url + '/jbossmq-httpil/HTTPServerILServlet'
        res=None
        try:
            res=requests.get(vul_url)
            res_sta = res.status_code
        except:
            return result
        finally:
            if res is not None:
                res.close()
                del res
        if res_sta == 200 and "This is the JBossMQ HTTP-IL" in res.content:
            cprint(vul_url + " 存在CVE-2017-7504反序列化漏洞", 'red')
            info = vul_url + " CVE-2017-7504 Vul"
            result['result']=True
            result['VerifyInfo'] = {}
            result['VerifyInfo']['type'] = 'Java serialization.'
            result['VerifyInfo']['URL'] = target_url
            result['VerifyInfo']['payload'] = vul_url
            result['VerifyInfo']['result'] = info
            result['VerifyInfo']['level'] = '高危(HOLE)'
        return result


if __name__ == '__main__':
    print P().verify(sys.argv[1], sys.argv[2])      
