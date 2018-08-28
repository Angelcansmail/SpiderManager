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
#             self.params='-A -Pn -sC -R -v -O -T5 '
            self.params='-sV -T4 -Pn -O '         #快捷扫描加强版
#             self.params='-sS -sU -T4 -A -v '   #深入扫描
        except nmap.PortScannerError:
#             print('Nmap not found', sys.exc_info()[0])
            self.logger.info('Nmap not found:%s',sys.exc_info()[0])
        except:
#             print('Unexpected error:', sys.exc_info()[0])
            self.logger.info('Unexpected error:%s',sys.exc_info()[0])

        self.config = config.Config
        self.sqlTool = Sqldatatask.getObject()  # init DBmanager, and connect database and thread number
#         self.sqlTool=SQLTool.getObject()
        self.portscan = portscantask.getObject()    #设置一些网络参数配置, 查看portScantask.log
        # init DBmanager and thread number
        self.getlocationtool = getLocationTool.getObject()

    def scaninfo(self,hosts='localhost', port='', arguments='',hignpersmission='0',callback=''):
        if callback == '': 
            callback = self.callback_result
        orders = ''
        if port != '':
            orders += port
        else :
            orders = None
        try:
            if hignpersmission == '0':
                acsn_result = self.nma.scan(hosts=hosts,ports=orders,arguments=self.params+arguments)
                print ("扫描结束\n%s\n"%(acsn_result))
                return callback(acsn_result) 
            else:
                return callback(self.nma.scan(hosts=hosts,ports= orders,arguments=arguments))
        except nmap.PortScannerError,e:
            print "spidertool::scaninfo()", traceback.print_exc()
            return ''

        except:
            print('Unexpected error', traceback.print_exc())
            self.logger.info('Unexpected error:%s',sys.exc_info()[0])
            return ''

    def callback_result(self, scan_result):
        print "\n\n======================sniffertool::callback_result()======================\n\n"
        tmp = scan_result
        for i in tmp['scan'].keys():
            host = i
            result=''
            try:
#                 result =  u"ip地址:%s 主机名:%s  ......  %s\n" %(host,tmp['scan'][host].get('hostnames','null'),tmp['scan'][host]['status'].get('state','null'))
#                 self.sqlTool.connectdb()
#                 print tmp['scan'][host].get('hostname','null')
#                 if 'osclass' in tmp['scan'][host].keys():
#                     result +=u"系统信息 ： %s %s %s   准确度:%s  \n" % (str(tmp['scan'][host]['osclass'].get('vendor','null')),str(tmp['scan'][host]['osclass'].get('osfamily','null')),str(tmp['scan'][host]['osclass'].get('osgen','null')),str(tmp['scan'][host]['osclass'].get('accuracy','null')))
#                 print result
                temphosts = str(host)
                localtime = str(time.strftime("%Y-%m-%d %X", time.localtime()))
                self.getlocationtool.add_work([temphosts])
                try :
                    tempvendor='null'
                    temposfamily='null'
                    temposgen='null'
                    tempaccuracy='null'
                    if len(tmp['scan'][host]['osmatch']) > 0 and len(tmp['scan'][host]['osmatch'][0]['osclass'])>0:
                        tempvendor = str(tmp['scan'][host]['osmatch'][0]['osclass'][0].get('vendor','null'))
                        temposfamily = str(tmp['scan'][host]['osmatch'][0]['osclass'][0].get('osfamily','null'))
                        temposgen = str(tmp['scan'][host]['osmatch'][0]['osclass'][0].get('osgen','null'))
                        tempaccuracy = str(tmp['scan'][host]['osmatch'][0]['osclass'][0].get('accuracy','null'))
                    temphostname = ''
                    tempdecide = tmp['scan'][host].get('hostnames',[])
                    if len(tempdecide) > 0:
                        for y in tmp['scan'][host]['hostnames']:
                            temphostname += str(y.get('name','unknow'))+' '

                    tempstate = str(tmp['scan'][host]['status'].get('state','null'))
                # print ("\n======================osmatch information======================\nhosts:%s\nvendor:%s\nosfamily:%s\nosgen:%s\naccuracy:%s\nlocaltime:%s"%(temphosts, tempvendor, temposfamily, temposgen, tempaccuracy, str(localtime)))
#                 self.sqlTool.replaceinserttableinfo_byparams(table=self.config.iptable,select_params= ['ip','vendor','osfamily','osgen','accurate','updatetime','hostname','state'],insert_values= [(temphosts,tempvendor,temposfamily,temposgen,tempaccuracy,localtime,temphostname,tempstate)])         
                    sqldatawprk=[]
                    dic={"table":self.config.iptable,"select_params": ['ip','vendor','osfamily','osgen','accurate','updatetime','hostname','state'],"insert_values": [(temphosts,tempvendor,temposfamily,temposgen,tempaccuracy,localtime,temphostname,tempstate)]}

                    tempwprk=Sqldata.SqlData('replaceinserttableinfo_byparams',dic)
                    sqldatawprk.append(tempwprk)
                    self.sqlTool.add_work(sqldatawprk)               
                except Exception,e:
                    print 'nmap system error d '+str(e)

                if 'tcp' in  tmp['scan'][host].keys():
                    ports = tmp['scan'][host]['tcp'].keys()

                    for port in ports:
