#!/usr/local/bin/python3
import yaml
import sys
import ipaddress

def add_host(myipam, newhost):
    if newhost not in myipam['console']['hosts']:
        myipam['console']['hosts'][newhost] = {}
        return myipam
    else:
        print("Error:", newhost,"already exists")
        exit()

def delete_host(myipam, newhost):
    if newhost in myipam['console']['hosts']:
        del myipam['console']['hosts'][newhost]
        return myipam
    else:
        print("Error:", newhost," does not exist")
        exit()

def add_address_to_host(myipam, host, lo0):
    if lo0 not in myipam['console']['hosts'][host]:
        myipam['console']['hosts'][host]['loopback0'] = []
        myipam['console']['hosts'][host]['loopback0'] = lo0
    else:
        print("Error:", lo0,"already exists for ", host)

def find_new_loopback(myipam, new_address):
    tracking_list = []
    new_address = ''
    for x in myipam['console']['hosts']:
        tracking_list.append(ipaddress.ip_address(myipam['console']['hosts'][x]['loopback0']))
    for candidate in list(ipaddress.ip_network(str(myipam['console']['aggregate']['dc']['network']))):
        if candidate not in tracking_list:
            new_address = candidate
            return new_address

def get_host_address(myipam, newhost):
    if newhost in myipam['console']['hosts']:
        print(newhost, myipam['console']['hosts'][newhost]['loopback0'])
    else:
        print(newhost, "not found.")
        exit()

def get_host_address_all(myipam):
    for host in myipam['console']['hosts']:
        print(host, myipam['console']['hosts'][host]['loopback0'])

def write_to_file(myipam, filename):
    with open(filename, 'w') as file:
        yaml.dump(myipam, file)   

def print_netmask_gw(myipam):
    agg = ipaddress.ip_network(myipam['console']['aggregate']['dc']['network'])
    print("mask: ", agg.netmask)
    print("gateway: ", list(agg)[1])

#Process args
input_error_msg = "Error -  usage: manageips.py --[add|delete|get|list] [--hostname <hostname>]"
if len(sys.argv) == 2 and sys.argv[1] == "--list":
    action = str(sys.argv[1])
elif len(sys.argv) == 2 and sys.argv[1] != "--list":
    print(input_error_msg)
    exit()
elif len(sys.argv) != 4 or sys.argv[2] != "--hostname":
    print(input_error_msg)
    exit()
else:
    action = str(sys.argv[1])
    newhost = str(sys.argv[3])

# Save the entire file into a dictionary
myipam = []
filename = "/Users/larson/code/networking/manageips/myipam.yaml"
with open(filename, "r") as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    myipam = yaml.load(file, Loader=yaml.FullLoader)

if action == '--add':
   new_address = ''
   new_address = find_new_loopback(myipam, new_address)
   add_host(myipam, newhost)
   add_address_to_host(myipam, newhost, str(new_address))
   write_to_file(myipam, filename)
   get_host_address(myipam, newhost)
   print_netmask_gw(myipam)
elif action == '--delete':
   delete_host(myipam, newhost)
   write_to_file(myipam, filename)
   print(newhost, "deleted.")
   print_netmask_gw(myipam)
elif action == '--get':
   get_host_address(myipam, newhost)
   print_netmask_gw(myipam)
elif action == '--list':
   get_host_address_all(myipam)
   print_netmask_gw(myipam)
else:
    print(input_error_msg)
    exit()
