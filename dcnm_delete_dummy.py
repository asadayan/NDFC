#!/usr/bin/python
# Author Ahamed Sadayan
# This python program adds port_channel to VxLAN fabric through DCNM

import dcnm_auth
import json
import requests
import dcnm_credentials
import dcnm_modules
import sys
import re
import pprint
import ipaddress
import time


username = dcnm_credentials.username
password = dcnm_credentials.password
url = 'https://' + dcnm_credentials.node_ip
dcnm_token = dcnm_auth.auth(url,username,password)
headers = {'Dcnm-Token': dcnm_token, 'Content-Type': 'application/json'}
posturl = url + '/rest/globalInterface/pti?isMultiEdit=false'

fabricName = input('Enter the Fabric Name: ')
NodeName = input('Enter Node Name: ')
NodeType = input('Enter Node Type( spine or leaf ): ')
StartingIntf = input('Enter starting interface: ')
IntfNum = input('Enter number of interface: ')

if NodeType.lower() == 'spine':
    spine_nodes = dcnm_modules.get_spine_nodes(fabricName)
    serialNum = dcnm_modules.get_spine_serial_num(spine_nodes,NodeName)
elif NodeType.lower() == 'leaf':
    leaf_nodes = dcnm_modules.get_leaf_nodes(fabricName)
    serialNum = dcnm_modules.get_serial_num(leaf_nodes, NodeName)



interfaces=[]
for intf in range(int(IntfNum)):
    interface = f'2'
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


response = requests.delete(posturl,
                             data=json.dumps(payload),
                             verify=False,
                             headers=headers)


print(response.text)
print('Applied intent on DCNM, please save and deploy')

