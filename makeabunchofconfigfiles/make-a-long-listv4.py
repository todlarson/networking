from jinja2 import Template
from ipaddress import IPv4Network
from ipaddress import IPv4Address

notvalidatingflag = True

ipam_data = '''
- random:
    scope: {{scope}}
    address: {{address}}
    description: {{description}}
    location: {{location|upper}}
    role: vlan
    state: Allocated'''

config_data ='''#include <edge.region.dca.prod.h>
#include <az.dca51.prod.h>

#define __HOSTNAME__ {{hostname}}
#define __LO0_CIDR__ {{lo_cidr}}/32
#define __ROUTER_ID__ {{lo_cidr}}
#define __EX4300_24P_BOOL__

#define __UPLINK1_CIDR__ {{uplink1_cidr}}/31
#define __UPLINK2_CIDR__ {{uplink2_cidr}}/31

#define __VLAN10_RVI__ {{vlan10_rvi}}/27

#include <prod.sc-acc.root.h>'''

agg_101_config_data ='''
#define __ACCSW{{agg_downlink_counter}}_CIDR__ {{downlink1_cidr}}/31
#define __ACCSW{{agg_downlink_counter}}_DESC__ {{access_switch_hostname}}

'''

agg_102_config_data ='''
#define __ACCSW{{agg_downlink_counter}}_CIDR__ {{downlink2_cidr}}/31
#define __ACCSW{{agg_downlink_counter}}_DESC__ {{access_switch_hostname}}

'''

ipam_template=Template(ipam_data)
device_file_template=Template(config_data)
agg_101_config_data_template=Template(agg_101_config_data)
agg_102_config_data_template=Template(agg_102_config_data)

az1_camera_aggregate = list(IPv4Network('10.4.20.0/22').subnets(new_prefix=27)) + list(IPv4Network('10.4.24.0/22').subnets(new_prefix=27)) + list(IPv4Network('10.4.28.0/22').subnets(new_prefix=27))
az2_camera_aggregate = list(IPv4Network('10.4.36.0/22').subnets(new_prefix=27)) + list(IPv4Network('10.4.40.0/22').subnets(new_prefix=27)) + list(IPv4Network('10.4.44.0/22').subnets(new_prefix=27))
az3_camera_aggregate = list(IPv4Network('10.4.52.0/22').subnets(new_prefix=27)) + list(IPv4Network('10.4.56.0/22').subnets(new_prefix=27)) + list(IPv4Network('10.4.60.0/22').subnets(new_prefix=27))

az1_acc_loopbacks = IPv4Address('10.4.16.0')
az2_acc_loopbacks = IPv4Address('10.4.32.0')
az3_acc_loopbacks = IPv4Address('10.4.48.0')

az1_acc_uplink_subnet = list(IPv4Network('10.4.16.128/25').subnets(new_prefix=31)) + list(IPv4Network('10.4.17.0/24').subnets(new_prefix=31))
az2_acc_uplink_subnet = list(IPv4Network('10.4.32.128/25').subnets(new_prefix=31)) + list(IPv4Network('10.4.33.0/24').subnets(new_prefix=31))
az3_acc_uplink_subnet = list(IPv4Network('10.4.48.128/25').subnets(new_prefix=31)) + list(IPv4Network('10.4.49.0/24').subnets(new_prefix=31))

camera_subnet_mask = 27
camera_starting_ip = 5
camera_ending_ip = 28 
loopback_subnet_mask = 32
az_list = ['dca50','dca51','dca54','apa60','apa61','apa62','lck50','lck51','lck52']
az_list_of_dicts = [{'az':'dca50','camera_aggregate':az1_camera_aggregate,'scope':'PROD-DCA','loopback':az1_acc_loopbacks,'uplink_subnet':az1_acc_uplink_subnet},
                    {'az':'dca51','camera_aggregate':az2_camera_aggregate,'scope':'PROD-DCA','loopback':az2_acc_loopbacks,'uplink_subnet':az2_acc_uplink_subnet},
                    {'az':'dca54','camera_aggregate':az3_camera_aggregate,'scope':'PROD-DCA','loopback':az3_acc_loopbacks,'uplink_subnet':az3_acc_uplink_subnet},
                    {'az':'apa60','camera_aggregate':az1_camera_aggregate,'scope':'PROD-APA','loopback':az1_acc_loopbacks,'uplink_subnet':az1_acc_uplink_subnet},
                    {'az':'apa61','camera_aggregate':az2_camera_aggregate,'scope':'PROD-APA','loopback':az2_acc_loopbacks,'uplink_subnet':az2_acc_uplink_subnet},
                    {'az':'apa62','camera_aggregate':az3_camera_aggregate,'scope':'PROD-APA','loopback':az3_acc_loopbacks,'uplink_subnet':az3_acc_uplink_subnet},
                    {'az':'lck50','camera_aggregate':az1_camera_aggregate,'scope':'Prod-LCK','loopback':az1_acc_loopbacks,'uplink_subnet':az1_acc_uplink_subnet},
                    {'az':'lck51','camera_aggregate':az2_camera_aggregate,'scope':'Prod-LCK','loopback':az2_acc_loopbacks,'uplink_subnet':az2_acc_uplink_subnet},
                    {'az':'lck52','camera_aggregate':az3_camera_aggregate,'scope':'Prod-LCK','loopback':az3_acc_loopbacks,'uplink_subnet':az3_acc_uplink_subnet}]


