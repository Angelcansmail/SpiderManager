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
    def __init__(self, logger=None):
        '''
        Constructor
        '''
        self.logger = logger
        try:
            self.nma = nmap.PortScanner()     # instantiate nmap.PortScanner object
            self.params='-sS -T4 -A -Pn '
            self.usual_ports='502'
#            self.usual_ports='7,9,13,21-23,25-26,31,37,42,53,67,69,79-82,85,88,99,102,106,109-111,113,119,135,137-139,143-144,161,177,179,199,389,427,443-445,456,465,502,513-515,543-544,548,554,587,631,636,646,666,873,990,993,995,1001,1011,1025-1029,1033,1089-1091,1110,1158,1170,1234,1243,1433-1434,1492,1500,1521,1524,1541,1600,1720,1723,1755,1900,1935,1962,1999-2001,2023,2049,2100,2121,2404,2717,3000,3128,3306,3389,3986,4000,4840,4843,4899,5000,5007,5009,5052,5060,5065,5101,5190,5357,5432,5450,5631,5666,5800,5900,6000-6001,6379,6646,6711,6776,7000-7002,7070,8000-8001,8008-8009,8080-8082,8088-8090,8099,8181,8400,8443,8888,9080,9090-9091,9100,9200,9999-10000,10307,10311,10364-10365,10407,10409-10410,10412,10414-10415,10428,10431-10432,10447,10449-10450,11001,12135-12137,12316,12645,12647-12648,13722,13724,13782-13783,18000,18245,20000,20547,32768,34962-34964,38000-38001,38011-38012,38014-38015,38200,38210,38301,38400,38589,38593,38600,38700,38971,39129,39278,44818,45678,47808,49152-49157,50001-50016,50018-50021,50025-50028,50110-50111,55000-55003,55555,56001-56099,62900,62911,62924,62930,62938,62956-62957,62963,62981-62982,62985,62992,63012,63027-63036,63041,63075,63079,63082,63088,63094,65000,65443'
#            self.params='-A -sC -R -v -O -T4 -Pn '
#            self.params='-sV -T4 -Pn -O '         #快捷扫描加强版
#            self.params='-sS -sU -T4 -A -v '   #深入扫描
        except nmap.PortScannerError:
            self.logger.error('Nmap not found:%s',sys.exc_info()[0])
        except:
            self.logger.error('Unexpected error:%s',sys.exc_info()[0])

        self.config = config.Config
        self.sqlTool = Sqldatatask.getObject()  # init DBmanager, and connect database and thread number
        self.portscan = portscantask.getObject()    #设置一些网络参数配置, 查看portScantask.log
        # init DBmanager and thread number
        self.getlocationtool = getLocationTool.getObject()

    def scaninfo(self,hosts='localhost', port='', arguments='', hignpersmission='0', callback=''):
        if callback == '': 
            callback = self.callback_result
#	后端添加任务的时候会写port，默认执行nmap自带的扫描
        orders = ''
        if port != '':
	    # 为什么要加，直接使用port不一样吗，在网页输入的时候是逗号分割的port
            orders += port
        else :
            orders = None
        try:
            if hignpersmission == '0':
                acsn_result = self.nma.scan(hosts=hosts,ports=self.usual_ports,arguments=self.params+arguments)
                self.logger.debug("%s:%s扫描结束\n"%(hosts, orders))
#                print ("%s:%s扫描结束\n%s\n"%(hosts, orders, acsn_result))
                return callback(acsn_result) 
            else:
                return callback(self.nma.scan(hosts=hosts,ports=orders,arguments=arguments))
        except nmap.PortScannerError,e:
            self.logger.error("spidertool::scaninfo()", traceback.print_exc())
            return ''
        except:
            self.logger.error('Unexpected error:%s',sys.exc_info()[0])
            return ''

    def callback_result(self, scan_result):
        self.logger.info("======================sniffertool::callback_result()======================")
        tmp = scan_result
        for i in tmp['scan'].keys():
            host = i
            result=''
            try:
                temphosts = str(host)
                localtime = str(time.strftime("%Y-%m-%d %X", time.localtime()))
                self.getlocationtool.add_work([temphosts])	#why add this operator? 在网页上没有执行zmap扫描，所以需要加入位置信息的判断，但是后端添加的任务，相当于执行了两次这个位置信息的扫描
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
                    self.logger.error('Nmap system Error::'+str(e))
#                    print 'nmap system error d '+str(e)

                if 'tcp' in tmp['scan'][host].keys():
                    ports = tmp['scan'][host]['tcp'].keys()

                    for port in ports:
                        tempport = str(port)
                        tempportname = str(tmp['scan'][host]['tcp'][port].get('name',''))
                        tempportstate = str(tmp['scan'][host]['tcp'][port].get('state',''))
                        tempproduct = str(tmp['scan'][host]['tcp'][port].get('product',''))
                        tempportversion = str(tmp['scan'][host]['tcp'][port].get('version',''))
                        tempscript=SQLTool.decodestr(str(tmp['scan'][host]['tcp'][port].get('script','')))

                        if tempportstate.find('open') == -1:
                            self.logger.info("[%s] not open! passing...%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s", temphosts,tempport,localtime,tempportstate,tempportname,tempproduct,tempportversion,tempscript,str(tempport))
                            continue

                        sqldatawprk=[]
                        dic={"table":self.config.porttable,"select_params": ['ip','port','timesearch','state','name','product','version','script','portnumber'],"insert_values": [(temphosts,tempport,localtime,tempportstate,tempportname,tempproduct,tempportversion,tempscript,str(tempport))]}
                        tempwprk=Sqldata.SqlData('replaceinserttableinfo_byparams',dic)

                        sqldatawprk.append(tempwprk)
                        self.sqlTool.add_work(sqldatawprk)
			# 端口扫描(正常协议|非正常协议)
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
                self.logger.error('Nmap Error'+str(e))
            except IOError,e:
                self.logger.error('错误IOError'+str(e))
            except KeyError,e:
                self.logger.warning('不存在该信息'+str(e))
            finally:
                return str(scan_result)

    def scanaddress(self,hosts=[], ports=[],arguments=''):
        temp=''
	self.logger.info("begin scanaddress->%s:%s", str(hosts), str(ports))

        for i in range(len(hosts)):
            # 不指定端口，则扫描全部端口
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



