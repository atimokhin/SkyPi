#!/bin/bash

#  link Ad-Hoc mode config file to /etc/network/interface
ln -sf /etc/network/interfaces.ad-hoc /etc/network/interfaces

ifdown wlan0
ifup   wlan0

# start dhcpd fro interface wlan0
/etc/init.d/isc-dhcp-server start
