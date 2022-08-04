# This is a personal project to get case information from access.redhat.com API
# API Server: access.redhat.com
# Password encoding: echo -n "<SSO-USERNAME>:<PASSWORD>"|base64 -w0

import user_endpoints as user
import case_endpoints as case
import auth
import sysmgmt_fts
import getpass
import base64
import sys
import json
import os
import configparser
from pathlib import Path

TOKEN = ''
HOME = str(Path.home())

def menu_screen():
    auth.auth()
    #Print Menu
    menu = {}
    menu['1:'] = 'Search for a user from SSO Username'
    menu['2:'] = 'Search for reportees by manager SSO'
    menu['3:'] = 'Search for a case by case number'
    menu['4:'] = 'Search for 24x7 cases for an SBR'
    while True:
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])
        try:
            selection = input("Select An Option: ")
            if selection == '1':
                sso = input('Enter the SSO Username: ')
                print(json.dumps(user.get_user_id(sso, TOKEN), indent = 4, sort_keys = True))
                break
            elif selection == '2':
                sso = input('Enter the SSO Username: ')
                print(json.dumps(user.get_reportees(sso, TOKEN), indent = 4, sort_keys = True))
                break
            elif selection == '3':
                caseNumber = input('Enter a case number: ')
                print(json.dumps(case.get_case_info(caseNumber, TOKEN), indent = 4, sort_keys = True))
                break
            elif selection == '4':
                print('Comma separated, no spaces between the SBRs')
                sbrGroups = input('Enter the SBR(s) you want 24x7 cases from: ')
                print(json.dumps(case.get_fts(sbrGroups, TOKEN), indent = 4, sort_keys = True))
            else:
                print("Unknown Option")
        except KeyboardInterrupt:
            print('\nOk byeeeeeeeee')
            sys.exit()


def main():
    menu_screen()


if __name__ == "__main__":
    if os.path.exists(HOME + '/.fts_notifier.conf'):
        print('found config')
        config = configparser.ConfigParser()
        config.read(HOME + '/.fts_notifier.conf')
        username = config['access.redhat.com']['username']
        password = config['access.redhat.com']['password']
        TOKEN = auth.auth(username, password)
        print(TOKEN)
    else:
        TOKEN = auth.auth()
    #print(json.dumps(sysmgmt_fts.sysmgmt_fts_notifier(TOKEN), indent = 4, sort_keys = True))
    print(sysmgmt_fts.analyze_fts_list(TOKEN))