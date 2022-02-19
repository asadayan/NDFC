#!/usr/bin/python
# Author Ahamed Sadayan
#DCNM modules to facilitate API calls

import ndfc_auth
import json
import requests
import ndfc_credentials
import re
import pprint
import time

def get_switch_role(serialNo):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/switches/roles?serialNumber={serialNo}'
    response = requests.get(posturl, verify=False, headers=headers)
    if response.status_code == 200:
        output = json.loads(response.text)
        return output[0]['role']


def vrf_list(fabricName,type='deployed'):
        username = ndfc_credentials.username
        password = ndfc_credentials.password
        url = 'https://' + ndfc_credentials.node_ip
        ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip,username,password)
        headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
        posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/vrfs'
        response = requests.get(posturl, verify=False, headers=headers)
        if response.status_code == 200:
            output = json.loads(response.text)

        all_vrf_list=[]
        all_deployed_vrf=[]
        all_undeployed_vrf = []
        for item in output:
            all_vrf_list.append((item['vrfName'],item['vrfStatus'],item['vrfId']))
            if item['vrfStatus'].lower() == 'deployed':
                all_deployed_vrf.append(item['vrfName'])
            if item['vrfStatus'].lower() == 'na' or item['vrfStatus'].lower() == 'pending':
                all_undeployed_vrf.append(item['vrfName'])


        Ndeployed =  len(all_deployed_vrf)
        Nundeployed = len(all_undeployed_vrf)
        Nall = len(all_vrf_list)
        response.close()
        if type.lower() == 'deployed':
            return (Ndeployed,all_deployed_vrf)
        elif type.lower() == 'undeployed':
            return (Nundeployed, all_undeployed_vrf)
        elif type.lower() == 'all':
            return (Nall,all_vrf_list)



def vrf(fabricName,vrfName):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/vrfs/{vrfName}'
    response = requests.get(posturl, verify=False, headers=headers)
    if response.status_code == 200:
        output = json.loads(response.text)
        output['vrfTemplateConfig'] = json.loads(output['vrfTemplateConfig'])
        response.close()
    return output


def network_list(fabricName,type='deployed'):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks'
    response = requests.get(posturl, verify=False, headers=headers)
    if response.status_code == 200:
        output = json.loads(response.text)
        print('Network information fetched')

    all_network_list = []
    all_deployed_network = []
    all_undeployed_network = []
    all_pending_network = []
    for item in output:
        netcfg = json.loads(item['networkTemplateConfig'])
        all_network_list.append({'vrf':item['vrf'], 'network':item['displayName'],
                                         'ipv4_add':netcfg['gatewayIpAddress'],
                                         'vlan':netcfg['vlanId'], 'ipv6_add':netcfg['gatewayIpV6Address']})
        if item['networkStatus'].lower() == 'deployed':
            all_deployed_network.append({'vrf':item['vrf'], 'network':item['displayName'],
                                         'ipv4_add':netcfg['gatewayIpAddress'],
                                         'vlan':netcfg['vlanId'], 'ipv6_add':netcfg['gatewayIpV6Address']})
        if item['networkStatus'].lower() != 'deployed':
            all_undeployed_network.append({'vrf':item['vrf'], 'network':item['displayName'],
                                         'ipv4_add':netcfg['gatewayIpAddress'],
                                         'vlan':netcfg['vlanId'], 'ipv6_add':netcfg['gatewayIpV6Address']})
        if item['networkStatus'].lower() == 'pending':
            all_pending_network.append({'vrf':item['vrf'], 'network':item['displayName'],
                                         'ipv4_add':netcfg['gatewayIpAddress'],
                                         'vlan':netcfg['vlanId'], 'ipv6_add':netcfg['gatewayIpV6Address']})
    response.close()
    #print(type)
    if type.lower() == 'deployed':
        print('returning deployed network list')
        return all_deployed_network
    elif type.lower() == 'undeployed':
        print('returning undeployed network list')
        return all_undeployed_network
    elif type.lower() == 'all':
        print('returning all network list')
        return all_network_list
    elif type.lower() == 'pending':
        print('returning pending network list')
        return all_pending_network

