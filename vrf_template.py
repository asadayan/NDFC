#!/usr/bin/python
# Author Ahamed Sadayan
# Template for http post VRF creation
# After import make changes to the releavent field



vrf = {'fabric': 'default',
 'vrfExtensionTemplate': 'Default_VRF_Extension_Universal',
 'vrfId': '16777214',
 'vrfName': 'default-test',
 'vrfTemplate': 'Default_VRF_Universal',
 'vrfTemplateConfig': {'L3VniMcastGroup': '',
                       'advertiseDefaultRouteFlag': 'true',
                       'advertiseHostRouteFlag': 'true',
                       'asn': '65500',
                       'configureStaticDefaultRouteFlag': 'true',
                       'ipv6LinkLocalFlag': 'true',
                       'isRPExternal': 'false',
                       'loopbackNumber': '',
                       'maxBgpPaths': '1',
                       'maxIbgpPaths': '2',
                       'mtu': '9216',
                       'multicastGroup': '',
                       'nveId': '1',
                       'rpAddress': '',
                       'tag': '12345',
                       'trmBGWMSiteEnabled': 'false',
                       'trmEnabled': 'false',
                       'vrfDescription': '',
                       'vrfIntfDescription': '',
                       'vrfName': 'default-test',
                       'vrfRouteMap': 'FABRIC-RMAP-REDIST-SUBNET',
                       'vrfSegmentId': '51111',
                       'vrfVlanId': '',
                       'vrfVlanName': ''}}


