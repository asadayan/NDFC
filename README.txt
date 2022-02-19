NDFC rest api based python scripts are created mainly for NDFC based POC setup.
These scripts will be helpful to create bulk set of VRFs, Networks, VPC, Port channels and
attaching the physical interface or port channels to the respective networks.

This help file help you to navigate how to use the script file and how to create basic config per Fabric
such as
- Create multiple set of VRFs
- Create different set of networks per VRF
- Attach those networks to physical interface
- Create VPC and ttach those vpc interface to networks
- Create regular l2 and l3 port-channel and attach those port-channels to networks
- Detach physical interface from networks
- Detach VPC from networks
- Detach Port-channels from networks
- Delete VPCs
- Delete Port-Channels
- List VRFs
- List Networks
- List Fabrics

Step-1: Copy all the provided files to a project directory.
Step-2: Edit ndfc_credentials.py to update the ndfc ip address and it credentials

Given below are some examples.

======
python ndfc_add_bulk_vrf.py
usage python ndfc_add_bulk_vrf.py fabric-name vrf_prefix start_l3vni number_of_vrf [DefaultRouteFlag] [HostRouteFlag] [StaticDefaultRouteFlag]
Example: python ndfc_add_bulk_vrf.py IBM_VxLAN_Fabric ibmvRF 70001 20 0 1 0
This will create 20 vrfs, with each vrf starting prefix being ibmvRF on ndfc fabric IBM_VxLAN_Fabric with host_route being enabled for each vrf.

output:
python ndfc_add_bulk_vrf.py IBM_VxLAN_Fabric ibmvRF 70001 20 0 1 0
Fabric Name: IBM_VxLAN_Fabric VRF Name: ibmvRF-001  L3 VNI: 70001  status: created
                            ---- OUTPUT TRUNCATED-----
Fabric Name: IBM_VxLAN_Fabric VRF Name: ibmvRF-020  L3 VNI: 70020  status: created
Do you want to save and deploy?[Y/N]y
Saved Config
{"status":"Config save is completed"}
Deployed Config
{"status":"Config deployment has been triggered"}

ndfc takes time in saving and deploying, it is better NOT to save and deploy for each configuration run.

======

To delete all undeployed bulk vrf:

python ndfc_delete_vrf.py IBM_VxLAN_Fabric all

Do you really want to delete all the un deployed vrfs in the fabric IBM_VxLAN_Fabric? if yes confirm by typing "yes":yes
Deleting all the un deployed vrfs in the fabric IBM_VxLAN_Fabric
 vrf ibmvRF-001 deleted
 vrf ibmvRF-002 deleted
 vrf ibmvRF-003 deleted

=======================

python ndfc_add_bulk_network.py
Enter the fabric Name: IBM_VxLAN_Fabric
Do you want to create networks on all vrfs or only undeployed or vrf starting with certain prefix(all,undeployed,vrfprefix): all
Enter the starting L2 VNI for the networks: 13001
Enter number of networks per vrf: 2
Enter the starting vlan for the networks: 301
Enter the starting ipv4 address for the networks: 13.29.1.1
Enter the ipv4 address mask: 25
Enter the starting ipv6 address for the networks to skip just press enter: 2019:2020:2021:2022::1
Enter the ipv6 address mask, to skip press enter: 97
Type YES/NO to enable disable arp suppression per network: yes
Please enter the multicast address for BUM traffic to skip press enter: 225.1.1.1
Network VRF_50001_NET_13001 created under vrf VRF_50001
Network VRF_50003_NET_13006 created under vrf VRF_50003
Network ibmvRF-001_NET_13007 created under vrf ibmvRF-001
                           ---- OUTPUT TRUNCATED-----
Network ibmvRF-020_NET_13046 created under vrf ibmvRF-020
Do you want to save and deploy?[Y/N]n
Save separately ..

=====

