import ipaddress


# wscor=['10.1.1.1/32','10.1.1.0/24','172.16.0.0/12','192.168.1.1/32']
# wssvc=['10.1.1.1/32','10.1.1.0/24','172.16.0.0/12','1.1.1.1/32','192.168.0.0/16']
# ip1=ipaddress.ip_network('10.1.1.1/32')
# ip2=ipaddress.ip_network('10.1.1.0/24')
# ip3=ipaddress.ip_network('10.1.1.0/24')

# read file contents into a list
wscor_routing_table=[]
with open("wscor.txt") as file:
    for line in file:
        line = line.strip() #preprocess line
        wscor_routing_table.append(line)

# read file contents into a list
wssvc_routing_table=[]
with open("wssvc.txt") as file:
    for line in file:
        line = line.strip() #preprocess line
        wssvc_routing_table.append(line)

# some files are large to have a global flag
found_errors = False

# loop through ws-cor routing table
for rt in wscor_routing_table:
    wscor_route=ipaddress.ip_network(rt)
    # initialize to false at the start of each loop
    route_is_covered = False
    # loop through ws-svc routing table
    for rt in wssvc_routing_table:
          wssvc_route=ipaddress.ip_network(rt)
          # check if the ws-cor route is with or identical to any of the ws-svc routes
          if (wscor_route.subnet_of(wssvc_route)):
            route_is_covered = True
    if route_is_covered:
        print(wscor_route," has a covering route in the wssvc")
    else:
        print(wscor_route," ERROR has NO covering route in the wssvc")
        found_errors = True

# Did I find any routes with no coverage?
if found_errors:
    print("There were errors bro")
else:
    print("Congratulations, no errors")