for i in az_list_of_dicts:
    counter = 0
    acc_num = 103
    acc_ae = 1
    for camera_subnet in i['camera_aggregate']:
        if 'dca' in i['az'] and counter <= 75:
            hostname = str(i['az']) + "-" + str(i['az'][-2:]) + "-ws-sc-acc-sw" + str(acc_num)
            lo_cidr = str(i['loopback']+counter)
            uplink1_cidr_lower = i['uplink_subnet'][counter][0]
            uplink1_cidr_upper = i['uplink_subnet'][counter][1]
            uplink2_cidr_lower = i['uplink_subnet'][counter+1][0]
            uplink2_cidr_upper = i['uplink_subnet'][counter+1][1]
            vlan10_rvi = list(camera_subnet)[1]
            # print(hostname, lo_cidr, lo_cidr + "/32", vlan10_rvi, uplink1_cidr_lower, uplink1_cidr_upper, uplink2_cidr_lower, uplink2_cidr_upper)
            device_files = device_file_template.render(hostname=hostname,lo_cidr=lo_cidr,uplink1_cidr=uplink1_cidr_upper,uplink2_cidr=uplink2_cidr_upper,vlan10_rvi=vlan10_rvi)
            outputfilename = "./outputfiles/" + hostname + ".txt"
            f = open(outputfilename, "w")
            f.write(device_files)
            f.close()
            counter += 2
            acc_num += 1
    

""" for i in az_list_of_dicts:
    switch_number = 201
    loopback = i['loopbacks']
    agg_101 = "./outputfiles/" + i['az'] + "-agg-r101-config.txt"
    agg_102 = "./outputfiles/" + i['az'] + "-agg-r102-config.txt"
    agg_101_file = open(agg_101, "w")
    agg_102_file = open(agg_102, "w")
    agg_downlink_counter_tally = 0
    uplink_counter = 3
    for subnet in i['camera_aggregate']:
        the_host = list(subnet)
        az = i['az']
        aznum = az[-2:]
        address = subnet
        gw = the_host[1]
        temp1 = str(the_host[camera_starting_ip])
        temp2 = str(the_host[camera_ending_ip])
        cameraiprange = temp1 + "-" + temp2
        hostname = str(az) + "-" + str(aznum) + "-ws-sc-acc-sw" + str(switch_number)
        description = 'Access switch {0}-{1}-ws-sc-acc-sw{2} subnet, Camera IPs {3}, Gateway:{4}'.format(az,aznum,switch_number,cameraiprange,gw)
        templist1 = i['uplink_subnet']
        uplink1_cidr = templist1[uplink_counter]
        uplink2_cidr = templist1[uplink_counter+1]
        uplink1_cidr_upper = uplink1_cidr
        uplink1_cidr_lower = uplink1_cidr
        uplink2_cidr_upper = uplink2_cidr
        uplink2_cidr_lower = uplink2_cidr
        device_files = device_file_template.render(hostname=hostname,lo_cidr=loopback,router_id=loopback,uplink1_cidr=uplink1_cidr_upper,uplink2_cidr=uplink2_cidr_upper,vlan10_rvi=gw)
        device_files_agg_101 = agg_101_config_data_template.render(agg_downlink_counter=agg_downlink_counter_tally, downlink1_cidr=uplink1_cidr_lower,access_switch_hostname=hostname)
        device_files_agg_102 = agg_102_config_data_template.render(agg_downlink_counter=agg_downlink_counter_tally, downlink2_cidr=uplink2_cidr_lower,access_switch_hostname=hostname)
        loopback += 1
        uplink_counter += 2
        agg_downlink_counter_tally += 1
        outputfilename = "./outputfiles/" + hostname + ".txt"
        if switch_number >= 103 and switch_number <= 140:
            f = open(outputfilename, "w")
            f.write(device_files)
            f.close()
            agg_101_file.write(device_files_agg_101)
            agg_102_file.write(device_files_agg_102)
        if switch_number == 201:
            switch_number = 101
        else:
            switch_number += 1

agg_101_file.close()
agg_102_file.close()

 """

############################################Section below does the agg <> acc p2p links
""" dca_file = open("sc_agg_downlink_subnets_dca.yaml", "w")
apa_file = open("sc_agg_downlink_subnets_apa.yaml", "w")
lck_file = open("sc_agg_downlink_subnets_lck.yaml", "w")

for i in az_list_of_dicts:
    agg_num = 101
    acc_num = 103
    acc_ae = 1
    s = 7
    while acc_num <= 140:
        description = str(i['az']) + "-" + str(i['az'][-2:]) + "-ws-sc-agg-r" + str(agg_num) + " ae" + str(acc_num) + " <> " + str(i['az']) + "-" + str(i['az'][-2:]) + "-ws-sc-acc-r" + str(acc_num) + " ae" + str(acc_ae)
        ipam_file = ipam_template.render(scope=i['scope'],address=i['uplink_subnet'][s], description=description, location=i['az'])
        if 'dca' in str(i['az']):
            dca_file.write(ipam_file)
        elif 'apa' in str(i['az']):
            apa_file.write(ipam_file)
        else:
            lck_file.write(ipam_file)
        if acc_ae == 2: 
            acc_num += 1
        acc_ae = 2 if acc_ae == 1 else 1
        agg_num = 102 if agg_num == 101 else 101
        s += 1

dca_file.close()
apa_file.close()
lck_file.close()
 """
 ############################################