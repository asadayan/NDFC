#!/usr/bin/python
# Author Ahamed Sadayan
# This python program adds vpc to VxLAN fabric through DCNM
# All the network name configured in the system should have the ability to identify with first 3 character prefix to focus
# only on those network prefixes. If all the network falls on the same prefix, then all the networks will be configured.

import ndfc_auth
import json
import requests
import ndfc_credentials
import ndfc_modules
import sys
import re
import pprint
import vpc_template
import time


username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/globalInterface'


fabricName = input('Enter the fabric Name: ')
vpc_type = input('Enter the vpc port_channel type (trunk,access or dot1qtunnel): ')
svpc = int(input('Enter the starting vPC port-channel number: '))
pair = input('Enter the vPC pair if a particular pair need to be configured or just enter to ignore (leaf1~leaf2): ')
excl = input('Enter the vpc pair to be excluded or just enter to be ignore leaf3~leaf4: ')
all = input('Type "all" if you want to configure all the vpc pair leafs in the fabric: ')
network_prefix = input('Enter the first 3 characters of the network created to configure only those network: ')
intf = input('Enter the physical interface list or range to be configured, symmetry across all leaf is assumed(e1/1-2,e3/8-9): ')
intf_range = ndfc_modules.get_intf_set(intf) # Convert the given interface range and discrete interface to elements of interface
intf = re.split(',',intf_range)
print(intf_range)
vpc_all_nodes = ndfc_modules.get_vpc_nodes(fabricName)
pairNodes = re.split('~',pair)
exclNodes = re.split('~',excl)

if vpc_type == 'trunk':
    vpc_dict = vpc_template.trunk
elif vpc_type == 'access':
    vpc_dict = vpc_template.access
elif vpc_type == 'dot1qtunnel':
    vpc_dict = vpc_template.dot1qtunnel

if len(pairNodes) == 2:
    pairLeaf =[]
    for item in vpc_all_nodes:
        if item['name'] == pairNodes[0] or item['name'] == pairNodes[1]:
            pairLeaf.append(item)
    vpc_nodes = pairLeaf

if len(exclNodes) == 2:
    vpc_but_excl =[]
    for item in vpc_all_nodes:
        if item['name'] != exclNodes[0] and item['name'] != exclNodes[1]:
            vpc_but_excl.append(item)
    vpc_nodes = vpc_but_excl


if all == 'all':
    vpc_nodes = vpc_all_nodes

interface = vpc_dict['interfaces'][0]
interface['fabricName'] = fabricName
interfaces =[]
deploy_vpc_list = []
vpc_node_list = []

for item in vpc_nodes:
    serial_no = item['serial_no']
    this_node = item['name']
    peer_node = item['nname']
    peer_serial_no = item['peer_serial_no']
    attach_intf = ''
    for Intf in intf:
        interface['nvPairs']['PEER1_MEMBER_INTERFACES'] = Intf
        interface['nvPairs']['PEER2_MEMBER_INTERFACES'] = Intf
        interface['serialNumber'] = f'{serial_no}~{peer_serial_no}'
        interface['ifName'] = f'vPC{svpc}'
        interface['nvPairs']['PEER1_PCID'] = str(svpc)
        interface['nvPairs']['PEER2_PCID'] = str(svpc)
        interface['nvPairs']['INTF_NAME'] = f'vPC{svpc}'
        interface['nvPairs'] = json.dumps(interface['nvPairs'])
        interfaces.append(interface)
        interface['nvPairs'] = json.loads(interface['nvPairs'])
        vpc_dict['interfaces'] = interfaces
        payload = vpc_dict
        #pprint.pprint(payload)
        response = requests.post(posturl,
                                 data=json.dumps(payload),
                                 verify=False,
                                 headers=headers)
        if response.status_code == 200:
            output = response.reason + '\n' + response.text
            print(f"VPC vPC{svpc} added with {Intf} on {this_node}--{peer_node}")
            pprint.pprint(output)
        else:
            output = response.reason + '\n' + response.text
            print(f" Error creating vPC{svpc} with {Intf} on {this_node}--{peer_node},{output}")
        interfaces=[]
        deploy_pair = { 'ifName': interface['ifName'],
                        'fabricName': fabricName,
                        'serialNumber' : interface['serialNumber']}
        deploy_vpc_list.append(deploy_pair)
        attach_intf += f'Port-channel{svpc},'
        svpc += 1
    vpc_node_list.append((serial_no, peer_serial_no, attach_intf[:-1],f'{this_node}--{peer_node}'))
    prev_peer_node = peer_node

print(f'Starting vpc deployment in the fabric {fabricName}')
fetch = 'all'
network_list = ndfc_modules.network_list(fabricName, fetch)
network_list_prefix = []
vpc_list = vpc_node_list
print(vpc_list[0])
for network in network_list:
    if network['network'].lower()[:3] == network_prefix.lower():
        network_list_prefix.append(network)

print('Attaching vpc port-channels to networks..')
#pprint.pprint(vpc_list)
ndfc_modules.attach_vpc_interface(fabricName,network_list_prefix,vpc_list)

save = input('Do you want to save and deploy?[Y/N]: ')

if save.lower() == 'y' or save.lower() == 'yes':
    output = ndfc_modules.save_config(fabricName)
    print(output)

    output = ndfc_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')