To delete all undeployed bulk networks:
python ndfc_delete_networks.py IBM_VxLAN_Fabric all
Do you really want to delete all the un deployed Networks in the fabric IBM_VxLAN_Fabric? if yes confirm by typing "yes":yes
Deleting all the un deployed Networks in the fabric IBM_VxLAN_Fabric
Number of Deployed Networks: 30

Network ibmvRF-001_NET_13001 deleted
   ---- OUTPUT TRUNCATED-----
Network ibmvRF-020_NET_13040 deleted
Do you want to save and deploy?[Y/N]n
Save separately ..



=======

Adding VPC and attaching those vpc to undeployed network
 python ndfc_add_vpc.py
Enter the fabric Name: IBM_VxLAN_Fabric
Enter the vpc port_channel type (trunk,access or dot1qtunnel): trunk
Enter the starting vPC port-channel number: 101
Enter the vPC pair if a particular pair need to be configured or just enter to ignore (leaf1~leaf2):
Enter the vpc pair to be excluded or just enter to be ignore leaf3~leaf4:
Type "all" if you want to configure all the vpc pair leafs in the fabric: all
Enter the first 3 characters of the network created to configure only those network: ibm
Enter the physical interface list or range to be configured, symmetry across all leaf is assumed(e1/1-2,e3/8-9): e1/5-9,e1/23-27
e1/5,e1/6,e1/7,e1/8,e1/9,e1/23,e1/24,e1/25,e1/26,e1/27
VPC vPC101 added with e1/5 on Leaf-1--Leaf-2
'OK\n'
VPC vPC102 added with e1/6 on Leaf-1--Leaf-2
'OK\n'
   ---- OUTPUT TRUNCATED-----
VPC vPC120 added with e1/27 on Leaf-3--Leaf-4
'OK\n'
Starting vpc deployment in the fabric IBM_VxLAN_Fabric
Network information fetched
returning all network list
('FDO242109B1', 'FDO234602KX', 'Port-channel101,Port-channel102,Port-channel103,Port-channel104,Port-channel105,Port-channel106,Port-channel107,Port-channel108,Port-channel109,Port-channel110', 'Leaf-1--Leaf-2')
Attaching vpc port-channels to networks..
{'ibmvRF-001_NET_19001-[FDO242109B1/Leaf-1]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS'}
Interface Port-channel101,Port-channel102,Port-channel103,Port-channel104,Port-channel105,Port-channel106,Port-channel107,Port-channel108,Port-channel109,Port-channel110 with VLAN 701 attached to Leaf-1--Leaf-2

         ---- OUTPUT TRUNCATED-----

{'ibmvRF-020_NET_19040-[FDO23480XXX/Leaf-3]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS',
 'ibmvRF-020_NET_19040-[FDO242109B1/Leaf-1]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS'}
Interface Port-channel111,Port-channel112,Port-channel113,Port-channel114,Port-channel115,Port-channel116,Port-channel117,Port-channel118,Port-channel119,Port-channel120 with VLAN 740 attached to Leaf-3--Leaf-4
Do you want to save and deploy?[Y/N]n
Save separately ..

==================================
Creating L3 port-channel on the fabric
python ndfc_add_port_chnl.py
Enter the Fabric Name:IBM_VxLAN_Fabric
Enter the port_channel type, options are trunk, access, dot1qtunnel and routed: routed
Enter the starting port channel number: 601
Enter the leaf name if for specif leaf config, to skip press enter:
Enter the leaf name to exclude certain leaf nodes, to skip press enter:
Enter all if you want to configure on all leaf nodes: all
Enter number of interfaces per port channel: 2
Enter the interfaces used to create the port channel( symmentry of the port assumed across fabric): e1/31-34
Enter the first 3 characters of the networks created(net prefix): ibm
['e1/31,e1/32', 'e1/33,e1/34']
Please enter the vrf name for the routed port channel: default if there is no vrf:ibmvRF-001
Please enter the starting ipv4/ipv6 address for the routed port channel:24.29.42.1
Please enter ipv4/ipv6 address prefix length:24
port_channel port_channel601 added with e1/31,e1/32 on IBM_POAP_SW
'OK\n'
port_channel port_channel602 added with e1/33,e1/34 on IBM_POAP_SW
'OK\n'
  ---- OUTPUT TRUNCATED-----
