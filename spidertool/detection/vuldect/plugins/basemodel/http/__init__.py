KEYWORDS = ['http', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if 'http' in productname.get('protocol',''):
        return True
    else:
        return False
