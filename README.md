# STM32-OS
A Linux operative system for the STM32 Computer

* Qt6
* Ethernet
* USB
* HDMI
* Package manager
* etc.

Under construction....

Status: I have made the first version work with the `rootfs` system. Here is an log where I got the `ethernet` working.

```sh
# dmesg | grep end0
[    5.693179] stm32-dwmac 5800a000.ethernet end0: renamed from eth0
# ifconfig end0 up
[ 1894.021178] stm32-dwmac 5800a000.ethernet end0: Register MEM_TYPE_PAGE_POOL RxQ-0
[ 1894.142636] stm32-dwmac 5800a000.ethernet end0: PHY [stmmac-0:00] driver [RTL8211F Gigabit Ethernet] (irq=POLL)
[ 1894.161409] dwmac4: Master AXI performs any burst length
[ 1894.165328] stm32-dwmac 5800a000.ethernet end0: No Safety Features support found
[ 1894.183185] stm32-dwmac 5800a000.ethernet end0: IEEE 1588-2008 Advanced Timestamp supported
[ 1894.190549] stm32-dwmac 5800a000.ethernet end0: registered PTP clock
[ 1894.197412] stm32-dwmac 5800a000.ethernet end0: configuring for phy/rgmii-id link mode
# [ 1897.365490] stm32-dwmac 5800a000.ethernet end0: Link is Up - 100Mbps/Full - flow control rx/tx
ifconfig
end0      Link encap:Ethernet  HWaddr 36:87:20:DC:C5:CD  
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:3 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:180 (180.0 B)  TX bytes:0 (0.0 B)
          Interrupt:33 Base address:0x8000 

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

# udhcpc -i end0
udhcpc: started, v1.36.1
udhcpc: broadcasting discover
udhcpc: broadcasting select for 192.168.1.34, server 192.168.1.1
udhcpc: lease of 192.168.1.34 obtained from 192.168.1.1, lease time 7200
deleting routers
adding dns 192.168.1.1
# ifconfig
end0      Link encap:Ethernet  HWaddr 36:87:20:DC:C5:CD  
          inet addr:192.168.1.34  Bcast:192.168.1.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:10 errors:0 dropped:0 overruns:0 frame:0
          TX packets:2 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:1164 (1.1 KiB)  TX bytes:684 (684.0 B)
          Interrupt:33 Base address:0x8000 

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

# ip addr show end0
2: end0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq qlen 1000
    link/ether 36:87:20:dc:c5:cd brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.34/24 brd 192.168.1.255 scope global end0
       valid_lft forever preferred_lft forever
# free -m
              total        used        free      shared  buff/cache   available
Mem:            488          17         462           0           9         462
Swap:             0           0           0
# arp -a
? (192.168.1.35) at 7c:7a:91:4e:a4:7b [ether]  on end0
? (192.168.1.1) at e8:37:7a:7e:c4:21 [ether]  on end0
# hostname my-stm32
# ping my-stm32
ping: bad address 'my-stm32'
# 
```