def network_list_raw(fabricName):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks'
    response = requests.get(posturl, verify=False, headers=headers)
    if response.status_code == 200:
        output = json.loads(response.text)
        print('Network information fetched')
    else:
        output = response.reason
    return output

def is_net_in_intf(fabricName,netWork):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks'
    response = requests.get(posturl, verify=False, headers=headers)
    if response.status_code == 200:
        output = json.loads(response.text)
        print('Network information fetched')
        for item in output:
            if netWork in item['attached_net']:
                return True
        return False
    else:
        output = response.reason
        print(output)
        return -1




def get_leaf_nodes(fabricName,raw=0):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}'
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    try:
        response = requests.get(posturl, verify=False, headers=headers)
        if response.status_code == 200:
            output = json.loads(response.text)
        fabric_id = output['id']
    except Exception as e:
        print(e.message,response.reason)
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_id}/inventory'
    try:
        response = requests.get(posturl, verify=False, headers=headers)
        if response.status_code == 200:
            output = json.loads(response.text)
            response.close()
        else:
            print('error getting leaf vpc  nodes')
            return -1
    except Exception as e:
        print(e.message,response.reason)
    if raw == 1:
        return output
    leaf_nodes=[]
    for index, leaf in enumerate(output):
        leaf_dict = {}
        if leaf['switchRole'].lower() == 'leaf':
            leaf_dict['name'] = leaf['logicalName']
            leaf_dict['mgmt_ip'] = leaf['ipAddress']
            leaf_dict['serial_no'] = leaf['serialNumber']
            leaf_dict['model'] = leaf['nonMdsModel']
            leaf_dict['uptime'] = leaf['upTimeStr']
            leaf_dict['fabric'] = leaf['fabricName']
            leaf_dict['vpc'] = leaf['isVpcConfigured']
            leaf_dict['vpc_domain'] = leaf['vpcDomain']
            leaf_dict['vpc_role'] = leaf['role']
            leaf_dict['vpc_peer'] = leaf['peer']
            if int(leaf['vpcDomain']) == 0:
                leaf_dict['nname'] = None
                leaf_dict['peer_mgmt_ip'] = None
                leaf_dict['peer_serial_no'] = 0
                leaf_dict['peer_model'] = None
                leaf_dict['peer_vpc_role'] = None
                leaf_nodes.append(leaf_dict)
            for new_index, value in enumerate(output):
                if leaf['logicalName'] == output[new_index]['peer']:
                    leaf_dict['nname'] = output[new_index]['logicalName']
                    leaf_dict['peer_mgmt_ip'] = output[new_index]['ipAddress']
                    leaf_dict['peer_serial_no'] =  output[new_index]['serialNumber']
                    leaf_dict['peer_model'] = output[new_index]['nonMdsModel']
                    leaf_dict['peer_vpc_role'] =  output[new_index]['role']
                    leaf_nodes.append(leaf_dict)


    return(leaf_nodes)


def get_leaf_serial_no(fabricName,leafname):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}'
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    try:
        response = requests.get(posturl, verify=False, headers=headers)
        if response.status_code == 200:
            output = json.loads(response.text)
        fabric_id = output['id']
    except Exception as e:
        print(e.message,response.reason)
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_id}/inventory'
    try:
        response = requests.get(posturl, verify=False, headers=headers)
        if response.status_code == 200:
            output = json.loads(response.text)
            response.close()
        else:
            print('error getting leaf nodes')
            return -1
    except Exception as e:
        print(e.message,response.reason)
    for index, leaf in enumerate(output):
        if leaf['switchRole'].lower() == 'leaf':
            if leaf['logicalName'] == leafname:
                return leaf['serialNumber']
    print('Leaf Name Invalid or SerialNumber not Found in Database')
    return 0

def get_spine_serial_no(fabricName,spinename):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}'
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    try:
        response = requests.get(posturl, verify=False, headers=headers)
        if response.status_code == 200:
            output = json.loads(response.text)
        fabric_id = output['id']
    except Exception as e:
        print(e.message,response.reason)
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_id}/inventory'
    try:
        response = requests.get(posturl, verify=False, headers=headers)
        if response.status_code == 200:
            output = json.loads(response.text)
            response.close()
        else:
            print('error getting spine nodes')
            return -1
    except Exception as e:
        print(e.message,response.reason)

    for index, spine in enumerate(output):
        if spine['switchRole'].lower() == 'spine':
            if spine['logicalName'] == spinename:
                return spine['serialNumber']
    print('Spine Name Invalid or SerialNumber not Found in Database')
    return 0

