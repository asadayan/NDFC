#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import pprint


if len(sys.argv) < 2:
    print(f'usage python {sys.argv[0]} fabric-name ')
    sys.exit()
fabricName = sys.argv[1]


username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/vrfs'
response = requests.get(posturl, verify=False, headers=headers)
if response.status_code == 200:
    output = json.loads(response.text)


all_vrf_list=[]
all_deployed_vrf=[]
all_undeployed_vrf = []
for item in output:
    all_vrf_list.append(f"vrf_name: {item['vrfName']}    status: {item['vrfStatus']}    l3_vni: {item['vrfId']}")
    if item['vrfStatus'].lower() == 'deployed':
        all_deployed_vrf.append(f"vrf_name: {item['vrfName']}    status: {item['vrfStatus']}    l3_vni: {item['vrfId']}")
    if item['vrfStatus'].lower() == 'na':
        all_undeployed_vrf.append(f"vrf_name: {item['vrfName']}    status: {item['vrfStatus']}    l3_vni: {item['vrfId']}")


for item in all_deployed_vrf:
    print(item)

for item in all_undeployed_vrf:
    print(item)
print(f'\nNumber of Deployed VRF: {len(all_deployed_vrf)}')
print(f'\nNumber of Un-Deployed VRF: {len(all_undeployed_vrf)}\n')




