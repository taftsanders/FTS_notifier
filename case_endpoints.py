import caller

def get_case_info(caseNumber, token):
    return caller.case('/cases/' + caseNumber, '', token)

def get_case_24x7_status(caseNumber, token):
    return caller.case('/cases/' + caseNumber, '?fields=fts', token)

def get_case_contact_timezone(caseNumber, token):
    return caller.case('/cases/' + caseNumber, '?fields=contact.timezone', token)

def get_fts(sbrGroup, token):
    sbrGroup.replace(' ', '%20')
    return caller.case('/cases?\
                                    fts=true&\
                                    status=Waiting%20on%20Red%20Hat%2CWaiting%20on%20Customer&\
                                    sbrGroups=' + sbrGroup.replace(',','%2C'),'', token)

