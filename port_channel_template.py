#!/usr/bin/python
# Author Ahamed Sadayan
# Template for http post VPC creation
# After import make changes to the releavent field



access = {
    "policy": "int_port_channel_access_host_11_1",
    "interfaceType": "INTERFACE_PORT_CHANNEL",
    "interfaces": [
        {
            "serialNumber": "FDO242109B1",
            "interfaceType": "INTERFACE_PORT_CHANNEL",
            "ifName": "Port-channel3",
            "fabricName": "default_fabric",
            "nvPairs": {
                "MEMBER_INTERFACES": "e1/5",
                "PC_MODE": "active",
                "BPDUGUARD_ENABLED": False,
                "PORTTYPE_FAST_ENABLED": True,
                "MTU": "jumbo",
                "ACCESS_VLAN": "",
                "DESC": "",
                "CONF": "",
                "ADMIN_STATE": True,
                "PO_ID": "Port-channel3"
            }
        }
    ],
    "skipResourceCheck": False
}

trunk = {
    "policy": "int_port_channel_trunk_host_11_1",
    "interfaceType": "INTERFACE_PORT_CHANNEL",
    "interfaces": [
        {
            "serialNumber": "FDO242109B1",
            "interfaceType": "INTERFACE_PORT_CHANNEL",
            "ifName": "Port-channel501",
            "fabricName": "default_fabric",
            "nvPairs": {
                "MEMBER_INTERFACES": "e1/5",
                "PC_MODE": "active",
                "BPDUGUARD_ENABLED": True,
                "PORTTYPE_FAST_ENABLED": True,
                "MTU": "jumbo",
                "ALLOWED_VLANS": "none",
                "DESC": "",
                "CONF": "",
                "ADMIN_STATE": True,
                "PO_ID": "Port-channel501"
            }
        }
    ],
    "skipResourceCheck": False
}

dot1qtunnel = {
    "policy": "int_port_channel_dot1q_tunnel_host_11_1",
    "interfaceType": "INTERFACE_PORT_CHANNEL",
    "interfaces": [
        {
            "serialNumber": "FDO242109B1",
            "interfaceType": "INTERFACE_PORT_CHANNEL",
            "ifName": "Port-channel3",
            "fabricName": "default_fabric",
            "nvPairs": {
                "MEMBER_INTERFACES": "e1/5",
                "PC_MODE": "active",
                "BPDUGUARD_ENABLED": True,
                "PORTTYPE_FAST_ENABLED": True,
                "MTU": "jumbo",
                "ACCESS_VLAN": "",
                "DESC": "",
                "CONF": "",
                "ADMIN_STATE": True,
                "PO_ID": "Port-channel3"
            }
        }
    ],
    "skipResourceCheck": False
}

routed_chnl = {
    "policy": "int_l3_port_channel",
    "interfaceType": "INTERFACE_PORT_CHANNEL",
    "interfaces": [
        {
            "serialNumber": "FDO242109B1",
            "interfaceType": "INTERFACE_PORT_CHANNEL",
            "ifName": "Port-channel3",
            "fabricName": "default_fabric",
            "nvPairs": {
                "MEMBER_INTERFACES": "e1/5",
                "PC_MODE": "active",
                "INTF_VRF": "red",
                "IP": "13.1.1.1",
                "PREFIX": "24",
                "ROUTING_TAG": "",
                "MTU": "9216",
                "DESC": "",
                "CONF": "",
                "ADMIN_STATE": True,
                "PO_ID": "Port-channel3"
            }
        }
    ],
    "skipResourceCheck": False
}