#                     portinfo = " port : %s  name:%s  state : %s  product : %s version :%s  script:%s \n" %(port,tmp['scan'][host]['tcp'][port].get('name',''),tmp['scan'][host]['tcp'][port].get('state',''),   tmp['scan'][host]['tcp'][port].get('product',''),tmp['scan'][host]['tcp'][port].get('version',''),tmp['scan'][host]['tcp'][port].get('script',''))
                        tempport = str(port)
                        tempportname = str(tmp['scan'][host]['tcp'][port].get('name',''))
                        tempportstate = str(tmp['scan'][host]['tcp'][port].get('state',''))
                        tempproduct = str(tmp['scan'][host]['tcp'][port].get('product',''))
                        tempportversion = str(tmp['scan'][host]['tcp'][port].get('version',''))
                        tempscript=SQLTool.decodestr(str(tmp['scan'][host]['tcp'][port].get('script',{})))

#                         self.sqlTool.replaceinserttableinfo_byparams(table=self.config.porttable,select_params= ['ip','port','timesearch','state','name','product','version','script'],insert_values= [(temphosts,tempport,localtime,tempportstate,tempportname,tempproduct,tempportversion,tempscript)])         
                        sqldatawprk=[]
                        dic={"table":self.config.porttable,"select_params": ['ip','port','timesearch','state','name','product','version','script','portnumber'],"insert_values": [(temphosts,tempport,localtime,tempportstate,tempportname,tempproduct,tempportversion,tempscript,str(tempport))]}
                        tempwprk=Sqldata.SqlData('replaceinserttableinfo_byparams',dic)

                        sqldatawprk.append(tempwprk)
                        self.sqlTool.add_work(sqldatawprk)
                        self.portscan.add_work([(tempportname,temphosts,tempport,tempportstate,tempproduct,tempscript)])
                elif 'udp' in  tmp['scan'][host].keys():
                    ports = tmp['scan'][host]['udp'].keys()
                    for port in ports:
#                         portinfo = " port : %s  name:%s  state : %s  product : %s version :%s  script:%s \n" %(port,tmp['scan'][host]['udp'][port].get('name',''),tmp['scan'][host]['udp'][port].get('state',''),   tmp['scan'][host]['udp'][port].get('product',''),tmp['scan'][host]['udp'][port].get('version',''),tmp['scan'][host]['udp'][port].get('script',''))
#                         result = result + portinfo
                        tempport = str(port)
                        tempportname = str(tmp['scan'][host]['udp'][port].get('name',''))
                        tempportstate = str(tmp['scan'][host]['udp'][port].get('state',''))
                        tempproduct = str(tmp['scan'][host]['udp'][port].get('product',''))
                        tempportversion = str(tmp['scan'][host]['udp'][port].get('version',''))
                        tempscript = str(tmp['scan'][host]['udp'][port].get('script',''))
                        
#                         self.sqlTool.replaceinserttableinfo_byparams(table=self.config.porttable,select_params= ['ip','port','timesearch','state','name','product','version','script'],insert_values= [(temphosts,tempport,localtime,tempportstate,tempportname,tempproduct,tempportversion,tempscript)])         
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
#                 print result
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

def callback_resultl(host, scan_result):
    print '———不触发这个函数———'
    tmp=scan_result
    result=''

    try:
        result =  u"ip地址:%s 主机名:%s  ......  %s\n" %(host,tmp['scan'][host]['hostname'],tmp['scan'][host]['status']['state'])
        if 'osclass' in tmp['scan'][host].keys():
            result +=u"系统信息 ： %s %s %s   准确度:%s  \n" % (str(tmp['scan'][host]['osclass']['vendor']),str(tmp['scan'][host]['osclass']['osfamily']),str(tmp['scan'][host]['osclass']['osgen']),str(tmp['scan'][host]['osclass']['accuracy']))
        if 'tcp' in  tmp['scan'][host].keys():
            ports = tmp['scan'][host]['tcp'].keys()
            for port in ports:

                portinfo = " port : %s  name:%s  state : %s  product : %s version :%s  script:%s \n" %(port,tmp['scan'][host]['tcp'][port]['name'],tmp['scan'][host]['tcp'][port]['state'],   tmp['scan'][host]['tcp'][port]['product'],tmp['scan'][host]['tcp'][port]['version'],tmp['scan'][host]['tcp'][port]['script'])
                print portinfo
                result+=  portinfo
        elif 'udp' in  tmp['scan'][host].keys():
            ports = tmp['scan'][host]['udp'].keys()
            for port in ports:
                portinfo = " port : %s  name:%s  state : %s  product : %s  version :%s  script:%s \n" %(port,tmp['scan'][host]['udp'][port]['name'],tmp['scan'][host]['udp'][port]['state'],   tmp['scan'][host]['udp'][port]['product'],tmp['scan'][host]['udp'][port]['version'],tmp['scan'][host]['udp'][port]['script'])
                result += portinfo
    except Exception,e:
        print e
    except IOError,e:
        print '错误IOError'+str(e)
    except KeyError,e:
        print '不存在该信息'+str(e)
    finally:
            return result
    
"""
def callback_resultl(host, scan_result):
    print scan_result
    print scan_result['scan']
    f = open('abc.xml','w+')
    f.write(str(scan_result))
    f.close()
"""


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