port_channel port_channel610 added with e1/33,e1/34 on Leaf-4
'OK\n'
No Network attachments for L3 routed port channel..




=============================
Creating L2 trunk port-channels across the fabric
python ndfc_add_port_chnl.py
Enter the Fabric Name:IBM_VxLAN_Fabric
Enter the port_channel type, options are trunk, access, dot1qtunnel and routed: trunk
Enter the starting port channel number: 650
Enter the leaf name if for specif leaf config, to skip press enter:
Enter the leaf name to exclude certain leaf nodes, to skip press enter:
Enter all if you want to configure on all leaf nodes: all
Enter number of interfaces per port channel: 2
Enter the interfaces used to create the port channel( symmentry of the port assumed across fabric): e1/35-40
Enter the first 3 characters of the networks created(net prefix): ibm
['e1/35,e1/36', 'e1/37,e1/38', 'e1/39,e1/40']
port_channel port_channel650 added with e1/35,e1/36 on IBM_POAP_SW
'OK\n'
port_channel port_channel651 added with e1/37,e1/38 on IBM_POAP_SW
'OK\n'
 ---- OUTPUT TRUNCATED-----
port_channel port_channel664 added with e1/39,e1/40 on Leaf-4
'OK\n'
Starting port_channel deployment in the fabric IBM_VxLAN_Fabric
Network information fetched
returning all network list
Attaching port_channel port-channels to networks..
{'ibmvRF-001_NET_19001-[FDO23440CZ6/IBM_POAP_SW]': 'SUCCESS'}
Interface Port-channel650,Port-channel651,Port-channel652 with VLAN 701 attached to IBM_POAP_SW
{'ibmvRF-001_NET_19001-[FDO23440CZ6/IBM_POAP_SW]': 'SUCCESS',
 'ibmvRF-001_NET_19001-[FDO242109B1/Leaf-1]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS'}
Interface Port-channel653,Port-channel654,Port-channel655 with VLAN 701 attached to Leaf-1

 ---- OUTPUT TRUNCATED-----

 {'ibmvRF-020_NET_19040-[FDO23440CZ6/IBM_POAP_SW]': 'SUCCESS',
 'ibmvRF-020_NET_19040-[FDO234602KX/Leaf-2]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS',
 'ibmvRF-020_NET_19040-[FDO23480XXX/Leaf-3]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS',
 'ibmvRF-020_NET_19040-[FDO23480Y42/Leaf-4]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS',
 'ibmvRF-020_NET_19040-[FDO242109B1/Leaf-1]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS'}
Interface Port-channel662,Port-channel663,Port-channel664 with VLAN 740 attached to Leaf-4
Saved Config
{"status":"Config save is completed"}




=====================

Attaching physical interface to networks, in the example below from the deployed and undeployed network the physical interface is attached
only on those network starting with 'ibm'

python ndfc_attach_intf.py IBM_VxLAN_Fabric e1/41-43 ibm all
Ethernet1/41,Ethernet1/42,Ethernet1/43,
Network information fetched
returning all network list
Network name prefix not matching skipping network Network_30031
Network name prefix not matching skipping network Network_30010
---------OUTPUT TRUNCATED------------
attached interfaces to node IBM_POAP_SW,172.28.81.209
{'ibmvRF-001_NET_19001-[FDO23440CZ6/IBM_POAP_SW]': 'SUCCESS',
 'ibmvRF-001_NET_19002-[FDO23440CZ6/IBM_POAP_SW]': 'SUCCESS',
 'ibmvRF-002_NET_19003-[FDO23440CZ6/IBM_POAP_SW]': 'SUCCESS',
 ---------OUTPUT TRUNCATED------------
 'ibmvRF-019_NET_19037-[FDO23480Y42/Leaf-4]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS',
 'ibmvRF-019_NET_19038-[FDO23480Y42/Leaf-4]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS',
 'ibmvRF-020_NET_19039-[FDO23480Y42/Leaf-4]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS',
 'ibmvRF-020_NET_19040-[FDO23480Y42/Leaf-4]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS'}
