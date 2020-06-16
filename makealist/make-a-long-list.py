from random import randrange
from jinja2 import Template

notvalidatingflag = True

data = '''- random:
    scope: {{scope}}
    address: {{address}}
    description: {{description}}
    location: {{az|upper}}
    role: vlan
    state: Allocated'''
tm=Template(data)

NumberPOEperAZ=24
for az in ['dca50','dca51','dca54','apa60','apa61','apa62','lck50','lck51','lck52']:
    switchnum = 100
    maxswitch = switchnum + NumberPOEperAZ
    aznum=az[-2:]
    octet3=18
    fiberflag=True
    if az in ['dca50','apa60','lck50']: octet3 = octet3
    elif az in ["dca51",'apa61','lck51']: octet3 = octet3 + 16
    elif az in ["dca54",'apa62','lck52']: octet3 = octet3 + 32
    else: octet3 = 99999999999
    if 'dca' in az: scope='PROD-DCA'
    elif 'apa' in az: scope='PROD-APA'
    elif 'lck' in az: scope='Prod-LCK'
    else: scope='ErrorErrorError'
    while switchnum < maxswitch:
        for octet4 in [0,32,64,96,128,160,192,224]:
            if switchnum < maxswitch:
                if switchnum == 100 and fiberflag: switchnum = 201
                else: switchnum = switchnum + 1
                ipstart = octet4 + 5
                ipend = ipstart + 23
                cameraiprange = '10.4.' + str(octet3) + '.' + str(ipstart) + '-' + str(ipend)
                gw = '10.4.' + str(octet3) + '.' + str(octet4 + 1)
                address = '10.4.' + str(octet3) + '.' + str(octet4) + '/27'
                description = 'Access switch {3}-{4}-ws-sc-acc-sw{2} subnet, Camera IPs {7}/27, Gateway:{6}'.format(octet3,octet4,switchnum,az,aznum,address,gw,cameraiprange)
                msg = tm.render(scope=scope,az=az,address=address,description=description)
                msgvalidation = '{3}-{4}-ws-sc-acc-sw{2} subnet:{5:20} gw:{6:17} CameraIPs:{7}'.format(octet3,octet4,switchnum,az,aznum,address,gw,cameraiprange)
                print(msg) if notvalidatingflag else print(msgvalidation)
                if switchnum == 201: switchnum = 100; fiberflag = False
        octet3 = octet3 + 1