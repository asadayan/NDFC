#!/usr/bin/python
# Author Ahamed Sadayan
# This python program adds port_channel to VxLAN fabric through DCNM

import ndfc_auth
import json
import requests
import ndfc_credentials
import ndfc_modules
import sys
import re
import pprint
import ipaddress
import time


username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
posturl = url + 'f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/globalInterface/pti?isMultiEdit=false'

fabricName = input('Enter the Fabric Name: ')
NodeName = input('Enter Node Name: ')
NodeType = input('Enter Node Type( spine or leaf ): ')
StartingIntf = input('Enter starting interface: ')
IntfNum = input('Enter number of interface: ')

if NodeType.lower() == 'spine':
    spine_nodes = ndfc_modules.get_spine_nodes(fabricName)
    serialNum = ndfc_modules.get_spine_serial_num(spine_nodes,NodeName)
elif NodeType.lower() == 'leaf':
    leaf_nodes = ndfc_modules.get_leaf_nodes(fabricName)
    serialNum = ndfc_modules.get_serial_num(leaf_nodes, NodeName)



mod_port = re.findall('\d+',StartingIntf)
module = int(mod_port[0])
port = int(mod_port[1])
interfaces=[]
for intf in range(int(IntfNum)):
    interface = f'Ethernet{module}/{port}'
    nvpair = {
                    "INTF_VRF": "",
                    "IP": "",
                    "PREFIX": "",
                    "ROUTING_TAG": "",
                    "MTU": "9216",
                    "SPEED": "Auto",
                    "DESC": "",
                    "CONF": "",
                    "ADMIN_STATE": True,
                    "INTF_NAME": interface
                }

    INTERFACE = {
                "serialNumber": serialNum,
                "interfaceType": "INTERFACE_ETHERNET",
                "ifName": interface,
                "fabricName": fabricName,
                "nvPairs": nvpair
                }
    interfaces.append(INTERFACE)
    payload = {
        "policy": "int_routed_host_11_1",
        "interfaces": interfaces
        }
    print(f'Building config to delete ip address  fabric {fabricName} on node {NodeName}, interface {interface} \n')
    port += 1


response = requests.post(posturl,
                             data=json.dumps(payload),
                             verify=False,
                             headers=headers)


print(response.text)
print('Applied intent on DCNM, please save and deploy')

