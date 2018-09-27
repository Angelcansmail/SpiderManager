KEYWORDS = ['nginx', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackinfo=''):
    if 'nginx' in  hackinfo or 'nginx' in head.lower() or 'nginx' in productname.get('productname',''):
        return True
    else:
        return False
