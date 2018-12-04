#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2
import json

def getGeoipinfo(data):
    print "httpdect::webdection::getGeoipinfo(%s)..."% data
#   组成查询ip地理位置的网址，返回字典格式在前端fontsearch/detailmapview.html展示
    url = 'http://ip-api.com/json/%s' % (data)
#    url = 'http://ip-api.com/json/%s' % (data['ip'][0])
#   访问url地址, urlobject是<type 'instance'>对象
#   设置超时时间，否则会假死
    urlobject = urllib2.urlopen(url, timeout=3)
    urlcontent = urlobject.read()

    '''
	{"as":"AS17964 Beijing Dian-Xin-Tong Network Technologies Co., Ltd.","city":"Beijing","country":"China","countryCode":"CN","isp":"China Telecom Beijing","lat":39.904,"lon":116.408,"org":"Beijing Dian-Xin-Tong Network Technologies Co.","query":"115.182.9.230","region":"11","regionName":"Beijing Shi","status":"success","timezone":"Asia/Shanghai","zip":""}
    '''
    # url地址访问后的返回值；urlcontent类型为字符串；
    # urlcontent = '{
    #   "ip":"172.25.254.250","country_code":"","country_name":"",
    #   "region_code":"","region_name":"","city":"","zip_code":"",
    #   "time_zone":"","latitude":0,"longitude":0,"metro_code":0
    #   }'
    # latitude: 纬度
    # longitude： 经度

    # 很明显字符串的信息不好处理的， 那么json模块可以帮忙的；
    res = json.loads(urlcontent)
    countryname=''
    cityname=''
    organization=''
    subdivisionnames=''
    Longitude = str(res['lon'])
    Latitude = str(res['lat'])
    countryName = res['country']
    countryCode = res['countryCode']
    cityname = res['city']
    isp = res['isp']
    organization = res['org']
    keywords = {'geoip':{'country':{'name':countryName,'code':countryCode},'city':{'name':cityname},'isp':{'organization':organization},'subdivisions':{'names':subdivisionnames},'location':{'longitude':Longitude,'latitude':Latitude}}}
    # 直接返回的是字典，不用转为字符串，后续还要调用其中的字段
#    keywords = json.dumps(keywords, sort_keys=True, indent=4, separators=(',', ': '))
    return keywords
