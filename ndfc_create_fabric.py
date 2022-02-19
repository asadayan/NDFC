#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import pprint
import ndfc_template


if len(sys.argv) < 3:
    print(f'usage python {sys.argv[0]} fabric-name as_num [replication-mode]')
    print('example: python create_fabric.py test-fabric 65001 [Multicast|Ingress]')
    sys.exit()
fabricName = sys.argv[1]
asNumber = sys.argv[2]
payload = ndfc_template.easy_fabric
payload['fabricName'] = fabricName
payload['nvPairs']['FABRIC_NAME'] = fabricName
payload['nvPairs']['BGP_AS'] = asNumber
payload['nvPairs']['SITE_ID'] =  asNumber
payload['asn'] = asNumber
payload['siteId'] = asNumber
payload['nvPairs']['MULTICAST_GROUP_SUBNET'] = '235.1.1.0/24'
try:
    if sys.argv[3]:
        replicationMode = sys.argv[3]
        payload['nvPairs']['REPLICATION_MODE'] = replicationMode
        payload['replicationMode'] = replicationMode
except:
    print('Default replication mode Multicast configured')

#pprint.pprint(payload)
#sys.exit()
username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/'
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization':ndfc_token, 'Content-Type': 'application/json'}


#print(payload)

response = requests.post(posturl,
                        data=json.dumps(payload),
                        headers=headers,
                        verify=False)

if response.status_code == 200:
  try:
    output = json.loads(response.text)
  except:
    output = response.text
else:
  try:
     output = json.loads(response.reason)
  except:
     output = response.reason

pprint.pprint(output)

