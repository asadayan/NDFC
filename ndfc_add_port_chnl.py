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
import argparse
import port_channel_template
import ipaddress
import time


username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/globalInterface'

fabricName = input('Enter the Fabric Name:')
port_channel_type = input('Enter the port_channel type, options are trunk, access, dot1qtunnel and routed: ')
sport_channel = int(input('Enter the starting port channel number: '))
standalone = input('Enter the leaf name if for specif leaf config, to skip press enter: ')
excl = input('Enter the leaf name to exclude certain leaf nodes, to skip press enter: ')
all = input('Enter all if you want to configure on all leaf nodes: ')
intf_per_chnl = int(input('Enter number of interfaces per port channel: '))
if int(intf_per_chnl) < 1 or int(intf_per_chnl) > 8:
    print('Invalid no_of_ports_per_chnl please retry with value from 1 to 8')
    sys.exit()
interface = input('Enter the interfaces used to create the port channel( symmentry of the port assumed across fabric): ')
network_prefix = input('Enter the first 3 characters of the networks created(net prefix): ')
intf_range = ndfc_modules.get_intf_set(interface) # Convert the given interface range and discrete interface to elements of interface
intf = re.split(',',intf_range)
int_per_chnl_list = []
intf_count = 0
intfChnl = ''
#print(intf_range)
for interface in intf:
    intfChnl += f'{interface},'
    intf_count += 1
    if intf_count == int(intf_per_chnl):
        int_per_chnl_list.append(intfChnl[:-1])
        intfChnl = ''
        intf_count = 0


print(int_per_chnl_list)
port_channel_all_nodes = ndfc_modules.get_leaf_nodes(fabricName)

if port_channel_type == 'trunk':
    port_channel_dict = port_channel_template.trunk
elif port_channel_type == 'access':
    port_channel_dict = port_channel_template.access
elif port_channel_type == 'dot1qtunnel':
    port_channel_dict = port_channel_template.dot1qtunnel
elif port_channel_type == 'routed':
    port_channel_dict = port_channel_template.routed_chnl
    vrf = input('Please enter the vrf name for the routed port channel: default if there is no vrf:')
    ip_add = input('Please enter the starting ipv4/ipv6 address for the routed port channel:')
    mask = input('Please enter ipv4/ipv6 address prefix length:')
    ip_address = ipaddress.ip_address(ip_add)


if standalone != 'None':
    port_channel_nodes = standalone

if excl !=  'None':
    port_channel_nodes = excl

if all == 'all':
    port_channel_nodes = port_channel_all_nodes

#pprint.pprint(port_channel_nodes)
#sys.exit()
interface = port_channel_dict['interfaces'][0]
interface['fabricName'] = fabricName
interfaces =[]
deploy_port_channel_list = []
port_channel_node_list = []
#pprint.pprint(port_channel_nodes)
#sys.exit()
for item in port_channel_nodes:
    serial_no = item['serial_no']
    this_node = item['name']
    peer_serial_no = item['peer_serial_no']
    attach_intf = ''
    for Intf in int_per_chnl_list:
        if port_channel_type == 'routed':
            interface['nvPairs']['INTF_VRF'] = vrf
            interface['nvPairs']['IP'] = str(ip_address)
            interface['nvPairs']['PREFIX'] = str(mask)
            if ip_address.version == 4:
                ip_address += pow(2,32-int(mask))
            elif ip_address.version == 6:
                ip_address += pow(2, 128 - int(mask))
        interface['serialNumber'] = f'{serial_no}'
        interface['ifName'] = f'Port-channel{sport_channel}'
        interface['nvPairs']['MEMBER_INTERFACES'] = Intf
        interface['nvPairs']['PO_ID'] = f'Port-channel{sport_channel}'
        interface['nvPairs'] = json.dumps(interface['nvPairs'])
        interfaces.append(interface)
        interface['nvPairs'] = json.loads(interface['nvPairs'])
        port_channel_dict['interfaces'] = interfaces
        payload = port_channel_dict
        #pprint.pprint(payload)
        #sys.exit()
        response = requests.post(posturl,
                                 data=json.dumps(payload),
                                 verify=False,
                                 headers=headers)
        if response.status_code == 200:
            output = response.reason + '\n' + response.text
            print(f"port_channel port_channel{sport_channel} added with {Intf} on {this_node}")
            pprint.pprint(output)
        else:
            output = response.reason + '\n' + response.text
            print(f" Error creating port_channel{sport_channel} with {Intf} on {this_node},{output}")
        interfaces=[]
        deploy_pair = { 'ifName': interface['ifName'],
                        'fabricName': fabricName,
                        'serialNumber' : interface['serialNumber']}
        deploy_port_channel_list.append(deploy_pair)
        attach_intf += f'Port-channel{sport_channel},'
        sport_channel += 1
    port_channel_node_list.append((serial_no, peer_serial_no, attach_intf[:-1],f'{this_node}',item['vpc_domain']))



if port_channel_type == 'routed':
    print('No Network attachments for L3 routed port channel..')
    sys.exit()
print(f'Starting port_channel deployment in the fabric {fabricName}')
fetch = 'all'
network_list = ndfc_modules.network_list(fabricName, fetch)
network_list_prefix = []
port_channel_list = port_channel_node_list
print(port_channel_list[0])
for network in network_list:
    if network['network'].lower()[:3] == network_prefix.lower():
        network_list_prefix.append(network)

print('Attaching port_channel port-channels to networks..')
#pprint.pprint(port_channel_list)
#sys.exit()
ndfc_modules.attach_port_channel_interface(fabricName,network_list_prefix,port_channel_list)
output = ndfc_modules.save_config(fabricName)
print(output)

output = ndfc_modules.deploy_config(fabricName)
print(output)
