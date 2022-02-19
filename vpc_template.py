#!/usr/bin/python
# Author Ahamed Sadayan
# Template for http post VPC creation
# After import make changes to the releavent field



access = {
    "policy": "int_vpc_access_host_11_1",
    "interfaceType": "INTERFACE_VPC",
    "interfaces": [
        {
            "serialNumber": "FDO242109B1~FDO234602KX",
            "interfaceType": "INTERFACE_VPC",
            "ifName": "vPC2",
            "fabricName": "IBM_VxLAN_Fabric",
            "nvPairs": {
                "PEER1_PCID": "2",
                "PEER2_PCID": "2",
                "PEER1_MEMBER_INTERFACES": "e1/9",
                "PEER2_MEMBER_INTERFACES": "e1/9",
                "PC_MODE": "active",
                "BPDUGUARD_ENABLED": "True",
                "PORTTYPE_FAST_ENABLED": True,
                "MTU": "jumbo",
                "PEER1_ACCESS_VLAN": "",
                "PEER2_ACCESS_VLAN": "",
                "PEER1_PO_DESC": "",
                "PEER2_PO_DESC": "",
                "PEER1_PO_CONF": "",
                "PEER2_PO_CONF": "",
                "ADMIN_STATE": True,
                "INTF_NAME": "vPC2"
            }
        }
    ],
    "skipResourceCheck": False
}


trunk = {
    "policy": "int_vpc_trunk_host_11_1",
    "interfaceType": "INTERFACE_VPC",
    "interfaces": [
        {
            "serialNumber": "FDO242109B1~FDO234602KX",
            "interfaceType": "INTERFACE_VPC",
            "ifName": "vPC2",
            "fabricName": "IBM_VxLAN_Fabric",
            "nvPairs": {
                "PEER1_PCID": "2",
                "PEER2_PCID": "2",
                "PEER1_MEMBER_INTERFACES": "e1/9",
                "PEER2_MEMBER_INTERFACES": "e1/9",
                "PC_MODE": "active",
                "BPDUGUARD_ENABLED": True,
                "PORTTYPE_FAST_ENABLED": True,
                "MTU": "jumbo",
                "PEER1_ALLOWED_VLANS": "none",
                "PEER2_ALLOWED_VLANS": "none",
                "PEER1_PO_DESC": "",
                "PEER2_PO_DESC": "",
                "PEER1_PO_CONF": "",
                "PEER2_PO_CONF": "",
                "ADMIN_STATE": True,
                "INTF_NAME": "vPC2"
            }
        }
    ],
    "skipResourceCheck": False
}

dot1qtunnel = {
    "policy": "int_vpc_dot1q_tunnel_11_1",
    "interfaceType": "INTERFACE_VPC",
    "interfaces": [
        {
            "serialNumber": "FDO242109B1~FDO234602KX",
            "interfaceType": "INTERFACE_VPC",
            "ifName": "vPC2",
            "fabricName": "IBM_VxLAN_Fabric",
            "nvPairs": {
                "PEER1_PCID": "2",
                "PEER2_PCID": "2",
                "PEER1_MEMBER_INTERFACES": "e1/9",
                "PEER2_MEMBER_INTERFACES": "e1/9",
                "PC_MODE": "active",
                "BPDUGUARD_ENABLED": "True",
                "PORTTYPE_FAST_ENABLED": True,
                "MTU": "jumbo",
                "PEER1_ACCESS_VLAN": "",
                "PEER2_ACCESS_VLAN": "",
                "PEER1_PO_DESC": "",
                "PEER2_PO_DESC": "",
                "PEER1_PO_CONF": "",
                "PEER2_PO_CONF": "",
                "ADMIN_STATE": True,
                "INTF_NAME": "vPC2"
            }
        }
    ],
    "skipResourceCheck": False
}