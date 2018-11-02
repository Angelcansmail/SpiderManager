KEYWORDS = ['hadoop', 'namenode']

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if port in '50070' or 'namenode' in context.lower():
        return True
    else:
        return False
