#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import ndfc_modules
import pprint
import re

def is_net_in_intf(port_chnl_list,netWork):
    for item in port_chnl_list:
        if netWork in item['attached_net']:
            return True
    return False

if len(sys.argv) < 2:
    print(f'usage python {sys.argv[0]} fabric-name [net-prefix]')
    sys.exit()

fabricName = sys.argv[1]
if len(sys.argv) == 3:
    netPrefix = str(sys.argv[2])

username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
po_list = ndfc_modules.get_leaf_nodes(fabricName)
net_list = ndfc_modules.network_list(fabricName,'all')
port_chnl_list = ndfc_modules.get_port_channels(fabricName)
network_list = []
for net in net_list:
    if net['network'][:3].lower() == netPrefix[:3].lower():
        network_list.append(net)

node_names =''

for net in network_list:
    attach=[]
    if is_net_in_intf(port_chnl_list,net['network']):
        print(f"{net['network']} found attached")
        for node in po_list:
            pair1 = {
                    "fabric": fabricName,
                    "networkName": net["network"],
                    "serialNumber":node["serial_no"],
                    "switchPorts": "",
                    "detachSwitchPorts": "",
                    "vlan": net['vlan'],
                    "dot1QVlan": 1,
                    "untagged": False,
                    "freeformConfig": "",
                    "deployment": False,
                    "extensionValues": "",
                    "instanceValues": ""
                }
            attach.append(pair1)
            if int(node['vpc_domain']) != 0:
                pair2 = {
                        "fabric": fabricName,
                        "networkName": net["network"],
                        "serialNumber": node["peer_serial_no"],
                        "switchPorts": "",
                        "detachSwitchPorts": "",
                        "vlan": net['vlan'],
                        "dot1QVlan": 1,
                        "untagged": False,
                        "freeformConfig": "",
                        "deployment": False,
                        "extensionValues": "",
                        "instanceValues": ""
                    }
                attach.append(pair2)
            detach_load = [{
                "networkName": net['network'],
                "lanAttachList":attach}]
            posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
            response = requests.post(posturl, data=json.dumps(detach_load), verify=False, headers=headers)
            reason = response.reason
            if response.status_code == 200:
                output = response.text
                print(f"Detached interface from nodes for the network {net['network']} on node {node['name']}")
            elif reason.strip() == 'Unauthorized':
                ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
                headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
                posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
                response = requests.post(posturl, data=json.dumps(detach_load), verify=False, headers=headers)
                output = response.text
                print(f"Detached interface from nodes for the network {net['network']} on node {node['name']}")
            else:
                print('Error:', response.reason)
    else:
        print(f"No interface in {net['network']} - skipping")





save = input('Do you want to save and deploy?[Y/N]: ')

if save.lower() == 'y' or save.lower() == 'yes':
    output = ndfc_modules.save_config(fabricName)
    print(output)

    output = ndfc_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')

