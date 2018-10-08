KEYWORDS = ['xampp', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if 'xampp' in productname.get('protocol','') or 'xampp' in  productname.get('productname',''):
        return True
    else:
        return False
