#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import network_template
import pprint
import ndfc_modules

if len(sys.argv) < 7:
    print(f'usage python {sys.argv[0]} fabric-name vrf_name l2vni svi_vlan ipv4_address [ipv6_address] [multicast_group] [supress_arp] ')
    print("Example: python ndfc_add_network.py POC-FABRIC VRF-RED 300001 1001 12.1.1.1/24 2001:1/64 224.1.1.2 1")
    print("In this above example, network under VRF-RED will be created with svi vlan 1001,L2 VNI 300001 wip ipv4 and ipv6 address and l2 bum multicast with arp supression flag")
    sys.exit()

#print(sys.argv)
fabricName = str(sys.argv[1])
vrfName = str(sys.argv[2])
networkId = str(sys.argv[3])
svi_vlan = sys.argv[4]
ipv4_address = sys.argv[5]
network_dict = network_template.network
network_dict['vrf'] = vrfName
network_dict['fabric'] = fabricName
network_dict['networkId'] = networkId
network_dict['displayName'] = f'{vrfName}_NET_{networkId}'
network_dict['networkName'] = network_dict['displayName']
network_dict['networkTemplateConfig']['gatewayIpAddress'] = ipv4_address
if len(sys.argv) == 7:
    ipv6_address = sys.argv[6]
    network_dict['networkTemplateConfig']['gatewayIpV6Address'] = ipv6_address
elif len(sys.argv) == 8:
    ipv6_address = sys.argv[6]
    network_dict['networkTemplateConfig']['gatewayIpV6Address'] = ipv6_address
    mul_address = sys.argv[7]
    network_dict['networkTemplateConfig']['mcastGroup'] = mul_address
elif len(sys.argv) == 9:
    ipv6_address = sys.argv[6]
    network_dict['networkTemplateConfig']['gatewayIpV6Address'] = ipv6_address
    mul_address = sys.argv[7]
    network_dict['networkTemplateConfig']['mcastGroup'] = mul_address
    supress_arp_flag = int(sys.argv[8])
    if supress_arp_flag == 1: suppressArp = 'true'
    if supress_arp_flag == 0: suppressArp = 'false'
    network_dict['networkTemplateConfig']['suppressArp'] = suppressArp

network_dict['networkTemplateConfig']['networkName'] = network_dict['displayName']
network_dict['networkTemplateConfig']['segmentId'] = networkId
network_dict['networkTemplateConfig']['vrfName'] = vrfName
network_dict['networkTemplateConfig']['vlanId'] = svi_vlan

network_dict['networkTemplateConfig'] = json.dumps(network_dict['networkTemplateConfig'])
pprint.pprint(network_dict)
username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
segurl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/managed-pool/fabrics/{fabricName}/segments/ids'
segpayload = {
            "segmentId": networkId
            }
response = requests.post(segurl,
                        data=json.dumps(segpayload),
                        verify=False,
                        headers=headers)
if response.status_code == 200:
    output = response.text
    print(f'{networkId} created:{output}')


mulurl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/managed-pool/fabrics/{fabricName}/multicast-group-address?segment-id={networkId}'
mulpayload = {
                "mcastGroupIpAddress": mul_address
                }
response = requests.post(mulurl,
                        data=json.dumps(mulpayload),
                        verify=False,
                        headers=headers)
if response.status_code == 200:
    output = response.text
    print(f'{mul_address} created:{output}')



posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks'
payload = network_dict
response = requests.post(posturl,
                        data=json.dumps(payload),
                        verify=False,
                        headers=headers)
if response.status_code == 200:
    output = response.text
    print(output)
else:
    try:
        output = json.load(response.text)
        print(response.reason)
    except:
        output = response.text
        print(response.reason)
        print(output)

save = input('Do you want to save and deploy?[Y/N]')

if save.lower() == 'y' or save.lower() == 'yes':
    output = ndfc_modules.save_config(fabricName)
    print(output)

    output = ndfc_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')