Do you want to save and deploy?[Y/N]n
Save separately ..


====================


To detach physical interfaces from networks

python ndfc_detach_intf.py IBM_VxLAN_Fabric ibm

Network information fetched
returning all network list
Network name prefix not matching skipping network Network_30031
detached interfaces to node IBM_POAP_SW,172.28.81.209
{}
-------- OUTPUT TRUNCATED ---------
Network name prefix not matching skipping network Network_30019
detached interfaces to node IBM_POAP_SW,172.28.81.209
{}
Network prefix matched, going to detach interface from network ibmvRF-001_NET_19001
detached interfaces to node IBM_POAP_SW,172.28.81.209
{'ibmvRF-001_NET_19001-[FDO23440CZ6/IBM_POAP_SW]': 'SUCCESS'}
Network prefix matched, going to detach interface from network ibmvRF-001_NET_19002
detached interfaces to node IBM_POAP_SW,172.28.81.209
{'ibmvRF-001_NET_19002-[FDO23440CZ6/IBM_POAP_SW]': 'SUCCESS'}
Network prefix matched, going to detach interface from network ibmvRF-002_NET_19003
-------- OUTPUT TRUNCATED ---------

Network prefix matched, going to detach interface from network ibmvRF-019_NET_19038
detached interfaces to node Leaf-4,172.28.81.238
{'ibmvRF-019_NET_19038-[FDO23480Y42/Leaf-4]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS'}
Network prefix matched, going to detach interface from network ibmvRF-020_NET_19039
detached interfaces to node Leaf-4,172.28.81.238
{'ibmvRF-020_NET_19039-[FDO23480Y42/Leaf-4]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS'}
Network prefix matched, going to detach interface from network ibmvRF-020_NET_19040
detached interfaces to node Leaf-4,172.28.81.238
{'ibmvRF-020_NET_19040-[FDO23480Y42/Leaf-4]': 'SUCCESS Peer attach Reponse :  '
                                              'SUCCESS'}
Saved Config
{"status":"Config save is completed"}


===========================


python ndfc_detach_vpc.py IBM_VxLAN_Fabric ibm

and

python ndfc_detach_bulk_po.py
usage python ndfc_detach_bulk_po.py fabric-name [net-prefix]
python ndfc_detach_bulk_po.py IBM_VxLAN_Fabric ibm

Both the above scripts will has the same function of detaching the interfaces but these cmds will remove only the attached Port-channels or VPC
to the network.


==========


To Delete all the detached port channels

python ndfc_delete_po.py IBM_VxLAN_Fabric

Checking all the interface types in the fabric..
('Marked for deletion [{"ifName": "port-channel601", "serialNumber": '
 '"FDO23440CZ6"}]')
------OUTPUT TRUNCATED-----------
('Marked for deletion [{"ifName": "port-channel652", "serialNumber": '
 '"FDO23440CZ6"}]')

=============

To delete all VPC

python ndfc_delete_vpc.py IBM_VxLAN_Fabric

Checking all the interface types in the fabric..
('Marked for deletion [{"ifName": "vPC101", "serialNumber": '
 '"FDO242109B1~FDO234602KX"}]')
('Marked for deletion [{"ifName": "vPC102", "serialNumber": '
 '"FDO242109B1~FDO234602KX"}]')
------OUTPUT TRUNCATED-----------
('Marked for deletion [{"ifName": "vPC106", "serialNumber": '

==============
