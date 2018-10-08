KEYWORDS = ['elasticsearch', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if port in '9200' or 'elasticsearch' in  productname.get('productname',''):
        return True
    else:
        return False
