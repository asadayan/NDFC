#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import vrf_template
import pprint
import ndfc_modules

if len(sys.argv) < 4:
    print(f'usage python {sys.argv[0]} fabric-name vrf_name l3vni [DefaultRouteFlag] [HostRouteFlag] [StaticDefaultRouteFlag]')
    print("Example: python ndfc_add_vrf.py POC-FABRIC VRF-RED 500001 0 1 0")
    print("In this above example, VRF-RED will be created with L3 VNI 500001 enabling only host route to get advertised")
    sys.exit()

#print(sys.argv)
fabricName = str(sys.argv[1])
vrfName = str(sys.argv[2])
vrfId = str(sys.argv[3])
vrf_dict = vrf_template.vrf
vrf_dict['vrfName'] = vrfName
vrf_dict['fabric'] = fabricName
vrf_dict['vrfId'] = vrfId
vrf_dict['vrfTemplateConfig']['vrfName'] = vrfName
vrf_dict['vrfTemplateConfig']['vrfSegmentId'] = vrf_dict['vrfId']
advertiseDefaultRouteFlag = 'false'
advertiseHostRouteFlag = 'false'
configureStaticDefaultRouteFlag = 'false'

if len(sys.argv) == 5:
    DefaultRouteFlag = int(sys.argv[4])
    if DefaultRouteFlag == 1: advertiseDefaultRouteFlag = 'true'
elif len(sys.argv) == 6:
    HostRouteFlag = int(sys.argv[5])
    DefaultRouteFlag = int(sys.argv[4])
    if HostRouteFlag == 1: advertiseHostRouteFlag = 'true'
    if DefaultRouteFlag == 1: advertiseDefaultRouteFlag = 'true'
elif len(sys.argv) == 7:
    StaticDefaultRouteFlag = int(sys.argv[6])
    HostRouteFlag = int(sys.argv[5])
    DefaultRouteFlag = int(sys.argv[4])
    if StaticDefaultRouteFlag == 1: configureStaticDefaultRouteFlag = 'true'
    if HostRouteFlag == 1: advertiseHostRouteFlag = 'true'
    if DefaultRouteFlag == 1: advertiseDefaultRouteFlag = 'true'

vrf_dict['vrfTemplateConfig']['advertiseDefaultRouteFlag'] = advertiseDefaultRouteFlag
vrf_dict['vrfTemplateConfig']['advertiseHostRouteFlag'] = advertiseHostRouteFlag
vrf_dict['vrfTemplateConfig']['configureStaticDefaultRouteFlag'] = configureStaticDefaultRouteFlag
vrf_dict['vrfTemplateConfig'] = json.dumps(vrf_dict['vrfTemplateConfig'])

pprint.pprint(vrf_dict)


username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/vrfs'
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization':ndfc_token, 'Content-Type': 'application/json'}
payload = vrf_dict


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
        print(response.status_code)
        print(output)
    except:
        output = response.text
        print(response.reason)


save = input('Do you want to save and deploy?[Y/N]')

if save.lower() == 'y' or save.lower() == 'yes':
    output = ndfc_modules.save_config(fabricName)
    print(output)

    output = ndfc_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')
