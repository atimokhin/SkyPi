#!/bin/bash

# link managed mode config file to /etc/network/interfaces
ln -sf /etc/network/interfaces.managed /etc/network/interfaces

# flush address for wlan0
ip addr flush dev wlan0

ifdown wlan0
ifup   wlan0

# stop dhcpd server - do not need it, now Pi is a client
/etc/init.d/isc-dhcp-server stop
