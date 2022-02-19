#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import ndfc_modules
import sys
import network_template
import pprint
import re
import ipaddress
import ndfc_modules


ipv6_flag = 0
mul_flag = 0
fabricName = input('Enter the fabric Name: ')
apply_type = input('Do you want to create networks on all vrfs or only undeployed or vrf starting with certain prefix(all,undeployed,vrfprefix): ')
networkId = int(input('Enter the starting L2 VNI for the networks: '))
num_of_net_per_vrf = int(input('Enter number of networks per vrf: '))
svi_vlan = int(input('Enter the starting vlan for the networks: '))
ipv4_addr = input('Enter the starting ipv4 address for the networks: ')
ipv4_mask = int(input('Enter the ipv4 address mask: '))
ipv6_addr = input('Enter the starting ipv6 address for the networks to skip just press enter: ')
ipv6_mask = input('Enter the ipv6 address mask, to skip press enter: ')
suppressArp= input('Type YES/NO to enable disable arp suppression per network: ')
mul_address = input('Please enter the multicast address for BUM traffic to skip press enter: ')
if suppressArp.lower() == 'yes' or suppressArp.lower() == 'y':
    suppressArp = True
else:
    suppressArp = False


if apply_type.lower() == 'all':
    vrf_list=[]
    numVrf,vrf_list_all = ndfc_modules.vrf_list(fabricName,'all')
    for i in vrf_list_all:
        vrf_list.append(i[0])
elif apply_type.lower() == 'undeployed':
    numVrf, vrf_list = ndfc_modules.vrf_list(fabricName, 'undeployed')
    #print(vrf_list)
elif apply_type.lower() != all or apply_type.lower() != 'undeployed':
    vrf_list=[]
    numVrf,vrf_list_all = ndfc_modules.vrf_list(fabricName,'all')
    for i in vrf_list_all:
        if i[0].lower()[:3] == apply_type.lower():
            vrf_list.append(i[0])

vrf_list.sort()
#print(vrf_list)


network_dict = network_template.network
network_dict['fabric'] = fabricName
network_dict['networkTemplateConfig']['suppressArp'] = suppressArp
start_ipv4_address = ipaddress.ip_address(ipv4_addr)
if len(ipv6_addr) != 0:
    start_ipv6_address = ipaddress.ip_address(ipv6_addr)
    ipv6_flag = 1
if len(ipv6_mask) != 0:
    ipv6_mask = int(ipv6_mask)
if len(mul_address) != 0:
    mul_flag = 1
    multicast_address = ipaddress.ip_address(mul_address)
else:
    network_dict['networkTemplateConfig']['enableIR'] = True


username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks'

for vrfName in vrf_list:
    ipv4_address = start_ipv4_address
    if len(ipv6_addr) != 0:
        ipv6_address = start_ipv6_address
    for net in range(1,num_of_net_per_vrf+1):
        network_dict['vrf'] = vrfName
        network_dict['networkId'] = networkId
        network_dict['displayName'] = f'{vrfName}_NET_{networkId}'
        network_dict['networkName'] = network_dict['displayName']
        network_dict['networkTemplateConfig']['gatewayIpAddress'] = f'{str(ipv4_address)}/{ipv4_mask}'
        network_dict['networkTemplateConfig']['networkName'] = network_dict['displayName']
        network_dict['networkTemplateConfig']['segmentId'] = str(networkId)
        network_dict['networkTemplateConfig']['vrfName'] = vrfName
        network_dict['networkTemplateConfig']['vlanId'] = str(svi_vlan)
        network_dict['networkTemplateConfig']['suppressArp'] = suppressArp
        if ipv6_flag == 1:
            network_dict['networkTemplateConfig']['gatewayIpV6Address'] = f'{str(ipv6_address)}/{ipv6_mask}'
            ipv6_address += pow(2,128-ipv6_mask)
        else:
            network_dict['networkTemplateConfig']['gatewayIpV6Address'] = ""
        if mul_flag == 1:
            network_dict['networkTemplateConfig']['mcastGroup'] = str(multicast_address)
        else:
            network_dict['networkTemplateConfig']['mcastGroup'] = ""
        network_dict['networkTemplateConfig'] = json.dumps(network_dict['networkTemplateConfig'])
        svi_vlan += 1
        ipv4_address += pow(2,32-ipv4_mask)
        networkId += 1
        payload = network_dict
        response = requests.post(posturl,
                                 data=json.dumps(payload),
                                 verify=False,
                                 headers=headers)
        if response.status_code == 200:
            output = response.text
            print(f"Network {network_dict['displayName']} created under vrf {vrfName}")
        else:
            try:
                output = json.load(response.text)
                print(response.status_code)
                print(response.reason)
            except:
                output = response.text
                print(response.reason)
                print(output)
        #pprint.pprint(network_dict)
        network_dict['networkTemplateConfig'] = json.loads(network_dict['networkTemplateConfig'])
    start_ipv4_address += pow(2,32-ipv4_mask+8)
    if len(ipv6_addr) != 0:
        start_ipv6_address += pow(2,128-ipv6_mask+16)
    if mul_flag == 1:
        multicast_address += 1


save = input('Do you want to save and deploy?[Y/N]')

if save.lower() == 'y' or save.lower() == 'yes':
    output = ndfc_modules.save_config(fabricName)
    print(output)

    output = ndfc_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')

