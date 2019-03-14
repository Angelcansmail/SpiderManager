#!/usr/bin/python
#coding:utf-8
try:
    from spidertool.detection.httpdect.webdection import getgeoipinfo
except:
    pass

class Location(object):
    def __init__(self,ip=None):
        data={}
        data['ip']=[ip]
        from spidertool import redistool
        redisresult = redistool.get(ip)
        if redisresult:
            self.data = redisresult
        else:
            geoipinfo=''
            try:
                geoipinfo = getgeoipinfo.getGeoipinfo(ip)
            except:
                pass
            redistool.set(ip, geoipinfo)
            self.data = geoipinfo

    def getData(self):
        return self.data
