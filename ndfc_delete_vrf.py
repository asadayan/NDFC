#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials
import sys
import ndfc_modules
import pprint


if len(sys.argv) < 3:
    print(f'usage python {sys.argv[0]} fabric-name vrf_name|all')
    sys.exit()
fabricName = sys.argv[1]
vrfName = sys.argv[2]
delete_vrf = vrfName
if vrfName.lower() == 'all':
    confirm = input(f'Do you really want to delete all the un deployed vrfs in the fabric {fabricName}? if yes confirm by typing "yes":')
    if confirm.lower() != 'yes':
        print('Exiting for not confirming!')
        sys.exit()
    elif confirm.lower() == 'yes':
        print(f'Deleting all the un deployed vrfs in the fabric {fabricName}')


username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization':ndfc_token, 'Content-Type': 'application/json'}
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/vrfs'
response = requests.get(posturl, verify=False, headers=headers)
if response.status_code == 200:
    output = json.loads(response.text)


all_vrf_list=[]
all_deployed_vrf=[]
all_undeployed_vrf = []
for item in output:
    all_vrf_list.append(item['vrfName'])
    if item['vrfStatus'].lower() == 'deployed':
        all_deployed_vrf.append(item['vrfName'])
    if item['vrfStatus'].lower() == 'na':
        all_undeployed_vrf.append(item['vrfName'])






if delete_vrf.lower() != 'all':
    deleteurl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/vrfs/{delete_vrf}'
    response = requests.delete(deleteurl, verify=False, headers=headers)
    if response.status_code == 200:
        print(f'vrf {delete_vrf} deleted',response.text)
    else:
        error = json.loads(response.text)
        print(f'Error deleting vrf {delete_vrf} ', error['message'])


elif len(all_undeployed_vrf)>0 and delete_vrf.lower() == 'all':
    for delete_vrf in all_undeployed_vrf:
        deleteurl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/vrfs/{delete_vrf}'
        try:
            response = requests.delete(deleteurl, verify=False, headers=headers)
            if response.status_code == 200:
                print(f' vrf {delete_vrf} deleted')
            else:
                print(f'Error deleting vrf {delete_vrf}')
        except:
            ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
            headers = {'Authorization':ndfc_token, 'Content-Type': 'application/json'}
            response = requests.delete(deleteurl, verify=False, headers=headers)
            if response.status_code == 200:
                print(f' vrf {delete_vrf} deleted')
            else:
                print(f'Error deleting vrf {delete_vrf}')



save = input('Do you want to save and deploy?[Y/N]')

if save.lower() == 'y' or save.lower() == 'yes':
    output = ndfc_modules.save_config(fabricName)
    print(output)

    output = ndfc_modules.deploy_config(fabricName)
    print(output)
else:
    print('Save separately ..')
