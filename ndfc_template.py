#!/usr/bin/python
# Author Ahamed Sadayan


easy_fabric = {'asn': '65513',
 'deviceType': 'n9k',
 'fabricName': 'default-test',
 'fabricTechnology': 'VXLANFabric',
 'fabricTechnologyFriendly': 'VXLAN Fabric',
 'fabricType': 'Switch_Fabric',
 'fabricTypeFriendly': 'Switch Fabric',
 'networkExtensionTemplate': 'Default_Network_Extension_Universal',
 'networkTemplate': 'Default_Network_Universal',
 'nvPairs': {'AAA_REMOTE_IP_ENABLED': 'false',
             'AAA_SERVER_CONF': '',
             'ACTIVE_MIGRATION': 'false',
             'ADVERTISE_PIP_BGP': 'false',
             'AGENT_INTF': 'eth0',
             'ANYCAST_BGW_ADVERTISE_PIP': 'false',
             'ANYCAST_GW_MAC': '2020.0000.00aa',
             'ANYCAST_LB_ID': '',
             'ANYCAST_RP_IP_RANGE': '',
             'ANYCAST_RP_IP_RANGE_INTERNAL': '',
             'AUTO_SYMMETRIC_VRF_LITE': 'false',
             'BFD_AUTH_ENABLE': 'false',
             'BFD_AUTH_KEY': '',
             'BFD_AUTH_KEY_ID': '',
             'BFD_ENABLE': 'false',
             'BFD_IBGP_ENABLE': 'false',
             'BFD_ISIS_ENABLE': 'false',
             'BFD_OSPF_ENABLE': 'false',
             'BFD_PIM_ENABLE': 'false',
             'BGP_AS': '65001',
             'BGP_AS_PREV': '65001',
             'BGP_AUTH_ENABLE': 'false',
             'BGP_AUTH_KEY': '',
             'BGP_AUTH_KEY_TYPE': '3',
             'BGP_LB_ID': '0',
             'BOOTSTRAP_CONF': '',
             'BOOTSTRAP_ENABLE': 'false',
             'BOOTSTRAP_MULTISUBNET': '',
             'BOOTSTRAP_MULTISUBNET_INTERNAL': '',
             'BRFIELD_DEBUG_FLAG': 'Disable',
             'BROWNFIELD_NETWORK_NAME_FORMAT': 'Auto_Net_VNI$$VNI$$_VLAN$$VLAN_ID$$',
             'CDP_ENABLE': 'false',
             'COPP_POLICY': 'strict',
             'DCI_SUBNET_RANGE': '10.11.3.0/24',
             'DCI_SUBNET_TARGET_MASK': '24',
             'DEAFULT_QUEUING_POLICY_CLOUDSCALE': 'queuing_policy_default_8q_cloudscale',
             'DEAFULT_QUEUING_POLICY_OTHER': 'queuing_policy_default_other',
             'DEAFULT_QUEUING_POLICY_R_SERIES': 'queuing_policy_default_r_series',
             'DEPLOYMENT_FREEZE': 'false',
             'DHCP_ENABLE': 'false',
             'DHCP_END': '',
             'DHCP_END_INTERNAL': '',
             'DHCP_IPV6_ENABLE': 'DHCPv4',
             'DHCP_IPV6_ENABLE_INTERNAL': '',
             'DHCP_START': '',
             'DHCP_START_INTERNAL': '',
             'DNS_SERVER_IP_LIST': '',
             'DNS_SERVER_VRF': '',
             'ENABLE_AAA': 'false',
             'ENABLE_AGENT': 'false',
             'ENABLE_DEFAULT_QUEUING_POLICY': 'false',
             'ENABLE_EVPN': 'true',
             'ENABLE_FABRIC_VPC_DOMAIN_ID': 'false',
             'ENABLE_FABRIC_VPC_DOMAIN_ID_PREV': 'false',
             'ENABLE_MACSEC': 'false',
             'ENABLE_NETFLOW': 'false',
             'ENABLE_NETFLOW_PREV': 'false',
             'ENABLE_NGOAM': 'true',
             'ENABLE_NXAPI': 'true',
             'ENABLE_NXAPI_HTTP': 'true',
             'ENABLE_PBR': 'false',
             'ENABLE_TENANT_DHCP': 'true',
             'ENABLE_TRM': 'false',
             'ENABLE_VPC_PEER_LINK_NATIVE_VLAN': 'false',
             'EXTRA_CONF_INTRA_LINKS': '',
             'EXTRA_CONF_LEAF': '',
             'EXTRA_CONF_SPINE': '',
             'FABRIC_INTERFACE_TYPE': 'unnumbered',
             'FABRIC_MTU': '9216',
             'FABRIC_MTU_PREV': '9216',
             'FABRIC_NAME': 'SDDC-Fabric1',
             'FABRIC_TYPE': 'Switch_Fabric',
             'FABRIC_VPC_DOMAIN_ID': '',
             'FABRIC_VPC_DOMAIN_ID_PREV': '',
             'FABRIC_VPC_QOS': 'false',
             'FABRIC_VPC_QOS_POLICY_NAME': 'spine_qos_for_fabric_vpc_peering',
             'FEATURE_PTP': 'false',
             'FEATURE_PTP_INTERNAL': 'false',
             'FF': 'Easy_Fabric',
             'GRFIELD_DEBUG_FLAG': 'Disable',
             'HD_TIME': '180',
             'IBGP_PEER_TEMPLATE': '',
             'IBGP_PEER_TEMPLATE_LEAF': '',
             'ISIS_AUTH_ENABLE': 'false',
             'ISIS_AUTH_KEY': '',
             'ISIS_AUTH_KEYCHAIN_KEY_ID': '',
             'ISIS_AUTH_KEYCHAIN_NAME': '',
             'ISIS_LEVEL': 'level-2',
             'ISIS_OVERLOAD_ELAPSE_TIME': '',
             'ISIS_OVERLOAD_ENABLE': 'false',
             'ISIS_P2P_ENABLE': 'false',
             'L2_HOST_INTF_MTU': '9216',
             'L2_HOST_INTF_MTU_PREV': '9216',
             'L2_SEGMENT_ID_RANGE': '30000-49000',
             'L3VNI_MCAST_GROUP': '',
             'L3_PARTITION_ID_RANGE': '50000-59000',
             'LINK_STATE_ROUTING': 'ospf',
             'LINK_STATE_ROUTING_TAG': 'UNDERLAY',
             'LINK_STATE_ROUTING_TAG_PREV': 'UNDERLAY',
             'LOOPBACK0_IPV6_RANGE': '',
             'LOOPBACK0_IP_RANGE': '1.1.1.0/24',
             'LOOPBACK1_IPV6_RANGE': '',
             'LOOPBACK1_IP_RANGE': '1.1.2.0/24',
             'MACSEC_ALGORITHM': '',
             'MACSEC_CIPHER_SUITE': '',
             'MACSEC_FALLBACK_ALGORITHM': '',
             'MACSEC_FALLBACK_KEY_STRING': '',
             'MACSEC_KEY_STRING': '',
             'MACSEC_REPORT_TIMER': '',
             'MGMT_GW': '',
             'MGMT_GW_INTERNAL': '',
             'MGMT_PREFIX': '',
             'MGMT_PREFIX_INTERNAL': '',
             'MGMT_V6PREFIX': '64',
             'MGMT_V6PREFIX_INTERNAL': '64',
             'MPLS_HANDOFF': 'false',
             'MPLS_LB_ID': '',
             'MPLS_LOOPBACK_IP_RANGE': '',
             'MSO_CONNECTIVITY_DEPLOYED': 'true',
             'MSO_CONTROLER_ID': 'NDO-Cluster',
             'MSO_SITE_GROUP_NAME': 'default',
             'MSO_SITE_ID': '1',
             'MULTICAST_GROUP_SUBNET': '',
             'NETFLOW_EXPORTER_LIST': '',
             'NETFLOW_MONITOR_LIST': '',
             'NETFLOW_RECORD_LIST': '',
             'NETWORK_VLAN_RANGE': '2300-2999',
             'NTP_SERVER_IP_LIST': '',
             'NTP_SERVER_VRF': '',
             'NVE_LB_ID': '1',
             'OSPF_AREA_ID': '0.0.0.0',
             'OSPF_AUTH_ENABLE': 'false',
             'OSPF_AUTH_KEY': '',
             'OSPF_AUTH_KEY_ID': '',
             'OVERLAY_MODE': 'config-profile',
             'OVERLAY_MODE_PREV': 'config-profile',
             'PHANTOM_RP_LB_ID1': '',
             'PHANTOM_RP_LB_ID2': '',
             'PHANTOM_RP_LB_ID3': '',
             'PHANTOM_RP_LB_ID4': '',
             'PIM_HELLO_AUTH_ENABLE': 'false',
             'PIM_HELLO_AUTH_KEY': '',
             'PM_ENABLE': 'false',
             'PM_ENABLE_PREV': 'false',
             'POWER_REDUNDANCY_MODE': 'ps-redundant',
             'PREMSO_PARENT_FABRIC': 'None',
             'PTP_DOMAIN_ID': '',
             'PTP_LB_ID': '',
             'REPLICATION_MODE': 'Ingress',
             'ROUTER_ID_RANGE': '',
             'ROUTE_MAP_SEQUENCE_NUMBER_RANGE': '1-65534',
             'RP_COUNT': '2',
             'RP_LB_ID': '',
             'RP_MODE': 'asm',
             'RR_COUNT': '2',
             'SERVICE_NETWORK_VLAN_RANGE': '3000-3199',
             'SITE_ID': '1',
             'SNMP_SERVER_HOST_TRAP': 'true',
             'SPINE_COUNT': '0',
             'SSPINE_ADD_DEL_DEBUG_FLAG': 'Disable',
             'SSPINE_COUNT': '0',
             'STATIC_UNDERLAY_IP_ALLOC': 'false',
             'STRICT_CC_MODE': 'false',
             'SUBINTERFACE_RANGE': '2-511',
             'SUBNET_RANGE': '10.1.0.0/16',
             'SUBNET_TARGET_MASK': '30',
             'SYSLOG_SERVER_IP_LIST': '',
             'SYSLOG_SERVER_VRF': '',
             'SYSLOG_SEV': '',
             'TCAM_ALLOCATION': 'true',
             'UNDERLAY_IS_V6': 'false',
             'USE_LINK_LOCAL': 'false',
             'V6_SUBNET_RANGE': '',
             'V6_SUBNET_TARGET_MASK': '126',
             'VPC_AUTO_RECOVERY_TIME': '360',
             'VPC_DELAY_RESTORE': '150',
             'VPC_DELAY_RESTORE_TIME': '60',
             'VPC_DOMAIN_ID_RANGE': '1-1000',
             'VPC_ENABLE_IPv6_ND_SYNC': 'false',
             'VPC_PEER_KEEP_ALIVE_OPTION': 'management',
             'VPC_PEER_LINK_PO': '500',
             'VPC_PEER_LINK_VLAN': '3600',
             'VRF_LITE_AUTOCONFIG': 'Manual',
             'VRF_VLAN_RANGE': '2000-2299',
             'abstract_anycast_rp': 'anycast_rp',
             'abstract_bgp': 'base_bgp',
             'abstract_bgp_neighbor': 'evpn_bgp_rr_neighbor',
             'abstract_bgp_rr': 'evpn_bgp_rr',
             'abstract_dhcp': 'base_dhcp',
             'abstract_extra_config_bootstrap': 'extra_config_bootstrap_11_1',
             'abstract_extra_config_leaf': 'extra_config_leaf',
             'abstract_extra_config_spine': 'extra_config_spine',
             'abstract_feature_leaf': 'base_feature_leaf_upg',
             'abstract_feature_spine': 'base_feature_spine_upg',
             'abstract_isis': 'base_isis_level2',
             'abstract_isis_interface': 'isis_interface',
             'abstract_loopback_interface': 'int_fabric_loopback_11_1',
             'abstract_multicast': 'base_multicast_11_1',
             'abstract_ospf': 'base_ospf',
             'abstract_ospf_interface': 'ospf_interface_11_1',
             'abstract_pim_interface': 'pim_interface',
             'abstract_route_map': 'route_map',
             'abstract_routed_host': 'int_routed_host',
             'abstract_trunk_host': 'int_trunk_host',
             'abstract_vlan_interface': 'int_fabric_vlan_11_1',
             'abstract_vpc_domain': 'base_vpc_domain_11_1',
             'dcnmUser': 'admin',
             'default_network': 'Default_Network_Universal',
             'default_vrf': 'Default_VRF_Universal',
             'enableRealTimeBackup': '',
             'enableScheduledBackup': '',
             'network_extension_template': 'Default_Network_Extension_Universal',
             'scheduledTime': '',
             'temp_anycast_gateway': 'anycast_gateway',
             'temp_vpc_domain_mgmt': 'vpc_domain_mgmt',
             'temp_vpc_peer_link': 'int_vpc_peer_link_po',
             'vrf_extension_template': 'Default_VRF_Extension_Universal'},
 'provisionMode': 'DCNMTopDown',
 'replicationMode': 'Ingress',
 'siteId': '65513',
 'templateName': 'Easy_Fabric_11_1',
 'vrfExtensionTemplate': 'Default_VRF_Extension_Universal',
 'vrfTemplate': 'Default_VRF_Universal'}