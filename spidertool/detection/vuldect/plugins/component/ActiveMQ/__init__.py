KEYWORDS = ['activemq', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if 'activemq' in productname.get('protocol','') or 'Apache ActiveMQ' in  productname.get('productname',''):
        return True
    else:
        return False