def get_node_serial_no(fabricName,nodename):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}'
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    try:
        response = requests.get(posturl, verify=False, headers=headers)
        if response.status_code == 200:
            output = json.loads(response.text)
        fabric_id = output['id']
    except Exception as e:
        print(e.message,response.reason)
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_id}/inventory'
    try:
        response = requests.get(posturl, verify=False, headers=headers)
        if response.status_code == 200:
            output = json.loads(response.text)
            response.close()
        else:
            print('error getting  nodes')
            return -1
    except Exception as e:
        print(e.message,response.reason)
    for index, node in enumerate(output):
            if node['logicalName'] == nodename:
                return node['serialNumber']
    print('Node Name Invalid or SerialNumber not Found in Database')
    return 0

def get_vpc_nodes(fabricName):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}'
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    try:
        response = requests.get(posturl, verify=False, headers=headers)
        if response.status_code == 200:
            output = json.loads(response.text)
        fabric_id = output['id']
    except Exception as e:
        print(e.message,response.reason)
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_id}/inventory'
    try:
        response = requests.get(posturl, verify=False, headers=headers)
        if response.status_code == 200:
            output = json.loads(response.text)
            response.close()
        else:
            print('error getting leaf vpc  nodes')
            return -1
    except Exception as e:
        print(e.message,response.reason)
    leaf_nodes=[]
    leaf_dict = {}
    for index, leaf in enumerate(output):
        for new_index in range(index+1,len(output)):
            if leaf['logicalName'] == output[new_index]['peer']:
                leaf_dict['name'] = leaf['logicalName']
                leaf_dict['nname'] = output[new_index]['logicalName']
                leaf_dict['mgmt_ip'] = leaf['ipAddress']
                leaf_dict['peer_mgmt_ip'] = output[new_index]['ipAddress']
                leaf_dict['serial_no'] = leaf['serialNumber']
                leaf_dict['peer_serial_no'] =  output[new_index]['serialNumber']
                leaf_dict['model'] = leaf['nonMdsModel']
                leaf_dict['peer_model'] = output[new_index]['nonMdsModel']
                leaf_dict['uptime'] = leaf['upTimeStr']
                leaf_dict['fabric'] = leaf['fabricName']
                leaf_dict['vpc'] = leaf['isVpcConfigured']
                leaf_dict['vpc_domain'] = leaf['vpcDomain']
                leaf_dict['vpc_role'] = leaf['role']
                leaf_dict['peer_vpc_role'] =  output[new_index]['role']
                leaf_dict['vpc_peer'] = leaf['peer']
                leaf_nodes.append(leaf_dict)
        leaf_dict={}
    return(leaf_nodes)


def get_spine_nodes(fabricName):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}'
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    response = requests.get(posturl, verify=False, headers=headers)
    if response.status_code == 200:
        output = json.loads(response.text)
    fabric_id = output['id']
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabric_id}/inventory'
    response = requests.get(posturl, verify=False, headers=headers)
    if response.status_code == 200:
        output = json.loads(response.text)
        response.close()
    else:
        print('error getting spine nodes')
        return -1
    spine_nodes=[]
    spine_dict = {}
    for spine in output:
        if spine['switchRole'].lower() == 'spine':
            spine_dict['name'] = spine['logicalName']
            spine_dict['mgmt_ip'] = spine['ipAddress']
            spine_dict['serial_no'] = spine['serialNumber']
            spine_dict['model'] = spine['nonMdsModel']
            spine_dict['uptime'] = spine['upTimeStr']
            spine_dict['fabric'] = spine['fabricName']
            spine_nodes.append(spine_dict)
        spine_dict = {}
    return (spine_nodes)


def get_serial_num(leaf_nodes,leaf):
    for item in leaf_nodes:
        if item['name'] == leaf:
            return item['serial_no']

