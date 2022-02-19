#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import pprint


if len(sys.argv) < 3:
    print(f'usage python {sys.argv[0]} fabric-name switch_name')
    sys.exit()
fabricName = sys.argv[1]
switchName = sys.argv[2]

if switchName.lower() == 'all':
    confirm = input(f'Do you really want to delete all the switches in the fabric {fabricName}? if yes confirm by typing "yes":')
    if confirm.lower() != 'yes':
        print('Exiting for not confirming!')
        sys.exit()
    elif confirm.lower() == 'yes':
        print(f'Deleting all the switches in the fabric {fabricName}')


username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest//control/fabrics/{fabricName}'
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}

response = requests.get(posturl, verify=False, headers=headers)
if response.status_code == 200:
    output = json.loads(response.text)

fabric_id = output['id']

posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest//control/fabrics/{fabric_id}/inventory'
response = requests.get(posturl, verify=False, headers=headers)
if response.status_code == 200:
    output = json.loads(response.text)

delete_node_list=[]
for item in output:
    out = dict(zip(item['displayHdrs'],item['displayValues']))
    if out['Name'].lower() == switchName.lower():
        delete_node = out['WWN']
    elif switchName.lower() == 'all':
        delete_node_list.append(out['WWN'])

try:
    if delete_node:
        deleteurl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest//control/fabrics/{fabricName}/switches/{delete_node}'
        response = requests.delete(deleteurl, verify=False, headers=headers)
        if response.status_code == 200:
            print(response.text)
        else:
            print('device node deleted',response.text)
except:
    if len(delete_node_list)>0:
        for delete_node in delete_node_list:
            deleteurl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest//control/fabrics/{fabricName}/switches/{delete_node}'
            response = requests.delete(deleteurl, verify=False, headers=headers)
            #print(response.text)
            if response.status_code == 200:
                print(response.text)
            else:
                print('device node deleted', response.text)






