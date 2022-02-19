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
headers = {'Authorization':ndfc_token, 'Content-Type': 'application/json'}
posturl = url + 'f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/globalInterface/pti?isMultiEdit=false'

fabricName = input('Enter the Fabric Name: ')
NodeName = input('Enter Node Name: ')
NodeType = input('Enter Node Type( spine or leaf ): ')
IP_Address = input('Enter starting ip address: ')
IP_Mask = input('Enter ipv4 address mask: ')
StartingIntf = input('Enter starting interface: ')
IntfNum = input('Enter number of interface: ')

if NodeType.lower() == 'spine':
    spine_nodes = ndfc_modules.get_spine_nodes(fabricName)
    serialNum = ndfc_modules.get_spine_serial_num(spine_nodes,NodeName)
elif NodeType.lower() == 'leaf':
    leaf_nodes = ndfc_modules.get_leaf_nodes(fabricName)
    serialNum = ndfc_modules.get_serial_num(leaf_nodes, NodeName)

ip_addr = ipaddress.ip_address(IP_Address)

mod_port = re.findall('\d+',StartingIntf)
module = int(mod_port[0])
port = int(mod_port[1])
interfaces=[]
for intf in range(int(IntfNum)):
    interface = f'Ethernet{module}/{port}'
    #print(interface)
    nvpair = {
                    "INTF_VRF": "",
                    "IP": str(ip_addr),
                    "PREFIX": IP_Mask,
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
    print(f'Building config for fabric {fabricName} on node {NodeName}, interface {interface} ip address {ip_addr} mask {IP_Mask}\n')
    port += 1
    ip_addr = ip_addr + pow(2,32-int(IP_Mask))

#sys.exit()
response = requests.post(posturl,
                             data=json.dumps(payload),
                             verify=False,
                             headers=headers)


print(response.text)
print('Applied intent on DCNM, please save and deploy')

