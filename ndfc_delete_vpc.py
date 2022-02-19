#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import ndfc_modules
import pprint
import re

if len(sys.argv) < 2:
    print(f'usage python {sys.argv[0]} fabric-name [net-prefix]')
    sys.exit()

fabricName = sys.argv[1]
if len(sys.argv) == 3:
    netPrefix = str(sys.argv[2])

username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,ndfc_token,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
po_list = ndfc_modules.get_port_channels(fabricName)
#print(po_list)
payload_list =[]
for item in po_list:
    if  len(item['attached_net']) == 0 and int(item['vpc_id']) != 0:
        sr_no = re.split('~',item['vpc_pair_serial_no'])
        serialNum = f"{sr_no[0]}~{sr_no[1]}"
        payload =[{
                'ifName': item['vpc_name'],
                'serialNumber': serialNum
            }]
        payload_list.append(json.dumps(payload))
    elif len(sys.argv) == 3:
        for net in item['attached_net']:
          if net.lower()[:3] == netPrefix.lower()[:3]:
              sr_no = re.split('~', item['vpc_pair_serial_no'])
              serialNum = f"{sr_no[0]}~{sr_no[1]}"
              payload = [{
                  'ifName': item['vpc_name'],
                  'serialNumber': serialNum
              }]
              payload_list.append(json.dumps(payload))




posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/interface/markdelete'
for load in payload_list:
    response = requests.delete(posturl, data=load, verify=False, headers=headers)
    if response.status_code == 200:
        output = response.text
        pprint.pprint(f'Marked for deletion {load}')
    #else:
    #    print(f'Error deleting {load}',response.reason)

# posturl = url + 'f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/globalInterface/deploy'
# for load in payload_list:
#     response = requests.post(posturl, data=load, verify=False, headers=headers)
#     if response.status_code == 200:
#         output = response.text
#         pprint.pprint(f'Deletion Deployed {load}')
#     else:
#         print(f'Error deploying {load}',response.reason)


save = input('Do you want to save and deploy?[Y/N]: ')

if save.lower() == 'y' or save.lower() == 'yes':
    output = ndfc_modules.save_config(fabricName)
    print(output)

    output = ndfc_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')



