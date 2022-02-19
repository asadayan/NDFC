#!/usr/bin/python
# Author Ahamed Sadayan
# This python program adds vpc to VxLAN fabric through DCNM

import ndfc_auth
import ndfc_credentials
import ndfc_modules
import pprint
import sys


if len(sys.argv) < 3:
    print(f'usage python {sys.argv[0]} fabric-name network_prefix')
    print('Example python ndfc_detach_vpc  ibm|all')
    sys.exit()
fabricName = sys.argv[1]
network_prefix = sys.argv[2]
interface = ''


username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/globalInterface'


vpc_all_nodes = ndfc_modules.get_vpc_nodes(fabricName)
vpc_nodes = vpc_all_nodes
vpc_node_list = []

for item in vpc_nodes:
    serial_no = item['serial_no']
    this_node = item['name']
    peer_node = item['nname']
    peer_serial_no = item['peer_serial_no']
    attach_intf = ''
    vpc_node_list.append((serial_no, peer_serial_no, interface ,f'{this_node}--{peer_node}'))


print(f'Starting vpc detachment in the fabric {fabricName}')
network_list = ndfc_modules.network_list(fabricName, 'all')
print(network_list[0])
network_list_prefix = []
vpc_list = vpc_node_list
print(vpc_list[0])
for network in network_list:
    if network['network'].lower()[:3] == network_prefix.lower():
        network_list_prefix.append(network)

print('detaching vpc port-channels to networks..')
pprint.pprint(vpc_list)
ndfc_modules.detach_vpc_interface(fabricName,network_list_prefix,vpc_list)
output = ndfc_modules.save_config(fabricName)
print(output)

output = ndfc_modules.deploy_config(fabricName)
print(output)