def get_intf_set(intf_range,type='short'):
    interface = ''
    port_range = re.findall('[Eethrnt](\d+)/(\d+)-(\d+)', intf_range)
    if len(port_range) != 0:
        for item in port_range:
            for port in range(int(item[1]), int(item[2]) + 1):
                if type == 'long':
                    interface += f'Ethernet{item[0]}/{port},'
                elif type == 'short':
                    interface += f'e{item[0]}/{port},'

    port = re.findall('[Eethrnt](\d+)/(\d+(,|$))', intf_range)
    if len(port) != 0:
        for item in port:
            if type == 'long':
                interface += f'Ethernet{item[0]}/{item[1]}'
            elif type == 'short':
                interface += f'e{item[0]}/{item[1]}'
    if interface[-1] == ',':
        return interface[:-1]
    else:
        return interface


def get_port_channels(fabricName,attached_net_len = -1):
    from ndfc_modules import get_switch_role
    from ndfc_modules import get_leaf_nodes
    leaf_nodes = get_leaf_nodes(fabricName)
    leafs_serial = []
    for i in leaf_nodes:
        leafs_serial.append(i['serial_no'])
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}'
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    response1 = requests.get(posturl, verify=False, headers=headers)
    fabric = json.loads(response1.text)
    fabric_id = fabric['id']
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/globalInterface/?navId={fabric_id}'
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    response = requests.get(posturl, verify=False, headers=headers)
    po_list = []
    attached_net =[]
    po_list_per_attached_net = []
    if response.status_code == 200:
        output = json.loads(response.text)
        #pprint.pprint(output)
        print('Checking all the interface types in the fabric..')
        for item in output:
            if item['serialNo'] in leafs_serial and  item['underlayPoliciesStr'] != None and item['ifType'].upper() == 'INTERFACE_PORT_CHANNEL':
                po_type = re.findall('vpc_peer_link',item['underlayPoliciesStr'])
                if len(po_type) > 0:
                    peer_link = True
                else:
                    peer_link = False
                    port_channel = {'leaf': item['sysName'], 'serial_no': item['serialNo'],
                                    'vpc_id': item['vpcId'], 'po_name': item['underlayPolicies'][0]['entityName'],
                                    'source': item['underlayPolicies'][0]['source'],
                                    'po_member_list': item['portChannelMemberList'],
                                    'vpc_pair_serial_no': item['vpcEntityId'], 'vrf': item['vrf'],
                                    'vpc_name': item['underlayPolicies'][0]['source'],
                                    'if_type': item['ifType'],'interfaceDbId': item['interfaceDbId'],
                                    'po_policy': item['underlayPoliciesStr']
                                    }
                    if len(item['overlayNetwork']) > 0:
                        for net in item['overlayNetwork']:
                            attached_net.append(net['templateName'])
                        port_channel['attached_net'] = attached_net
                    else:
                        port_channel['attached_net'] = []

                    po_list.append(port_channel)
    if attached_net_len == -1:
        #pprint.pprint(po_list)
        return po_list
    elif attached_net_len >= 0:
        for po in po_list:
            if len(po['attached_net']) == attached_net_len:
                po_list_per_attached_net.append(po)
        return po_list_per_attached_net



def get_interface(fabricName):
    fabricName = fabricName
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/globalInterface/'
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    response = requests.get(posturl, verify=False, headers=headers)
    if response.status_code == 200:
        output = json.loads(response.text)
    else:
        output = response.reason
    intf_list = []
    for item in output:
        if item['fabricName'] == fabricName:
            intf_list.append(item)
    return intf_list



