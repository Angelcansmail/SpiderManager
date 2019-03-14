#!/usr/bin/python
#coding:utf-8

def mssql(ip='',port='1433',name='',productname=''):
    head=''
    ans=None
    keywords=''
    hackresults=''
    import pymssql,chardet
    con=None
    passwd=['root','123456','admin','','12345','111111','password','123123','1234','12345678','123456789','123',
            'abc123','qwerty']
    for i in passwd:
        try:
            con = pymssql.connect(host=ip,user='sa',password=i,login_timeout=5)  
            hackresults = {'level':'警告', 'type': 'Mssql Connect Error.', 'URL': ip + ':' + port, 'result': ' the password is :'+i}
            print ip+hackresults
            keywords='mssql'
            break;
        except Exception,e:
            keywords='mssql'
            hackresults = {'level':'警告', 'type': 'Mssql Connect Error.', 'URL': ip + ':' + port, 'result': str(e)}
            if 'sa' in hackresults:
                print 'yes'
            chardit1 = chardet.detect(hackresults)
            print hackresults.decode(chardit1['encoding']).encode('utf8')
            
        finally:
            if con !=None:
                con.close()
    return head,ans,keywords,hackresults
# print mssql(ip='192.168.1.100')