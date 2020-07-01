from jinja2 import Template
from ipaddress import IPv4Network

notvalidatingflag = True

data = '''-
    what: prod
    address: {{address}}
    description: {{description}}
    location: {{az|upper}}
    role: vlan
    camera_default_gateway: {{gw}}
    camera_ip_range: {{cameraiprange}}'''
tm=Template(data)

az1_aggregate = IPv4Network('10.4.16.0/22')
az2_aggregate = IPv4Network('10.4.32.0/22')
az3_aggregate = IPv4Network('10.4.48.0/22')
camera_subnet_mask = 27
camera_starting_ip = 5
camera_ending_ip = 22
az_list = ['dca50','dca51','dca54','apa60','apa61','apa62','lck50','lck51','lck52']
az_list_of_dicts = [{'az':'dca50','aggregate':az1_aggregate},
                    {'az':'dca51','aggregate':az2_aggregate},
                    {'az':'dca54','aggregate':az3_aggregate},
                    {'az':'apa60','aggregate':az1_aggregate},
                    {'az':'apa61','aggregate':az2_aggregate},
                    {'az':'apa62','aggregate':az3_aggregate},
                    {'az':'lck50','aggregate':az1_aggregate},
                    {'az':'lck51','aggregate':az2_aggregate},
                    {'az':'lck52','aggregate':az3_aggregate}]
for i in az_list_of_dicts:
    switch_number = 201
    for subnet in list(i['aggregate'].subnets(new_prefix=camera_subnet_mask)):
        the_host = list(subnet)
        az = i['az']
        aznum = az[-2:]
        address = subnet
        description = 'Access switch {0}-{1}-ws-sc-acc-sw{2} camera subnet'.format(az,aznum,switch_number)
        gw = the_host[1]
        temp1 = str(the_host[camera_starting_ip])
        temp2 = str(the_host[camera_ending_ip])
        cameraiprange = temp1 + "-" + temp2
        msg = tm.render(az=az,address=address,description=description,gw=gw,cameraiprange=cameraiprange)
        print(msg) if notvalidatingflag else print(msgvalidation)
        if switch_number == 201:
            switch_number = 101
        else:
            switch_number += 1