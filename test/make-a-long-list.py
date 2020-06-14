from random import randrange
from jinja2 import Template

notvalidatingflag = False

data = '''-
    what: prod
    address: {{address}}
    description: {{description}}
    location: {{az|upper}}
    role: vlan
    camera_default_gateway: {{gw}}
    camera_ip_range: {{ipstart}}-{{ipend}}'''
tm=Template(data)

NumberPOEperAZ=randrange(3,10)
for az in ['dca50','dca51','dca54','apa60','apa61','apa62','lck50','lck51','lck52']:
    switchnum = 100
    maxswitch = switchnum + NumberPOEperAZ
    aznum=az[-2:]
    octet3=0
    fiberflag=True
    if az in ['dca50','apa60','lck50']: octet3 = octet3
    elif az in ["dca51",'apa61','lck51']: octet3 = octet3 + 32
    elif az in ["dca54",'apa62','lck52']: octet3 = octet3 + 64
    while switchnum < maxswitch:
        for octet4 in [0,32,64,96,128,160,192,224]:
            if switchnum < maxswitch:
                if switchnum == 100 and fiberflag: switchnum = 191
                else: switchnum = switchnum + 1
                ipstart = octet4 + 5
                ipend = ipstart + 23
                gw = '192.168.' + str(octet3) + '.' + str(octet4 + 1)
                address = '192.168.' + str(octet3) + '.' + str(octet4) + '/27'
                description = 'Access switch {3}-{4}-ws-sc-acc-sw{2} camera subnet'.format(octet3,octet4,switchnum,az,aznum,address,gw,ipstart,ipend)
                msg = tm.render(az=az,address=address,description=description,gw=gw,ipstart=ipstart,ipend=ipend)
                msgvalidation = '{3}-{4}-ws-sc-acc-sw{2} {5:20} gw:{6:17} {7:3}-{8:3}'.format(octet3,octet4,switchnum,az,aznum,address,gw,ipstart,ipend)
                print(msg) if notvalidatingflag else print(msgvalidation)
                if switchnum == 191: switchnum = 100; fiberflag = False
        octet3 = octet3 + 1