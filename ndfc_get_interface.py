#!/usr/bin/python
# Author Ahamed Sadayan

import ndfc_modules
import sys
import pprint


if len(sys.argv) < 2:
    print(f'usage python {sys.argv[0]} fabric-name [network_numers] # 0 means no network attached to interface')
    sys.exit()
fabricName = sys.argv[1]
if len(sys.argv) == 3:
    number_of_networks = int(sys.argv[2])
else:
    number_of_networks = -1

po_list = ndfc_modules.get_port_channels(fabricName, number_of_networks )
pprint.pprint(po_list)