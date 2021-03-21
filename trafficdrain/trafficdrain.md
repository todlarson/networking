# Goal

Create a one line configuration command that drains traffic from a juniper device. 
Then, use the "delete" form of that same command to put traffic back onto the device.

## Conditions
A lab with 2 directly connected routers, R1 and R2.
The routers are ospf and bgp adjacent.

We are tasked to drain traffic from R1 so we can perform a Junos update and reboot without impacting the users.
This lab does not have data plane traffic flowing through it so we use control plane details to verify the configuration.

### Versions
Both routers are Juniper vmx devices run in Juniper vLabs https://cloudlabs.juniper.net.
```
jcluser@R1> show version 
Hostname: R1
Model: vmx
Junos: 18.3R1.9
```
### Topology
```
Router-id                            ospf                        Router-id
10.1.1.1           R1 ge-0/0/0 <-----------------> ge-0/0/0 R2   10.1.2.1
Advertised Subnets                   bgp
10.1.1.0/24
10.1.99.0/24
```
## Expectations
In the NORMAL or non-DRAINED state, we expect the following:
- R2 will see 10.1.1.1/24 and 10.1.99.1/24 in the ospf database with a metric of 1.
- R2 will see 10.1.1.1/24 and 10.1.99.1/24 in the bgp table with an AS path of 11.

In the DRAINED state, we expect the following:
- R2 will see 10.1.1.1/24 and 10.1.99.1/24 in the ospf database with a metric of 65535.
- R2 will see 10.1.1.1/24 and 10.1.99.1/24 in the bgp table with an AS path of "11 11 11 11 11".

Finally, back in the NORMAL or non-DRAINED state, we expect the following:
- R2 will see 10.1.1.1/24 and 10.1.99.1/24 in the ospf database with a metric of 1.
- R2 will see 10.1.1.1/24 and 10.1.99.1/24 in the bgp table with an AS path of 11.
## Design
This design address ospf and bgp in different ways.
First, the design uses apply-groups to insert `overload` into the ospf configuration.
Next, the design uses the apply-groups wildcard feature to insert an as-path-prepend configration into all terms of the bgp export policy. In this example we add four occurances of R1's AS 11.

### Group configuration
```
jcluser@R1> show configuration groups 
maint {
    protocols {
        ospf {
            overload;
        }
    }
    policy-options {
        policy-statement send-loopbacks {
            term <*> {
                then as-path-prepend "11 11 11 11";
            }
        }
    }
}
```

A downside of this design is it depends on the export policy to be configured with terms. Term in the policy are a good practice to help with readability and maintainablity so this seems like and acceptable limitation.
## Demo
### Normal conditions on R2
```
jcluser@R2> show ospf database router detail advertising-router 10.1.1.1    

    OSPF database, Area 0.0.0.0
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len 
Router   10.1.1.1         10.1.1.1         0x80000005   325  0x22 0x7fdf  84
  bits 0x0, link count 5
  id 172.16.1.2, data 172.16.1.1, Type Transit (2)
    Topology count: 0, Default metric: 1           <--- Metric is 1
  id 10.1.1.1, data 255.255.255.255, Type Stub (3)
    Topology count: 0, Default metric: 0
  id 10.1.1.0, data 255.255.255.0, Type Stub (3)
    Topology count: 0, Default metric: 0
  id 10.1.99.1, data 255.255.255.255, Type Stub (3)
    Topology count: 0, Default metric: 0
  id 10.1.99.0, data 255.255.255.0, Type Stub (3)
    Topology count: 0, Default metric: 0
  Topology default (ID 0)
    Type: Transit, Node ID: 172.16.1.2
      Metric: 1, Bidirectional

jcluser@R2> show route receive-protocol bgp 172.16.1.1                      

inet.0: 17 destinations, 21 routes (16 active, 0 holddown, 1 hidden)
  Prefix  Nexthop       MED     Lclpref    AS path
  10.1.1.0/24             172.16.1.1       11 I   <--- One entry in AS Path 
  10.1.99.0/24            172.16.1.1       11 I

inet6.0: 1 destinations, 1 routes (1 active, 0 holddown, 0 hidden)

jcluser@R2> 
```

### Drain draffic from R1
```
configure exclusive
set apply-group maint
commit and-quit
```