def attach_vpc_interface(fabricName,network_list,vpc_intf_list):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
    for network in network_list:
        payload_list = []
        for index, vpc in enumerate(vpc_intf_list):
            serial_no = vpc[0]
            peer_serial_no = vpc[1]
            interface = vpc[2]
            lanattach =[{
                "fabric": fabricName,
                "networkName": network['network'],
                "serialNumber": serial_no,
                "switchPorts": interface,
                "detachSwitchPorts": "",
                "vlan": network['vlan'],
                "dot1QVlan": 1,
                "untagged": False,
                "freeformConfig": "",
                "deployment": True,
                "extensionValues": "",
                "instanceValues": ""
            },
                {
                "fabric": fabricName,
                "networkName": network['network'],
                "serialNumber": peer_serial_no,
                "switchPorts": interface,
                "detachSwitchPorts": "",
                "vlan": network['vlan'],
                "dot1QVlan": 1,
                "untagged": False,
                "freeformConfig": "",
                "deployment": True,
                "extensionValues": "",
                "instanceValues": ""
            }]
            payload = {
                "networkName": network['network']
            }
            payload["lanAttachList"] = lanattach
            payload_list.append(payload)
            #pprint.pprint(payload_list)
            try:
                response = requests.post(posturl,
                                     data=json.dumps(payload_list),
                                     verify=False,
                                     headers=headers)
                time.sleep(0.5)
                if response.status_code == 200:
                    output = json.loads(response.text)
                    pprint.pprint(output)
                    print(f"Interface {interface} with VLAN {network['vlan']} attached to {vpc[3]}")
                else:
                    output = response.reason
                    if output.strip() == 'Unauthorized':
                        ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
                        headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
                        posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
                        time.sleep(0.5)
                        response = requests.post(posturl,
                                                 data=json.dumps(payload_list),
                                                 verify=False,
                                                 headers=headers)
                        if response.status_code == 200:
                            output = json.loads(response.text)
                            pprint.pprint(output)
                            print(f"Interface {interface} with VLAN {network['vlan']} attached to {vpc[3]}")
                        else:
                            print(f" Error attaching {interface} with VLAN {network['vlan']} to node {vpc[3]},{output}")
                    else:
                        print(f" Error attaching {interface} with VLAN {network['vlan']} to node {vpc[3]}, {output}")
            except:
                ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
                headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
                posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
                response = requests.post(posturl,
                                         data=json.dumps(payload_list),
                                         verify=False,
                                         headers=headers)
                time.sleep(0.5)
                if response.status_code == 200:
                    output = json.loads(response.text)
                    pprint.pprint(output)
                    print(f"Interface {interface} with VLAN {network['vlan']} attached to {vpc[3]}")
                else:
                    print(f" Error attaching {interface} with VLAN {network['vlan']} to node {vpc[3]}, {output}")


    response.close()



def detach_vpc_interface(fabricName,network_list,vpc_intf_list):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
    for network in network_list:
        payload_list = []
        for index, vpc in enumerate(vpc_intf_list):
            serial_no = vpc[0]
            peer_serial_no = vpc[1]
            interface = vpc[2]
            lanattach =[{
                "fabric": fabricName,
                "networkName": network['network'],
                "serialNumber": serial_no,
                "switchPorts": "",
                "detachSwitchPorts": "",
                "vlan": "",
                "dot1QVlan": 1,
                "untagged": False,
                "freeformConfig": "",
                "deployment": False,
                "extensionValues": "",
                "instanceValues": ""
            },
                {
                "fabric": fabricName,
                "networkName": network['network'],
                "serialNumber": peer_serial_no,
                "switchPorts": "",
                "detachSwitchPorts": "",
                "vlan": "",
                "dot1QVlan": 1,
                "untagged": False,
                "freeformConfig": "",
                "deployment": False,
                "extensionValues": "",
                "instanceValues": ""
            }]
            payload = {
                "networkName": network['network']
            }
            payload["lanAttachList"] = lanattach
            payload_list.append(payload)
            #pprint.pprint(payload_list)
            try:
                response = requests.post(posturl,
                                     data=json.dumps(payload_list),
                                     verify=False,
                                     headers=headers)
                time.sleep(0.5)
                if response.status_code == 200:
                    output = json.loads(response.text)
                    pprint.pprint(output)
                    print(f"Interface {interface} with VLAN {network['vlan']} detached to {vpc[3]}")
                else:
                    output = response.reason
                    if output.strip() == 'Unauthorized':
                        ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
                        headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
                        posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
                        time.sleep(0.5)
                        response = requests.post(posturl,
                                                 data=json.dumps(payload_list),
                                                 verify=False,
                                                 headers=headers)
                        if response.status_code == 200:
                            output = json.loads(response.text)
                            pprint.pprint(output)
                            print(f"Interface {interface} with VLAN {network['vlan']} detached to {vpc[3]}")
                        else:
                            print(f" Error detaching {interface} with VLAN {network['vlan']} to node {vpc[3]},{output}")
                    else:
                        print(f" Error detaching {interface} with VLAN {network['vlan']} to node {vpc[3]}, {output}")
            except:
                ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
                headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
                posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
                response = requests.post(posturl,
                                         data=json.dumps(payload_list),
                                         verify=False,
                                         headers=headers)
                time.sleep(0.5)
                if response.status_code == 200:
                    output = json.loads(response.text)
                    pprint.pprint(output)
                    print(f"Interface {interface} with VLAN {network['vlan']} detached to {vpc[3]}")
                else:
                    print(f" Error detaching {interface} with VLAN {network['vlan']} to node {vpc[3]}, {output}")


    response.close()


