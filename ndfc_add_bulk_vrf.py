#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import vrf_template
import ndfc_modules
import pprint


if len(sys.argv) < 4:
    print(f'usage python {sys.argv[0]} fabric-name vrf_prefix start_l3vni number_of_vrf [DefaultRouteFlag] [HostRouteFlag] [StaticDefaultRouteFlag]')
    print("Example: python ndfc_add_vrf.py POC-FABRIC VRF 500001 100 0 1 0")
    print("In this above example, 100 vrf will be created with preifx of VRF name(VRF-1) with starting  L3 VNI 500001 will be created")
    print("enabling only host route to get advertised")
    sys.exit()

#print(sys.argv)
fabricName = str(sys.argv[1])
vrfprefix = str(sys.argv[2])
start_vrf_id = int(sys.argv[3])
number_of_vrf = int(sys.argv[4])
count = 1
vrfName = f'{vrfprefix}_{count}'
vrfId = start_vrf_id

vrf_dict = vrf_template.vrf
vrf_dict['fabric'] = fabricName
advertiseDefaultRouteFlag = 'false'
advertiseHostRouteFlag = 'false'
configureStaticDefaultRouteFlag = 'false'

if len(sys.argv) == 6:
    DefaultRouteFlag = int(sys.argv[5])
    if DefaultRouteFlag == 1: advertiseDefaultRouteFlag = 'true'
elif len(sys.argv) == 7:
    HostRouteFlag = int(sys.argv[6])
    DefaultRouteFlag = int(sys.argv[5])
    if HostRouteFlag == 1: advertiseHostRouteFlag = 'true'
    if DefaultRouteFlag == 1: advertiseDefaultRouteFlag = 'true'
elif len(sys.argv) == 8:
    StaticDefaultRouteFlag = int(sys.argv[7])
    HostRouteFlag = int(sys.argv[6])
    DefaultRouteFlag = int(sys.argv[5])
    if StaticDefaultRouteFlag == 1: configureStaticDefaultRouteFlag = 'true'
    if HostRouteFlag == 1: advertiseHostRouteFlag = 'true'
    if DefaultRouteFlag == 1: advertiseDefaultRouteFlag = 'true'

vrf_dict['vrfTemplateConfig']['advertiseDefaultRouteFlag'] = advertiseDefaultRouteFlag
vrf_dict['vrfTemplateConfig']['advertiseHostRouteFlag'] = advertiseHostRouteFlag
vrf_dict['vrfTemplateConfig']['configureStaticDefaultRouteFlag'] = configureStaticDefaultRouteFlag


#pprint.pprint(vrf_dict)


username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
for index in range(1,number_of_vrf+1):
    vrfId = str(start_vrf_id)
    vrfName = f'{vrfprefix}-{str(index).zfill(3)}'
    vrf_dict['vrfName'] = vrfName
    vrf_dict['vrfId'] = vrfId
    vrf_dict['vrfTemplateConfig']['vrfName'] = vrfName
    vrf_dict['vrfTemplateConfig']['vrfSegmentId'] = vrf_dict['vrfId']
    vrf_dict['vrfTemplateConfig'] = json.dumps(vrf_dict['vrfTemplateConfig'])
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/vrfs'
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    payload = vrf_dict
    #pprint.pprint(payload)
    response = requests.post(posturl,
                            data=json.dumps(payload),
                            verify=False,
                            headers=headers)
    if response.status_code == 200:
        output = response.text
        print(f'Fabric Name: {fabricName} VRF Name: {vrfName}  L3 VNI: {vrfId}  status: created')
    else:
        try:
            output = json.load(response.text)
            print(response.status_code)
            print(output["message"])
        except:
            output = response.text
            print(response.status_code)
            print(f'Error creating vrf {vrfName}')
    start_vrf_id += 1
    vrf_dict['vrfTemplateConfig'] = json.loads(vrf_dict['vrfTemplateConfig'])

save = input('Do you want to save and deploy?[Y/N]')

if save.lower() == 'y' or save.lower() == 'yes':
    output = ndfc_modules.save_config(fabricName)
    print(output)

    output = ndfc_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')

