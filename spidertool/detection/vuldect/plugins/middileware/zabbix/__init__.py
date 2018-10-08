KEYWORDS = ['zabbix', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if 'zabbix' in hackresults or 'zabbix' in context:
        return True
    else:
        return False