def save_config(fabricName):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    save_url = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}/config-save'
    response = requests.post(save_url, verify=False, headers=headers)
    if response.status_code == 200:
        output = response.text
        print('Saved Config')
    else:
        output = response.reason
        print(f'Error in Saving {response.reason}')
    return output


def deploy_config(fabricName):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    deploy_cfg = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/control/fabrics/{fabricName}/config-deploy'
    response = requests.post(deploy_cfg, verify=False, headers=headers)
    if response.status_code == 200:
        output = response.text
        print('Deployed Config')
    else:
        output = response.reason
        print(f'Error in Deploying {response.reason}')
    return output

def attach_port_channel_interface(fabricName,network_list,po_intf_list):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
    for network in network_list:
        payload_list = []
        for index, po in enumerate(po_intf_list):
            serial_no = po[0]
            peer_serial_no = po[1]
            interface = po[2]
            vpc_domain = po[4]
            lanattach = []
            pair1 = {
                "fabric": fabricName,
                "networkName": network['network'],
                "serialNumber": serial_no,
                "switchPorts": interface,
                "detachSwitchPorts": "",
                "vlan": network['vlan'],
                "dot1QVlan": 1,
                "untagged": False,
                "freeformConfig": "",
                "deployment": True,
                "extensionValues": "",
                "instanceValues": ""
            }
            lanattach.append(pair1)
            if int(vpc_domain) != 0:
                pair2 = {
                        "fabric": fabricName,
                        "networkName": network['network'],
                        "serialNumber": peer_serial_no,
                        "switchPorts":"",
                        "detachSwitchPorts": "",
                        "vlan": network['vlan'],
                        "dot1QVlan": 1,
                        "untagged": False,
                        "freeformConfig": "",
                        "deployment": True,
                        "extensionValues": "",
                        "instanceValues": ""
                    }
                lanattach.append(pair2)
            pair3 = {
                "fabric": fabricName,
                "networkName": network['network'],
                "serialNumber": peer_serial_no,
                "switchPorts": "",
                "detachSwitchPorts": "",
                "vlan": network['vlan'],
                "dot1QVlan": 1,
                "untagged": False,
                "freeformConfig": "",
                "deployment": True,
                "extensionValues": "",
                "instanceValues": ""
            }
            payload = {
                "networkName": network['network']
            }
            payload["lanAttachList"] = lanattach
            payload_list.append(payload)
            #pprint.pprint(payload_list)
            try:
                response = requests.post(posturl,
                                     data=json.dumps(payload_list),
                                     verify=False,
                                     headers=headers)
                time.sleep(0.5)
                if response.status_code == 200:
                    output = json.loads(response.text)
                    pprint.pprint(output)
                    print(f"Interface {interface} with VLAN {network['vlan']} attached to {po[3]}")
                else:
                    output = response.reason
                    if output.strip() == 'Unauthorized':
                        ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
                        headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
                        posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
                        time.sleep(0.5)
                        response = requests.post(posturl,
                                                 data=json.dumps(payload_list),
                                                 verify=False,
                                                 headers=headers)
                        if response.status_code == 200:
                            output = json.loads(response.text)
                            pprint.pprint(output)
                            print(f"Interface {interface} with VLAN {network['vlan']} attached to {po[3]}")
                        else:
                            print(f" Error attaching {interface} with VLAN {network['vlan']} to node {po[3]},{output}")
                    else:
                        print(f" Error attaching {interface} with VLAN {network['vlan']} to node {po[3]}, {output}")
            except:
                ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
                headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
                posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
                response = requests.post(posturl,
                                         data=json.dumps(payload_list),
                                         verify=False,
                                         headers=headers)
                time.sleep(0.5)
                if response.status_code == 200:
                    output = json.loads(response.text)
                    pprint.pprint(output)
                    print(f"Interface {interface} with VLAN {network['vlan']} attached to {po[3]}")
                else:
                    print(f" Error attaching {interface} with VLAN {network['vlan']} to node {po[3]}, {output}")


    response.close()



