#!/usr/bin/python
#coding:utf-8

'''
Created on 2015年10月29日

@author: sherwel
'''

import sys
import nmap   
import os
import time
import SQLTool
import Sqldatatask
import config
import Sqldata

import connectpool
import portscantask
import getLocationTool

import traceback

reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   

class SniffrtTool(object):
    '''
    classdocs
    '''
    def __init__(self,logger=None):
        '''
        Constructor
        '''
        self.logger = logger
        try:
            self.nma = nmap.PortScanner()     # instantiate nmap.PortScanner object
#            self.params='-A -sC -R -v -O -T5 '
            self.params='-sV -T4 -Pn -O '         #快捷扫描加强版
#             self.params='-sS -sU -T4 -A -v '   #深入扫描
        except nmap.PortScannerError:
            self.logger.info('Nmap not found:%s',sys.exc_info()[0])
        except:
            self.logger.info('Unexpected error:%s',sys.exc_info()[0])

        self.config = config.Config
        self.sqlTool = Sqldatatask.getObject()  # init DBmanager, and connect database and thread number
        self.portscan = portscantask.getObject()    #设置一些网络参数配置, 查看portScantask.log
        # init DBmanager and thread number
        self.getlocationtool = getLocationTool.getObject()

    def scaninfo(self,hosts='localhost', port='', arguments='',hignpersmission='0',callback=''):
        if callback == '': 
            callback = self.callback_result
        orders = ''
        if port != '':
            orders += port	#为什么要加，直接使用port不一样吗，都是一个port
        else :
            orders = None
        try:
            if hignpersmission == '0':
                acsn_result = self.nma.scan(hosts=hosts,ports=orders,arguments=self.params+arguments)
                self.logger.info("扫描结束%s:%s\n%s\n"%(hosts, orders, acsn_result))
                return callback(acsn_result) 
            else:
                return callback(self.nma.scan(hosts=hosts,ports= orders,arguments=arguments))
        except nmap.PortScannerError,e:
            print "spidertool::scaninfo()", traceback.print_exc()
            return ''

        except:
            self.logger.info('Unexpected error:%s',sys.exc_info()[0])
            return ''

    def callback_result(self, scan_result):
        print "\n\n======================sniffertool::callback_result()======================\n\n"
        tmp = scan_result
        for i in tmp['scan'].keys():
            host = i
            result=''
            try:
                temphosts = str(host)
                localtime = str(time.strftime("%Y-%m-%d %X", time.localtime()))
                self.getlocationtool.add_work([temphosts])
                try :
                    tempvendor=''
                    temposfamily=''
                    temposgen=''
                    tempaccuracy=''
                    if len(tmp['scan'][host]['osmatch']) > 0 and len(tmp['scan'][host]['osmatch'][0]['osclass'])>0:
                        tempvendor = str(tmp['scan'][host]['osmatch'][0]['osclass'][0].get('vendor',''))
                        temposfamily = str(tmp['scan'][host]['osmatch'][0]['osclass'][0].get('osfamily',''))
                        temposgen = str(tmp['scan'][host]['osmatch'][0]['osclass'][0].get('osgen',''))
                        tempaccuracy = str(tmp['scan'][host]['osmatch'][0]['osclass'][0].get('accuracy',''))
                    temphostname = ''
                    tempdecide = tmp['scan'][host].get('hostnames',[])
                    if len(tempdecide) > 0:
                        for y in tmp['scan'][host]['hostnames']:
                            temphostname += str(y.get('name','unknow'))+' '

                    tempstate = str(tmp['scan'][host]['status'].get('state',''))

		    sqldatawprk=[]
                    dic={"table":self.config.iptable,"select_params": ['ip','vendor','osfamily','osgen','accurate','updatetime','hostname','state'],"insert_values": [(temphosts,tempvendor,temposfamily,temposgen,tempaccuracy,localtime,temphostname,tempstate)]}

                    tempwprk=Sqldata.SqlData('replaceinserttableinfo_byparams',dic)
                    sqldatawprk.append(tempwprk)
                    self.sqlTool.add_work(sqldatawprk)               
                except Exception,e:
                    print 'nmap system error d '+str(e)

                if 'tcp' in tmp['scan'][host].keys():
                    ports = tmp['scan'][host]['tcp'].keys()

                    for port in ports:
                        tempport = str(port)
                        tempportname = str(tmp['scan'][host]['tcp'][port].get('name',''))
                        tempportstate = str(tmp['scan'][host]['tcp'][port].get('state',''))
                        tempproduct = str(tmp['scan'][host]['tcp'][port].get('product',''))
                        tempportversion = str(tmp['scan'][host]['tcp'][port].get('version',''))
                        tempscript=SQLTool.decodestr(str(tmp['scan'][host]['tcp'][port].get('script','')))

                        sqldatawprk=[]
                        dic={"table":self.config.porttable,"select_params": ['ip','port','timesearch','state','name','product','version','script','portnumber'],"insert_values": [(temphosts,tempport,localtime,tempportstate,tempportname,tempproduct,tempportversion,tempscript,str(tempport))]}
                        tempwprk=Sqldata.SqlData('replaceinserttableinfo_byparams',dic)

                        sqldatawprk.append(tempwprk)
                        self.sqlTool.add_work(sqldatawprk)
			# 端口扫描
			self.portscan.add_work([(tempportname,temphosts,tempport,tempportstate,tempproduct,tempscript)])
                elif 'udp' in  tmp['scan'][host].keys():
                    ports = tmp['scan'][host]['udp'].keys()
                    for port in ports:
                        tempport = str(port)
                        tempportname = str(tmp['scan'][host]['udp'][port].get('name',''))
                        tempportstate = str(tmp['scan'][host]['udp'][port].get('state',''))
                        tempproduct = str(tmp['scan'][host]['udp'][port].get('product',''))
                        tempportversion = str(tmp['scan'][host]['udp'][port].get('version',''))
                        tempscript = str(tmp['scan'][host]['udp'][port].get('script',''))

                        sqldatawprk=[]
                        dic={"table":self.config.porttable,"select_params": ['ip','port','timesearch','state','name','product','version','script','portnumber'],"insert_values": [(temphosts,tempport,localtime,tempportstate,tempportname,tempproduct,tempportversion,tempscript,str(tempport))]}
                        tempwprk=Sqldata.SqlData('replaceinserttableinfo_byparams',dic)
                        sqldatawprk.append(tempwprk)
                        self.sqlTool.add_work(sqldatawprk)
            except Exception,e:
                print 'nmap error'+str(e)
            except IOError,e:
                print '错误IOError'+str(e)
            except KeyError,e:
                print '不存在该信息'+str(e)
            finally:
                return str(scan_result)

    def scanaddress(self,hosts=[], ports=[],arguments=''):
        temp=''
        for i in range(len(hosts)):
            if len(ports) <= i:
                result = self.scaninfo(hosts=hosts[i],arguments=arguments)
                if result is None:
                    pass
                else:
                    temp += result
            else:
                result = self.scaninfo(hosts=hosts[i], port=ports[i],arguments=arguments)
                if result is None:
                    pass
                else:
                    temp+=result
        return temp

    def isrunning(self):
        return self.nma.has_host(self.host)


order=' -P0 -sV -sC  -sU  -O -v  -R -sT  '
orderq='-A -P0   -Pn  -sC  -p '


if __name__  ==  "__main__":   
    hosts = []
    host_file = open(sys.argv[1]).readlines()
    for fi in host_file:
        hosts.append(fi.strip())
#    print hosts
#    hosts=['www.ykgs.gov.cn', 'zhengxie.bjtzh.gov.cn','hbj.bjmtg.gov.cn', 'www.bjchp.gov.cn']
#    hosts=['localhost']
    temp = SniffrtTool()
    localtime = str(time.strftime("%Y-%m-%d %X", time.localtime()))
    temp.scanaddress(hosts, ports=['443'],arguments='')
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))



