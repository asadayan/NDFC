#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import ndfc_modules
import pprint


if len(sys.argv) < 3:
    print(f'usage python {sys.argv[0]} fabric-name network_name|all')
    print("network_name is any specific network and 'all' keyword is for all undeployed network")
    sys.exit()
fabricName = sys.argv[1]
netName = sys.argv[2]
delete_net = netName
if netName.lower() == 'all':
    confirm = input(f'Do you really want to delete all the un deployed Networks in the fabric {fabricName}? if yes confirm by typing "yes":')
    if confirm.lower() != 'yes':
        print('Exiting for not confirming!')
        sys.exit()
    elif confirm.lower() == 'yes':
        print(f'Deleting all the un deployed Networks in the fabric {fabricName}')

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
all_deployed_networks=[]
all_undeployed_networks = []
all_deployed_network=[]
all_undeployed_network = []
for item in output:
    netcfg = json.loads(item['networkTemplateConfig'])
    all_network_list.append((item['vrf'],item['networkStatus']))
    if item['networkStatus'].lower() == 'deployed':
        all_deployed_networks.append(f"Vrf:{item['vrf']} Network: {item['displayName']}  IPv4: {netcfg['gatewayIpAddress']} vlan: {netcfg['vlanId']}")
        all_deployed_network.append(item['displayName'])
    if item['networkStatus'].lower() != 'deployed':
        all_undeployed_networks.append(f"Vrf:{item['vrf']} Network: {item['displayName']}  IPv4: {netcfg['gatewayIpAddress']} vlan: {netcfg['vlanId']}")
        all_undeployed_network.append(item['displayName'])
all_deployed_network.sort()
all_undeployed_network.sort()
print(f'Number of Deployed Networks: {len(all_deployed_network)}\n')
for item in all_deployed_networks:
    print(item)
print(f'\nNumber of Un-Deployed Networks: {len(all_undeployed_network)}\n')
for item in all_undeployed_networks:
    print(item)


if delete_net.lower() != 'all':
    deleteurl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/{delete_net}'
    response = requests.delete(deleteurl, verify=False, headers=headers)
    if response.status_code == 200:
        print(f'Network {delete_net} deleted',response.text)
    else:
        error = json.loads(response.text)
        print(f'Error deleting Network {delete_net} ', error['message'])


elif len(all_undeployed_network)>0 and delete_net.lower() == 'all':
    #print(all_undeployed_network)
    for delete_net in all_undeployed_network:
        deleteurl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/{delete_net}'
        try:
            response = requests.delete(deleteurl, verify=False, headers=headers)
            if response.status_code == 200:
                print(f' Network {delete_net} deleted')
            else:
                print(f'Error deleting Network {delete_net}')
        except:
            ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
            headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
            response = requests.delete(deleteurl, verify=False, headers=headers)
            if response.status_code == 200:
                print(f' Network {delete_net} deleted')
            else:
                print(f'Error deleting Network {delete_net}')

save = input('Do you want to save and deploy?[Y/N]: ')

if save.lower() == 'y' or save.lower() == 'yes':
    output = ndfc_modules.save_config(fabricName)
    print(output)

    output = ndfc_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')







