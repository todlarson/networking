import yaml
import ipaddress

with open(r'myipam.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    myipam_list = yaml.load(file, Loader=yaml.FullLoader)

# Print all the aggregates
# for key,value in myipam_list.items():
#     if value['type'] == 'aggregate':
#         print(value['desc'])
#         for x in value['address']:
#             print("    ", x)

# List all the host addresses availabe in the loopback aggregate
for x in myipam_list['aggregate_loopbacks']['address']:
    for z in ipaddress.ip_network(x):
        for a in myipam_list['allocated_loopbacks']['address']: 
            if z in ipaddress.ip_network(a):            
                print("NOT", z)
            else:
                print("available", z)