def detach_port_channel_interface(fabricName,network_list,po_intf_list):
    username = ndfc_credentials.username
    password = ndfc_credentials.password
    url = 'https://' + ndfc_credentials.node_ip
    ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
    headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
    posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
    for network in network_list:
        payload_list = []
        for index, po in enumerate(po_intf_list):
            serial_no = po[0]
            peer_serial_no = po[1]
            interface = po[2]
            vpc_domain = po[4]
            lanattach = []
            pair1 = {
                "fabric": fabricName,
                "networkName": network['network'],
                "serialNumber": serial_no,
                "switchPorts": "",
                "detachSwitchPorts": "",
                "vlan": network['vlan'],
                "dot1QVlan": 1,
                "untagged": False,
                "freeformConfig": "",
                "deployment": False,
                "extensionValues": "",
                "instanceValues": ""
            }
            lanattach.append(pair1)
            if int(vpc_domain) != 0:
                pair2 = {
                    "fabric": fabricName,
                    "networkName": network['network'],
                    "serialNumber": peer_serial_no,
                    "switchPorts": "",
                    "detachSwitchPorts": "",
                    "vlan": network['vlan'],
                    "dot1QVlan": 1,
                    "untagged": False,
                    "freeformConfig": "",
                    "deployment": False,
                    "extensionValues": "",
                    "instanceValues": ""
                }
                lanattach.append(pair2)
            payload = {
                "networkName": network['network']
            }
            payload["lanAttachList"] = lanattach
            payload_list.append(payload)
            #pprint.pprint(payload_list)
            try:
                response = requests.post(posturl,
                                     data=json.dumps(payload_list),
                                     verify=False,
                                     headers=headers)
                time.sleep(0.5)
                if response.status_code == 200:
                    output = json.loads(response.text)
                    pprint.pprint(output)
                    print(f"Interface {interface} with VLAN {network['vlan']} detached to {po[3]}")
                else:
                    output = response.reason
                    if output.strip() == 'Unauthorized':
                        ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
                        headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
                        posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
                        time.sleep(0.5)
                        response = requests.post(posturl,
                                                 data=json.dumps(payload_list),
                                                 verify=False,
                                                 headers=headers)
                        if response.status_code == 200:
                            output = json.loads(response.text)
                            pprint.pprint(output)
                            print(f"Interface {interface} with VLAN {network['vlan']} detached to {po[3]}")
                        else:
                            print(f" Error detaching {interface} with VLAN {network['vlan']} to node {po[3]},{output}")
                    else:
                        print(f" Error detaching {interface} with VLAN {network['vlan']} to node {po[3]}, {output}")
            except:
                ndfc_token = ndfc_auth.auth(ndfc_credentials.node_ip, username, password)
                headers = {'Authorization': ndfc_token, 'Content-Type': 'application/json'}
                posturl = url + f'/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics/{fabricName}/networks/attachments'
                response = requests.post(posturl,
                                         data=json.dumps(payload_list),
                                         verify=False,
                                         headers=headers)
                time.sleep(0.5)
                if response.status_code == 200:
                    output = json.loads(response.text)
                    pprint.pprint(output)
                    print(f"Interface {interface} with VLAN {network['vlan']} detached to {po[3]}")
                else:
                    print(f" Error detaching {interface} with VLAN {network['vlan']} to node {po[3]}, {output}")


    response.close()
