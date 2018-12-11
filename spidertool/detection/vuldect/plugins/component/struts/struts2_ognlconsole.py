#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
POC Name  :  OGNL console
Author    :  a
mail        :  a@lcx.cc
Referer:	http://wooyun.org/bugs/wooyun-2010-080076
"""

import urlparse
from termcolor import cprint
from ..miniCurl import Curl
from ..t import T

class P(T):
    def __init__(self):
        T.__init__(self)

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        arg='http://'+ip+':'+port
        print arg
        curl=Curl()
        result = {}
        result['result']=False

        # 如果存在了webconsole.html页面,则判断系统存在Struts2漏洞
	    # webconsole.html为了方便开发人员进行Debug而提供的功能, 只有在调试模式下才能使用
	    # <constant name="struts.devMode" value="true" />
	    # webconsole.html页面与后端交互时,使用了Dojo的js框架来完成请求和应答处理,
	    # 所以webconsole.html页面可以与后端进行正常交互的前提是,项目中使用了Dojo的lib库
        # 只有在开启了Debug模式且ClassPath中使用了struts2-dojo-plugin-*.jar的情况下,webconsole.html页面才有可能存在安全漏洞的风险。
        payload = '/struts/webconsole.html'
        url = arg + payload

        code, head, res, errcode, _ = curl.curl('"%s"' % url)
#    	print "code:%s,head:%s,res:%s,errcode:%s"%(code, head, res, errcode)
        if code == 200 and "Welcome to the OGNL console" in res:
            cprint(url + '存在structs ognl console漏洞', 'red')
            output('find ognl console:' +url,result,'info')
        del curl
        return result

def output(url,result,label):
    info = url + '  struts  Vul '
    result['result']=True
    result['VerifyInfo'] = {}
    result['VerifyInfo']['type']='struts Vul'
    result['VerifyInfo']['URL'] =url
    result['VerifyInfo']['payload']='/root/github/poccreate/thirdparty/www/www_38ab66d936ba162d25c98c1af6623f7c.py'
    result['VerifyInfo']['level']=label
    result['VerifyInfo']['result'] =info

if __name__ == '__main__':
    print P().verify(ip='202.108.143.152',port='80')

#/root/github/poccreate/thirdparty/www/www_38ab66d936ba162d25c98c1af6623f7c.py
#/root/github/poccreate/codesrc/exp-745.py
