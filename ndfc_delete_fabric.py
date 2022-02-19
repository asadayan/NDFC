#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if len(sys.argv) < 2:
    print(f'usage python {sys.argv[0]} fabric-name ')
    sys.exit()
fabricName = sys.argv[1]
username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}'
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization':ndfc_token, 'Content-Type': 'application/json'}
deleteurl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/' + fabricName
payload = {"sync": "true", "query": {}}
response = requests.delete(deleteurl,
                           data=json.dumps(payload),
                           headers=headers,
                           verify=False)
print(response.text)