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


if len(sys.argv) < 5:
    print(f'usage python {sys.argv[0]} fabric-name intf_range ifgrp_name network_prefix [all]')
    print('Example python ndfc_attach_intf_group e1/1,e1/5|e1/1-3 ibm all')
    sys.exit()
fabricName = sys.argv[1]
intf_range = sys.argv[2]
ifgroupName = sys.argv[3]
network_prefix = sys.argv[4]
if len(sys.argv) == 6:
    fetch = 'all'
else:
    fetch = 'undeployed'

interface = ''
port_range = ndfc_modules.get_intf_set(intf_range,'long')





print(interface)


username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}




posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'

leaf_nodes = ndfc_modules.get_leaf_nodes(fabricName)
network_list = ndfc_modules.network_list(fabricName,fetch)
#print(network_list)
#sys.exit()
payload_list = []
lanattachedlist = []
for index, node in enumerate(leaf_nodes):
    ifgName = ifgroupName + str(index+1)
    ifgrp_url = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}/groups/{ifgName}
    resp0 = requests.post(ifgrp_url, verify=False, headers=headers)
    if resp0.status_code == 200:
        out = json.loads(resp0.text)
        print(out)
    else:
        print(response.reason)
    ifgrp_list=[]
    for item in interface:
        ifgrp_load = {
            "switchSN": node['serial_no'],
            "switchPort": item
        }
        ifgrp_list.append(ifgrp_load)
    ifgrp_payload = { 'switchandPortList': ifgrp_list
                    }
    intfGrpurl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}/groups/{ifgName}/ifassoc/'
    res = requests.post(intfGrpurl,
                             data=json.dumps(ifgrp_payload),
                             verify=False,
                             headers=headers)
    if res.status_code == 200:
        output = json.loads(res.text)
        print(output)
        for network in network_list:
            if network['network'].lower()[:3] == network_prefix.lower():
                if node['vpc_peer'] == None:
                    lanattach = {
                        "fabric": fabricName,
                        "networkName": network['network'],
                        "serialNumber": node['serial_no'],
                        "switchPorts": ifgName,
                        "detachSwitchPorts": "",
                        "vlan": network['vlan'],
                        "dot1QVlan": 1,
                        "untagged": False,
                        "freeformConfig": "",
                        "deployment": True,
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
                        "switchPorts": ifgName,
                        "detachSwitchPorts": "",
                        "vlan": network['vlan'],
                        "dot1QVlan": 1,
                        "untagged": False,
                        "freeformConfig": "",
                        "deployment": True,
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
                        "deployment": True,
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
        print(f"attached interfaces to node {node['name']},{node['mgmt_ip']}")
        pprint.pprint(output)
    else:
        output = response.reason
        print(f" Error attaching interfaces to node {node['name']},{node['mgmt_ip']},{output}")

    payload_list = []


save = input('Do you want to save and deploy?[Y/N]')

if save.lower() == 'y' or save.lower() == 'yes':
    output = ndfc_modules.save_config(fabricName)
    print(output)

    output = ndfc_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')

