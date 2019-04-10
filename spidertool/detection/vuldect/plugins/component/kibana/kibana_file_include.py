#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/12/25 13:36
@Author  : gzh
@contact : k39aE465wlulvnkhT0i9MQ==@qq.com
@Site    : https://www.anquanke.com/post/id/168291?from=timeline&isappinstalled=0
@File    : kibana_file_include.py
@Desc    : Elasticsearch Kibana 6.4.3之前版本和5.6.13之前版本中的Console插件存在严重的本地文件包含漏洞可导致拒绝服务攻击、任意文件读取攻击、配合第三方应用反弹SHELL攻击, CVE-2018-17246
@Software: PyCharm
"""


from ..t import T
from ..miniCurl import Curl
import re
from termcolor import cprint
from distutils.version import LooseVersion

class P(T):
    def __init__(self):
        T.__init__(self)

    def verify(self, head='', context='', ip='', port='', productname={}, keywords='', hackresults=''):
        if port=='443':
            protocal = 'https://'
        else:
            protocal = 'http://'

        url = protocal + ip + ':' + port + '/'
        # curl = Curl()
        result = {}
        result["result"] = False

        # code, head, body, error, _ = curl.curl(url)
        print "kibana_file_include detect head", head
        m = re.findall(r'kbn-version:.*', head)
        if m:
            version_info = m[0] # kbn-version: 5.6.4
            print version_info
            version = version_info[version_info.index('kbn-version: ') + 13: ]

            if LooseVersion(version) > LooseVersion('5.0') and LooseVersion(version) < LooseVersion('5.6.13') or LooseVersion(version) > LooseVersion('6.0') and LooseVersion(version) < LooseVersion('6.4.3'):
                cprint(url + "存在信息泄漏风险", "red")
                output(url, result, "高危(HOLE)")
        # del curl
        return result


def output(url,result,label):
    info = url + ' kibana arbitrary file inclusion(CVE-2018-17246)'
    result["result"] = True
    result["VerifyInfo"] = {}
    result["VerifyInfo"]["type"] = "arbitrary file inclusion"
    result["VerifyInfo"]["URL"] = url
    result["VerifyInfo"]["payload"] = "/component/kibana/kibana_file_include.py"
    result["VerifyInfo"]["level"] = label
    result["VerifyInfo"]["result"] = info


if __name__ == '__main__':
    print P().verify(ip='47.100.220.4', port='5601')
    # 52.82.23.34,62.234.136.76,219.142.70.212,219.142.70.212,139.198.13.163,47.100.220.4