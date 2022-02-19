#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_auth
import json
import requests
import ndfc_credentials

username = ndfc_credentials.username
password = ndfc_credentials.password
url = 'https://' + ndfc_credentials.node_ip
posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/msd/fabric-associations'
ndfc_token= ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
headers = {'Authorization':ndfc_token, 'Content-Type': 'application/json'}


response = requests.get(posturl, verify=False, headers=headers)
if response.status_code == 200:
    output = json.loads(response.text)


    for item in output:
        print(f'Fabric Name: {item["fabricName"]} \tFabric Type: {item["fabricTechnology"]}')
        posturl = url +f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{item["fabricName"]}/inventory'
        response = requests.get(posturl, verify=False, headers=headers)
        switches = json.loads(response.text)
        for switch in switches:
           print(f"Fabric Name: {switch['fabricName']}\t IP Address: {switch['ipAddress']}\t Serial Number: {switch['serialNumber']}" \
                 f"\t Switch Role: {switch['switchRole']}")

else:
    print(response.text)

