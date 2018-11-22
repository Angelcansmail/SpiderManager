KEYWORDS = ['heartblede', ]

def rules(head='',context='',ip='',port='',productname={},keywords='',hackresults=''):
    if int(port) in [443,587,465,995,8443] or productname.get('protocol','') in ['https','smtp','pop3','imap','https-alt']:
        return True
    else:
        return False
