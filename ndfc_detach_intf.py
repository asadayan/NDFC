#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import ndfc_modules
import sys
import re
import pprint


if len(sys.argv) < 3:
    print(f'usage python {sys.argv[0]} fabric-name network_prefix')
    print('Example python ndfc_detach_intf cus')
    sys.exit()
fabricName = sys.argv[1]
network_prefix = sys.argv[2]

interface = ''

username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
leaf_nodes = ndfc_modules.get_leaf_nodes(fabricName)
network_list = ndfc_modules.network_list(fabricName,'all')

payload_list = []
lanattachedlist = []
net_list = []
delete_list= []
for node in leaf_nodes:
    for network in network_list:
        if network['network'].lower()[:3] == network_prefix.lower():
            net_list.append(network['network'])
            print(f"Network prefix matched, going to detach interface from network {network['network']}")
            delete_load = {
                "scopeType": "Device",
                "allocatedTo": network['network'],
                "serialNumber": node['serial_no'],
                "resourceId": "",
                "usageType": "TOP_DOWN_NETWORK_VLAN"
            }
            delete_list.append(json.dumps(delete_load))
            if node['vpc_peer'] == None:
                lanattach = {
                    "fabric": fabricName,
                    "networkName": network['network'],
                    "serialNumber": node['serial_no'],
                    "switchPorts": interface,
                    "detachSwitchPorts": "",
                    "vlan": network['vlan'],
                    "dot1QVlan": 1,
                    "untagged": False,
                    "freeformConfig": "",
                    "deployment": False,
                    "extensionValues": "",
                    "instanceValues": ""
                }
                lanattachedlist.append(lanattach)
            else:
                peer_serial_no = ndfc_modules.get_serial_num(leaf_nodes,node['vpc_peer'])
                lanattach = {
                    "fabric": fabricName,
                    "networkName": network['network'],
                    "serialNumber": node['serial_no'],
                    "switchPorts": interface,
                    "detachSwitchPorts": "",
                    "vlan": network['vlan'],
                    "dot1QVlan": 1,
                    "untagged": False,
                    "freeformConfig": "",
                    "deployment": False,
                    "extensionValues": "",
                    "instanceValues": ""
                }
                lanattachedlist.append(lanattach)
                lanattach = {
                    "fabric": fabricName,
                    "networkName": network['network'],
                    "serialNumber": peer_serial_no,
                    "switchPorts": "",
                    "detachSwitchPorts": "",
                    "vlan": network['vlan'],
                    "dot1QVlan": 1,
                    "untagged": False,
                    "freeformConfig": "",
                    "deployment": False,
                    "extensionValues": "",
                    "instanceValues": ""
                }
                lanattachedlist.append(lanattach)
                lanattach = {}
            payload =   {
                    "networkName": network['network']
                    }
            payload["lanAttachList"] = lanattachedlist
            payload_list.append(payload)
            payload = {}
            lanattachedlist = []
        else:
            print(f"Network name prefix not matching skipping network {network['network']}")


        response = requests.post(posturl,
                                 data=json.dumps(payload_list),
                                 verify=False,
                                 headers=headers)


        if response.status_code == 200:
            output = json.loads(response.text)
            print(f"detached interfaces to node {node['name']},{node['mgmt_ip']}")
            pprint.pprint(output)
        else:
            output = response.text
            print(f" Error detaching interfaces to node {node['name']},{node['mgmt_ip']},{output}")
        payload_list = []


# delet_url = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/resource-manager/release'
# for del_net in delete_list:
#     response = requests.delete(delet_url,
#                              data=del_net,
#                              verify=False,
#                              headers=headers)
#     if response.status_code == 200:
#         output = json.loads(response.text)
#         print("undeployed detached interfaces to nodes ")
#     else:
#         print(f'Undeploy error: {response.reason}')

save = input('Do you want to save and deploy?[Y/N]')

if save.lower() == 'y' or save.lower() == 'yes':
    output = ndfc_modules.save_config(fabricName)
    print(output)

    output = ndfc_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')
