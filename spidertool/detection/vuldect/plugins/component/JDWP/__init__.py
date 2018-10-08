KEYWORDS = ['jdwp', ]
def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):


    if 'jdwp' in productname.get('protocol','') or 'Java Debug Wire Protocol' in  productname.get('productname',''):
        return True
    else:

        return False