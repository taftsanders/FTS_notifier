import requests
import warnings
import os
import json

URL = 'https://access.redhat.com/hydra/rest'

def case(endpoint, fields, token):
  headers = {'Authorization':'Basic ' + token}
  url = URL
  if os.path.exists('/etc/pki/tls/certs/ca-bundle.crt'):
    verify = '/etc/pki/tls/certs/ca-bundle.crt'
  else:
    verify = False
    warnings.filterwarnings("ignore")
  req = requests.get(url + endpoint + fields, headers = headers, verify = verify)
  if int(req.status_code) == 200:
    return req.json()
  else:
    return req.status_code

def user(endpoint, fields, token):
  headers = {'Authorization':'Basic ' + token}
  url = URL
  if os.path.exists('/etc/pki/tls/certs/ca-bundle.crt'):
    verify = '/etc/pki/tls/certs/ca-bundle.crt'
  else:
    verify = False
    warnings.filterwarnings("ignore")
  req = requests.get(url + endpoint + fields, headers = headers, verify = verify)
  #breakpoint()
  if int(req.status_code) == 200:
    return req.json()
  else:
    return req.status_code