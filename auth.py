import getpass
import base64
import sys




def auth(username = None, password = None):
    #Base64 username and password to make a token
    global TOKEN
    if not username and not password:
        while True:
            try:
                username = input('Enter your SSO username: ')
                password = getpass.getpass('Enter your password')
                auth_byte = base64.b64encode((username + ':' + password).encode('utf-8'))
                TOKEN =  auth_byte.decode('utf-8')
                break
            except KeyboardInterrupt:
                print('\nOK byeeeeeeeee')
                sys.exit()
    elif username and password:
        auth_byte = base64.b64encode((username + ':' + password).encode('utf-8'))
        TOKEN =  auth_byte.decode('utf-8')
    return TOKEN