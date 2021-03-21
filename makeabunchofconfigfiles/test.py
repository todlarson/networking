from jinja2 import Template
from ipaddress import IPv4Network
from ipaddress import IPv4Address

notvalidatingflag = True

sc_agg_template_data ='''#include <edge.region.dca.prod.h>
#include <az.dca51.prod.h>

#define __HOSTNAME__ {{sc_acc_hostname}}
#define __LO0_CIDR__ {{sc_acc_lo_cidr}}/32
#define __ROUTER_ID__ {{sc_acc_router_id}}
#define __EX4300_24P_BOOL__

#define __UPLINK1_CIDR__ {{sc_acc_uplink1_cidr}}
#define __UPLINK2_CIDR__ {{sc_acc_uplink2_cidr}}

#define __VLAN10_RVI__ {{sc_acc_vlan10_rvi}}/27

#include <prod.sc-acc.root.h>'''


sc_agg_r101_template_data ='''
#define __ACCSW{{sc_agg_downlink_counter}}_CIDR__ {{sc_agg_downlink1_cidr}}
#define __ACCSW{{sc_agg_downlink_counter}}_DESC__ {{access_switch_hostname}}

'''

sc_agg_r102_template_data ='''
#define __ACCSW{{sc_agg_downlink_counter}}_CIDR__ {{sc_agg_downlink2_cidr}}
#define __ACCSW{{sc_agg_downlink_counter}}_DESC__ {{access_switch_hostname}}

'''

sc_agg_template=Template(sc_agg_template_data)
sc_agg_r101_template=Template(sc_agg_r101_template_data)
sc_agg_r102_template=Template(sc_agg_r102_template_data)

az1_aggregate1 = IPv4Network('10.4.20.0/22')
az1_aggregate2 = IPv4Network('10.4.24.0/22')
az1_aggregate3 = IPv4Network('10.4.28.0/22')
az2_aggregate1 = IPv4Network('10.4.36.0/22')
az2_aggregate2 = IPv4Network('10.4.40.0/22')
az2_aggregate3 = IPv4Network('10.4.44.0/22')
az3_aggregate1 = IPv4Network('10.4.52.0/22')
az3_aggregate2 = IPv4Network('10.4.56.0/22')
az3_aggregate3 = IPv4Network('10.4.60.0/22')
az1_acc_loopbacks = IPv4Address('10.4.16.0')
az2_acc_loopbacks = IPv4Address('10.4.32.0')
az3_acc_loopbacks = IPv4Address('10.4.48.0')

az1_acc_uplinks_aggregate = list(IPv4Network('11.4.16.0/22').subnets(new_prefix=31))
az2_acc_uplinks_aggregate = list(IPv4Network('11.4.32.0/22').subnets(new_prefix=31))
az3_acc_uplinks_aggregate = list(IPv4Network('11.4.48.0/22').subnets(new_prefix=31))

camera_subnet_mask = 27
camera_starting_ip = 5
camera_ending_ip = 28 
loopback_subnet_mask = 32
az_list = ['dca50','dca51','dca54','apa60','apa61','apa62','lck50','lck51','lck52']
az_list_of_dicts = [{'az':'dca50','aggregate1':az1_aggregate1,'aggregate2':az1_aggregate2,'scope':'PROD-DCA','loopback':az1_acc_loopbacks,'uplinks':az1_acc_uplinks_aggregate},
                    {'az':'dca51','aggregate1':az2_aggregate1,'aggregate2':az2_aggregate2,'scope':'PROD-DCA','loopback':az2_acc_loopbacks,'uplinks':az2_acc_uplinks_aggregate},
                    {'az':'dca54','aggregate1':az3_aggregate1,'aggregate2':az3_aggregate2,'scope':'PROD-DCA','loopback':az3_acc_loopbacks,'uplinks':az3_acc_uplinks_aggregate},
                    {'az':'apa60','aggregate1':az1_aggregate1,'aggregate2':az1_aggregate2,'scope':'PROD-APA','loopback':az1_acc_loopbacks,'uplinks':az1_acc_uplinks_aggregate},
                    {'az':'apa61','aggregate1':az2_aggregate1,'aggregate2':az2_aggregate2,'scope':'PROD-APA','loopback':az2_acc_loopbacks,'uplinks':az2_acc_uplinks_aggregate},
                    {'az':'apa62','aggregate1':az3_aggregate1,'aggregate2':az3_aggregate2,'scope':'PROD-APA','loopback':az3_acc_loopbacks,'uplinks':az3_acc_uplinks_aggregate},
                    {'az':'lck50','aggregate1':az1_aggregate1,'aggregate2':az1_aggregate2,'scope':'Prod-LCK','loopback':az1_acc_loopbacks,'uplinks':az2_acc_uplinks_aggregate},
                    {'az':'lck51','aggregate1':az2_aggregate1,'aggregate2':az2_aggregate2,'scope':'Prod-LCK','loopback':az2_acc_loopbacks,'uplinks':az1_acc_uplinks_aggregate},
                    {'az':'lck52','aggregate1':az3_aggregate1,'aggregate2':az3_aggregate2,'scope':'Prod-LCK','loopback':az3_acc_loopbacks,'uplinks':az1_acc_uplinks_aggregate}]

counter = 0

for aggregate in ['aggregate1','aggregate2']:
    for i in az_list_of_dicts:
        for camera_subnet in list(i[aggregate].subnets(new_prefix=27)):
            if 'dca' in i['az'] and counter <= 40:
                print(str(i['az']) + "-" + str(i['az'][-2:]) + "-ws-sc-acc-sw" + str(counter+100), i['loopback']+counter, str(i['loopback']+counter) + "/32", camera_subnet, i['uplinks'][counter][0], i['uplinks'][counter][1])
                counter += 1
