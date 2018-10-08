KEYWORDS = ['nginx', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if 'nginx' in  hackresults or 'nginx' in head.lower() or 'nginx' in productname.get('productname',''):
        return True
    else:
        return False
