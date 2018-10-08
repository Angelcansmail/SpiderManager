#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import os,sys

error = ['404', 'Not Found', 'Safedog', '找不到', '安全狗', '无权访问', '403']

from ..t import T
from termcolor import cprint

reload(sys)
sys.setdefaultencoding('utf8')

class P(T):
    def __init__(self):
	T.__init__(self)

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    	result = {}
	result['result'] = False
	
	headers = {
	    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
	path = '/ws_utc/config.do'
	url = 'http://' + ip + path

	try:
            reques = requests.get(url=url, headers=headers, allow_redirects=False, timeout=3)

            for e in error:
                if reques.status_code == 200 and e not in reques.text:
                    pd = '[+]debug url:{}'.format(url)
		    cprint(url + '存在weblogic CVE-2018-2894漏洞', 'red')
		    output(url, result, 'hole')
		    break
	    return result
        except Exception, e:
	    print e
            pass

def output(url,result,label):
    info = url + ' has CVE-2018-2894 weblogic  Vul '
    result['result']=True
    result['VerifyInfo'] = {}
    result['VerifyInfo']['type']='weblogic Vul'
    result['VerifyInfo']['URL'] =url
    result['VerifyInfo']['payload']='/root/github/poccreate/thirdparty/weblogic/weblogic2894.py'
    result['VerifyInfo']['level']=label
    result['VerifyInfo']['result'] =info

    return result

if __name__=="__main__":
    print P().verify(ip=sys.argv[1])
