#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import pprint


if len(sys.argv) < 2:
    print(f'usage python {sys.argv[0]} fabric-name')
    sys.exit()
fabricName = sys.argv[1]

username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest//control/fabrics/{fabricName}'
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization':ndfc_token, 'Content-Type': 'application/json'}


response = requests.get(posturl, verify=False, headers=headers)
if response.status_code == 200:
    output = json.loads(response.text)

fabric_id = output['id']

posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest//control/fabrics/{fabric_id}/inventory'
response = requests.get(posturl, verify=False, headers=headers)
if response.status_code == 200:
    output = json.loads(response.text)

for item in output:
    out = dict(zip(item['displayHdrs'],item['displayValues']))
    print(out)


