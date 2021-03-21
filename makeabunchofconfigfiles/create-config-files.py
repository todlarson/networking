from jinja2 import Template
from ipaddress import IPv4Network
import yaml

data ='''
#include <edge.region.dca.prod.h>
#include <az.dca51.prod.h>

#define __HOSTNAME__ {{hostname}}
#define __LO0_CIDR__ {{lo_cidr}}
#define __ROUTER_ID__ {{router_id}}
#define __EX4300_24P_BOOL__

#define __UPLINK1_CIDR__ {{uplink1_cidr}}
#define __UPLINK2_CIDR__ {{uplink2_cidr}}

#define __VLAN10_RVI__ {{vlan10_rvi}}

#include <prod.sc-acc.root.h>
'''
tm=Template(data)

hostname_list = ['host1','host2']
lo_cidr_list = ['1.1.1.1/32','2.2.2.2/32']
router_id_list = ['1.1.1.1','2.2.2.2']
uplink1_cidr_list = ['3.3.3.3/31','4.4.4.4/31']
uplink2_cidr_list = ['5.5.5.5/31','6.6.6.6/31']
vlan10_rvi_list = ['10.0.0.1/27','10.0.0.33/27']

for i in range(0,2):
    msg = tm.render(hostname=hostname_list[i],lo_cidr=lo_cidr_list[i],router_id=router_id_list[i],uplink1_cidr=uplink1_cidr_list[i],uplink2_cidr=uplink2_cidr_list[i],vlan10_rvi=vlan10_rvi_list[i])
    print(msg)

try:
    config = yaml.load(file('access-switch-loopbacks-dca.yaml', 'r'))
except yaml.YAMLError exc:
    print "Error in configuration file:", exc
