KEYWORDS = ['apache', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackinfo=''):
    if 'apache' in head.lower() or 'apache' in productname.get('productname',''):
	return True
    else:
    	return False
