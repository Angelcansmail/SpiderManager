KEYWORDS = ['websphere', ]
def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):


	if 'websphere' in context or 'websphere' in head:
		return True
	else:
		return False