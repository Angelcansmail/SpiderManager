KEYWORDS = ['asus', ]
def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):


	if 'asus' in context or 'asus' in head:
		return True
	else:
		return False