### Updated conditions on R2
```
jcluser@R2> show ospf database router detail advertising-router 10.1.1.1    

    OSPF database, Area 0.0.0.0
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len 
Router   10.1.1.1         10.1.1.1         0x80000006     5  0x22 0x6bf3  84
  bits 0x0, link count 5
  id 172.16.1.2, data 172.16.1.1, Type Transit (2)
    Topology count: 0, Default metric: 65535       <--- Max Metric 
  id 10.1.1.1, data 255.255.255.255, Type Stub (3)
    Topology count: 0, Default metric: 0
  id 10.1.1.0, data 255.255.255.0, Type Stub (3)
    Topology count: 0, Default metric: 0
  id 10.1.99.1, data 255.255.255.255, Type Stub (3)
    Topology count: 0, Default metric: 0
  id 10.1.99.0, data 255.255.255.0, Type Stub (3)
    Topology count: 0, Default metric: 0
  Topology default (ID 0)
    Type: Transit, Node ID: 172.16.1.2
      Metric: 65535, Bidirectional

jcluser@R2> show route receive-protocol bgp 172.16.1.1                      

inet.0: 17 destinations, 21 routes (16 active, 0 holddown, 1 hidden)
  Prefix  Nexthop       MED     Lclpref    AS path
  10.1.1.0/24             172.16.1.1       11 11 11 11 11 I  <--- Five Entries
  10.1.99.0/24            172.16.1.1       11 11 11 11 11 I
```

### Put draffic back onto R1

```
configure exclusive
del apply-group maint
commit and-quit
```

### Normalized conditions on R2
```
jcluser@R2> show ospf database router detail advertising-router 10.1.1.1    

    OSPF database, Area 0.0.0.0
 Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len 
Router   10.1.1.1         10.1.1.1         0x80000007    12  0x22 0x7be1  84
  bits 0x0, link count 5
  id 172.16.1.2, data 172.16.1.1, Type Transit (2)
    Topology count: 0, Default metric: 1           <--- Metric is back to 1
  id 10.1.1.1, data 255.255.255.255, Type Stub (3)
    Topology count: 0, Default metric: 0
  id 10.1.1.0, data 255.255.255.0, Type Stub (3)
    Topology count: 0, Default metric: 0
  id 10.1.99.1, data 255.255.255.255, Type Stub (3)
    Topology count: 0, Default metric: 0
  id 10.1.99.0, data 255.255.255.0, Type Stub (3)
    Topology count: 0, Default metric: 0
  Topology default (ID 0)
    Type: Transit, Node ID: 172.16.1.2
      Metric: 1, Bidirectional

jcluser@R2> show route receive-protocol bgp 172.16.1.1                      

inet.0: 17 destinations, 21 routes (16 active, 0 holddown, 1 hidden)
  Prefix  Nexthop       MED     Lclpref    AS path
  10.1.1.0/24             172.16.1.1       11 I     <--- One entry in AS Path
  10.1.99.0/24            172.16.1.1       11 I
```

## Relevent Device configurations
### R1
```
configure exclusive
set groups maint protocols ospf overload
set groups maint policy-options policy-statement send-loopbacks term <*> then as-path-prepend "11 11 11 11"
set interfaces lo0 unit 0 family inet address 10.1.1.1/24
set interfaces lo0 unit 0 family inet address 10.1.99.1/24
set policy-options policy-statement send-loopbacks term 1 from route-filter 10.1.1.0/24 exact
set policy-options policy-statement send-loopbacks term 1 then accept
set policy-options policy-statement send-loopbacks term 2 from route-filter 10.1.99.0/24 exact
set policy-options policy-statement send-loopbacks term 2 then accept
set policy-options policy-statement send-loopbacks term 1000 then reject
set policy-options policy-statement myprepend then as-path-prepend "11 11 11 11" 
set policy-options policy-statement myprepend then accept
set protocols bgp export send-loopbacks
set protocols bgp group external-peers type external
set protocols bgp group external-peers peer-as 22
set protocols bgp group external-peers neighbor 172.16.1.2
set routing-options autonomous-system 11
set protocols ospf overload timeout 300
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0
set protocols ospf area 0.0.0.0 interface lo0.0
commit and-quit
```

### R2
```
configure exclusive
set interface lo0 unit 0 family inet address 10.2.1.1/24
set interface lo0 unit 0 family inet address 10.2.99.1/24
set protocols bgp group external-peers type external
set protocols bgp group external-peers peer-as 11
set protocols bgp group external-peers neighbor 172.16.1.1
set routing-options autonomous-system 22
set protocols ospf area 0.0.0.0 interface ge-0/0/0
commit and-quit
```

### Verificaiton show comands
#### R1
```
show configuration policy-options policy-statement send-loopbacks | display inheritance 
show configuration protocols ospf | display inheritance 
show ospf database router detail advertising-router self
```
#### R2
```
show route receive-protocol bgp 172.16.1.1
show ospf database router detail advertising-router 10.1.1.1
```