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
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks'
response = requests.get(posturl, verify=False, headers=headers)
if response.status_code == 200:
    output = json.loads(response.text)

#pprint.pprint(output)
all_network_list=[]
all_deployed_network=[]
all_undeployed_network = []
for item in output:
    netcfg = json.loads(item['networkTemplateConfig'])
    all_network_list.append((item['vrf'],item['networkStatus']))
    if item['networkStatus'].lower() == 'deployed':
        all_deployed_network.append(f"Vrf:{item['vrf']:<16} Network: {item['displayName']:<24}    IPv4: {netcfg['gatewayIpAddress']:<15}     IPv6: {netcfg['gatewayIpV6Address']:<3}    Vlan: {netcfg['vlanId']}")
    if item['networkStatus'].lower() != 'deployed':
        all_undeployed_network.append(f"Vrf:{item['vrf']:<16} Network: {item['displayName']:<24}    IPv4: {netcfg['gatewayIpAddress']:<15}    IPv6: {netcfg['gatewayIpV6Address']:<3}    Vlan: {netcfg['vlanId']}")

all_deployed_network.sort()
all_undeployed_network.sort()
print(f'Number of Deployed Networks: {len(all_deployed_network)}\n')
for item in all_deployed_network:
    print(item)
print(f'\nNumber of Un-Deployed Networks: {len(all_undeployed_network)}\n')
for item in all_undeployed_network:
    print(item)
print(f'\nNumber of Deployed Networks: {len(all_deployed_network)}\n')
print(f'Number of Un-Deployed Networks: {len(all_undeployed_network)}\n')




