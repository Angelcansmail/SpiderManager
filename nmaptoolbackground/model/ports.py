#!/usr/bin/python
#coding:utf-8


from spidertool import webtool
from location import Location
import ast

class Port(object):
    def __init__(self,ip='',port='',timesearch='',state='',name='',product='',version='',script='',detail='',head='',city='',hackinfo='',hackresults=None,disclosure=None,geoinfo=None,webtitle='',webkeywords=''):
        '''
            Constructor
        '''
        self.ip=ip
        self.port=port
        self.version=version
        self.state=state
        self.name=name
        if timesearch!='':
            self.timesearch=timesearch
        else:
            self.timesearch=webtool.getlocaltime()

        self.product=product
        self.script=script
        self.detail=detail
        self.head=head
        self.city=city
        self.hackinfo = hackinfo
        self.hackresults = hackresults
        self.disclosure = disclosure
        self.geoinfo = geoinfo
        self.webkeywords = webkeywords
        self.webtitle = webtitle

        if self.geoinfo is None:
            self.geoinfo = Location(ip=str(self.ip)).getData()
        else:
            try:
                data = eval(geoinfo)
                self.geoinfo = data
                if self.geoinfo.get('geoip',None) is None:
                    self.geoinfo = Location(ip=str(self.ip)).getData()
            except Exception, e:
                self.geoinfo = Location(ip=str(self.ip)).getData()
            # print self.geoinfo
            # print self.geoinfo['geoip']['country']

        try:
            # print("ports detect hackresults", type(hackresults), len(hackresults), str(hackresults))
            if self.hackresults is not None and self.hackresults != '':
                self.hackresults = ast.literal_eval(hackresults)
                # print "ports detect hackresults.", type(self.hackresults), str(self.hackresults)
            # print "ports detect disclosure.", (type(disclosure)), len(disclosure), disclosure
            if self.disclosure is not None:
                self.disclosure = ast.literal_eval(disclosure)
                # print "ports detect disclosure.", type(self.disclosure), str(self.disclosure)
        except Exception, e:
            print "ports trans hackresults and disclosures error: ", str(e)

    def getIP(self):
        return self.ip
    def getPort(self):
        return self.port
    def getVersion(self):
        return self.version
    def getState(self):
        return self.state
    def getName(self):
        return self.name
    def getTime(self):
        return self.timesearch
    def getProduct(self):
        return self.product 
    def getScript(self):
        return self.script
    def getHead(self):
        return self.head
