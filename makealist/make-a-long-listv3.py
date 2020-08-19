from jinja2 import Template
from ipaddress import IPv4Network

notvalidatingflag = True

data = '''- random:
    scope: {{scope}}
    address: {{address}}
    description: {{description}}
    location: {{az|upper}}
    role: vlan
    state: Allocated'''
tm=Template(data)

az1_aggregate1 = IPv4Network('10.4.20.0/22')
az1_aggregate2 = IPv4Network('10.4.24.0/22')
az1_aggregate3 = IPv4Network('10.4.28.0/22')
az2_aggregate1 = IPv4Network('10.4.36.0/22')
az2_aggregate2 = IPv4Network('10.4.40.0/22')
az2_aggregate3 = IPv4Network('10.4.44.0/22')
az3_aggregate1 = IPv4Network('10.4.52.0/22')
az3_aggregate2 = IPv4Network('10.4.56.0/22')
az3_aggregate3 = IPv4Network('10.4.60.0/22')
camera_subnet_mask = 27
camera_starting_ip = 5
camera_ending_ip = 28 
az_list = ['dca50','dca51','dca54','apa60','apa61','apa62','lck50','lck51','lck52']
az_list_of_dicts = [{'az':'dca50','aggregate1':az1_aggregate1,'aggregate2':az1_aggregate2,'scope':'PROD-DCA'},
                    {'az':'dca51','aggregate1':az2_aggregate1,'aggregate2':az2_aggregate2,'scope':'PROD-DCA'},
                    {'az':'dca54','aggregate1':az3_aggregate1,'aggregate2':az3_aggregate2,'scope':'PROD-DCA'},
                    {'az':'apa60','aggregate1':az1_aggregate1,'aggregate2':az1_aggregate2,'scope':'PROD-APA'},
                    {'az':'apa61','aggregate1':az2_aggregate1,'aggregate2':az2_aggregate2,'scope':'PROD-APA'},
                    {'az':'apa62','aggregate1':az3_aggregate1,'aggregate2':az3_aggregate2,'scope':'PROD-APA'},
                    {'az':'lck50','aggregate1':az1_aggregate1,'aggregate2':az1_aggregate2,'scope':'Prod-LCK'},
                    {'az':'lck51','aggregate1':az2_aggregate1,'aggregate2':az2_aggregate2,'scope':'Prod-LCK'},
                    {'az':'lck52','aggregate1':az3_aggregate1,'aggregate2':az3_aggregate2,'scope':'Prod-LCK'}]
for i in az_list_of_dicts:
    switch_number = 201
    for subnet in list(i['aggregate1'].subnets(new_prefix=camera_subnet_mask)):
        the_host = list(subnet)
        az = i['az']
        aznum = az[-2:]
        address = subnet
        gw = the_host[1]
        temp1 = str(the_host[camera_starting_ip])
        temp2 = str(the_host[camera_ending_ip])
        cameraiprange = temp1 + "-" + temp2
        description = 'Access switch {0}-{1}-ws-sc-acc-sw{2} subnet, Camera IPs {3}, Gateway:{4}'.format(az,aznum,switch_number,cameraiprange,gw)
        msg = tm.render(az=az,address=address,description=description,gw=gw,cameraiprange=cameraiprange,scope=i['scope'])
        if switch_number >= 103 and switch_number <= 140:
            print(msg) if notvalidatingflag else print(msgvalidation)
        if switch_number == 201:
            switch_number = 101
        else:
            switch_number += 1
    for subnet in list(i['aggregate2'].subnets(new_prefix=camera_subnet_mask)):
        the_host = list(subnet)
        az = i['az']
        aznum = az[-2:]
        address = subnet
        gw = the_host[1]
        temp1 = str(the_host[camera_starting_ip])
        temp2 = str(the_host[camera_ending_ip])
        cameraiprange = temp1 + "-" + temp2
        description = 'Access switch {0}-{1}-ws-sc-acc-sw{2} subnet, Camera IPs {3}, Gateway:{4}'.format(az,aznum,switch_number,cameraiprange,gw)
        msg = tm.render(az=az,address=address,description=description,gw=gw,cameraiprange=cameraiprange,scope=i['scope'])
        if switch_number >= 103 and switch_number <= 140:
            print(msg) if notvalidatingflag else print(msgvalidation)
        if switch_number == 201:
            switch_number = 101
        else:
            switch_number += 1
