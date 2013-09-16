# Copyright (c) 2013 MetaMetrics, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

'''pyplates: CloudFormation templates, generated with python

See also:

- https://aws.amazon.com/cloudformation/
- https://cfn-pyplates.readthedocs.org/ (you might already be here)
- https://github.com/seandst/cfn-pyplates/
'''

# Friendly PEP-386 version string
__version__ = '0.2.1'

import warnings

try:
    from verlib import NormalizedVersion
    # Validates the version above, exposing the version parts for anyone
    # that might want to make decisions based on a normalized version tuple
    version_parts = NormalizedVersion(__version__).parts
except ImportError:
    verlib_errormsg = '''
    Failed to import verlib, version_parts will not be available

    This should only happen during install, before dependencies are evaluated
    and installed.
    '''
    warnings.warn(verlib_errormsg, ImportWarning)

# Protocol numbers, used in setting up security group rules as documented
# in:
# https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
#
# The CloudFormation template requires the protocol number, but the name
# TCP, UDP etc is easier to remember. This mapping therefore helps.
PROTOCOLS = {
    '3PC': '34',
    'A/N': '107',
    'AH': '51',
    'ARGUS': '13',
    'ARIS': '104',
    'AX.25': '93',
    'BBN-RCC-MON': '10',
    'BNA': '49',
    'BR-SAT-MON': '76',
    'CBT': '7',
    'CFTP': '62',
    'CHAOS': '16',
    'CPHB': '73',
    'CPNX': '72',
    'CRTP': '126',
    'CRUDP': '127',
    'Compaq-Peer': '110',
    'DCCP': '33',
    'DCN-MEAS': '19',
    'DDP': '37',
    'DDX': '116',
    'DGP': '86',
    'DSR': '48',
    'EGP': '8',
    'EIGRP': '88',
    'EMCON': '14',
    'ENCAP': '98',
    'ESP': '50',
    'ETHERIP': '97',
    'FC': '133',
    'FIRE': '125',
    'GGP': '3',
    'GMTP': '100',
    'GRE': '47',
    'HIP': '139',
    'HMP': '20',
    'HOPOPT': '0',
    'I-NLSP': '52',
    'IATP': '117',
    'ICMP': '1',
    'IDPR': '35',
    'IDPR-CMTP': '38',
    'IDRP': '45',
    'IFMP': '101',
    'IGMP': '2',
    'IGP': '9',
    'IL': '40',
    'IPCV': '71',
    'IPComp': '108',
    'IPIP': '94',
    'IPLT': '129',
    'IPPC': '67',
    'IPTM': '84',
    'IPX-in-IP': '111',
    'IPv4': '4',
    'IPv6': '41',
    'IPv6-Frag': '44',
    'IPv6-ICMP': '58',
    'IPv6-NoNxt': '59',
    'IPv6-Opts': '60',
    'IPv6-Route': '43',
    'IRTP': '28',
    'ISIS over IPv4': '124',
    'ISO-IP': '80',
    'ISO-TP4': '29',
    'KRYPTOLAN': '65',
    'L2TP': '115',
    'LARP': '91',
    'LEAF-1': '25',
    'LEAF-2': '26',
    'MERIT-INP': '32',
    'MFE-NSP': '31',
    'MICP': '95',
    'MOBILE': '55',
    'MPLS-in-IP': '137',
    'MTP': '92',
    'MUX': '18',
    'Mobility Header': '135',
    'NARP': '54',
    'NETBLT': '30',
    'NSFNET-IGP': '85',
    'NVP-II': '11',
    'OSPFIGP': '89',
    'PGM': '113',
    'PIM': '103',
    'PIPE': '131',
    'PNNI': '102',
    'PRM': '21',
    'PTP': '123',
    'PUP': '12',
    'PVP': '75',
    'QNX': '106',
    'RDP': '27',
    'ROHC': '142',
    'RSVP': '46',
    'RSVP-E2E-IGNORE': '134',
    'RVD': '66',
    'SAT-EXPAK': '64',
    'SAT-MON': '69',
    'SCC-SP': '96',
    'SCPS': '105',
    'SCTP': '132',
    'SDRP': '42',
    'SECURE-VMTP': '82',
    'SKIP': '57',
    'SM': '122',
    'SMP': '121',
    'SNP': '109',
    'SPS': '130',
    'SRP': '119',
    'SSCOPMCE': '128',
    'ST': '5',
    'STP': '118',
    'SUN-ND': '77',
    'SWIPE': '53',
    'Shim6': '140',
    'Sprite-RPC': '90',
    'TCF': '87',
    'TCP': '6',
    'TLSP': '56',
    'TP++': '39',
    'TRUNK-1': '23',
    'TRUNK-2': '24',
    'TTP': '84',
    'UDP': '17',
    'UDPLite': '136',
    'UTI': '120',
    'VINES': '83',
    'VISA': '70',
    'VMTP': '81',
    'VRRP': '112',
    'WB-EXPAK': '79',
    'WB-MON': '78',
    'WESP': '141',
    'WSN': '74',
    'XNET': '15',
    'XNS-IDP': '22',
    'XTP': '36',
    'manet': '138'
}

