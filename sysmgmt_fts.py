import caller
import case_endpoints as case
import alerts

FTS_LIST=[]
CASE = {}
TIMEZONE = ''
NA_TIMEZONE_LIST = ['Atlantic/South_Georgia', 
                                        'America/Buenos_Aires', 
                                        'America/Sao_Paulo', 
                                        'America/St_Johns', 
                                        'America/Halifax', 
                                        'America/Puerto_Rico', 
                                        'America/Santiago', 
                                        'Atlantic/Bermuda', 
                                        'America/Caracas', 
                                        'America/Bogota', 
                                        'America/Indianapolis', 
                                        'America/Lima', 
                                        'America/New_York', 
                                        'America/Panama', 
                                        'America/Chicago', 
                                        'America/El_Salvador', 
                                        'America/Mexico_City', 
                                        'America/Denver', 
                                        'America/Phoenix', 
                                        'America/Los_Angeles', 
                                        'America/Tijuana', 
                                        'America/Anchorage', 
                                        'Pacific/Honolulu', 
                                        'Pacific/Niue', 
                                        'Pacific/Pago_Pago']

def sysmgmt_fts_notifier(token):
    return caller.case('/cases'
                                    '?fts=true'
                                    '&status=Waiting%20on%20Red%20Hat%2CWaiting%20on%20Customer'
                                    '&sbrGroups=SysMgmt%2CInsights%2CSubscription%20Management' ,'', token)

def compare_fts_list(token):
    global FTS_LIST
    # For case in fts_list, verify its still FTS, if not remove case from list
    for caseNumber in FTS_LIST:
        if case.get_case_24x7_status(caseNumber,token).get('fts') == False:
            FTS_LIST.remove(caseNumber)
    # Take data from sysmgmt_fts_notifier and extract caseNumbers
    for caseNumber in sysmgmt_fts_notifier(token):
        FTS_LIST.append(caseNumber.get('caseNumber'))
    FTS_LIST = list(dict.fromkeys(FTS_LIST))

def _set_case_info(caseNumber, token):
    global CASE
    CASE = case.get_case_info(caseNumber, token)

def check_for_owner():
    if not CASE.get('caseOwnerId'):
        return False
    else:
        return CASE.get('caseOwnerId')

def check_for_severity3or4():
    if CASE.get('severity') == '4 (Low)' or CASE.get('severity') == '3 (Normal)':
        return True

def get_timezone(token):
    global TIMEZONE
    contact = case.get_case_contact_timezone(CASE.get('caseNumber'), token)
    TIMEZONE = contact.get('contact').get('timezone')
    return TIMEZONE

def get_product():
    return CASE.get('product')

def get_version():
    return CASE.get('version')

def get_contact_name():
    return CASE.get('contact').get('name')

def get_caseOwner_name():
    return CASE.get('caseOwner').get('name')


# Construct algorithm to determine message display need (if this then do...)
def analyze_fts_list(token):
    while True:
        compare_fts_list(token)
        print("compared fts list")
        for ticket in FTS_LIST:
            _set_case_info(ticket, token)
            print("set_case_info")
            if check_for_severity3or4():
                print('check severity 3/4')
                message = ticket + ' is a ' + CASE.get('severity') + ' severity, DROP IT!'
                alerts.notification(ticket, message, 'critical')
            else:
                try:
                    if get_timezone(token) in NA_TIMEZONE_LIST:
                        if not check_for_owner():
                            message = 'NCQ FTS\n' + get_product() + ' ' + get_version()
                            alerts.notification(ticket,message, 'warning' )
                        elif check_for_owner():
                            message = 'Chowned FTS\n' + get_caseOwner_name()
                            alerts.notification(ticket, message, 'warning')
                    else:
                        #'{} is {}, not NA', ticket, TIMEZONE
                        #f'{ticket} is {TIMEZONE}'
                        print('Timezone %s not in NA' % TIMEZONE)
                except:
                    print(CASE)




