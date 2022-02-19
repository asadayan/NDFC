#!/usr/bin/python
# Author Ahamed Sadayan
# This python program adds vpc to VxLAN fabric through DCNM

import ndfc_auth
import json
import requests
import ndfc_credentials
import ndfc_modules
import sys
import re
import pprint
import argparse
import vpc_template
import time

my_parser = argparse.ArgumentParser(prog='ndfc_add_vpc',
                                    usage='%s(prog)s [options] path',
                                    description='Create VPC on a pair of leaf provided or all the fabric excluding certain leaf')

my_parser.add_argument('-f',
                       '--fabric',
                       required=True,
                       help='Name of the VxLAN Fabric')

my_parser.add_argument('-t',
                       '--type',
                       required=True,
                       help='VPC type, trunk, access or dot1qtunnel')

my_parser.add_argument('-s',
                       '--startvpc',
                       required=True,
                       help='Start VPC number')
my_parser.add_argument('-p',
                       '--pair',
                       required=True,
                       help='name of the first leaf in the pair')


my_parser.add_argument('-e',
                       '--exclude',
                       required=True,
                       help='name of the leaf(s) to exclude in the whole fabric')

my_parser.add_argument('-a',
                       '--all',
                       required=True,
                       help='all the leafs in the whole fabric')

my_parser.add_argument('-i',
                       '--intf',
                       required=True,
                       help='Interface example e1/1')

my_parser.add_argument('-px',
                       '--networkprefix',
                       required=True,
                       help='Interface example ibm')

username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/globalInterface'

args = my_parser.parse_args()
fabricName = args.fabric
vpc_type = args.type
svpc = int(args.startvpc)
pair = args.pair
excl = args.exclude
all = args.all
network_prefix = str(args.networkprefix)
intf_range = ndfc_modules.get_intf_set(args.intf) # Convert the given interface range and discrete interface to elements of interface
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
            output = response.text
            print(f"VPC vPC{svpc} added with {Intf} on {this_node}--{peer_node}")
            pprint.pprint(output)
        else:
            output = response.text
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
pprint.pprint(vpc_list)
ndfc_modules.attach_vpc_interface(fabricName,network_list_prefix,vpc_list)
output = ndfc_modules.save_config(fabricName)
print(output)

output = ndfc_modules.deploy_config(fabricName)
print(output)
