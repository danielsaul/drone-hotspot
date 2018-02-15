#!/bin/bash
chmod 755 /etc/init.d/CustomNetworkConfig.sh
chmod a+x /etc/init.d/CustomNetworkConfig.sh
chmod 777 /etc/init.d/CustomNetworkConfig.sh

chmod +x drone-hotspot/rpi/ppp-creator.sh
sudo drone-hotspot/rpi/ppp-creator.sh EVERYWHERE ttyUSB3
sudo pppd call gprs&
sleep 5
sudo route add default dev ppp0

sudo sed -i '/denyinterfaces/s/^/#/' /etc/dhcpcd.conf
sudo service dhcpcd restart
sleep 10
sudo service dnsmasq start
sudo sed -i '/^#.*denyinterfaces /s/^#//' /etc/dhcpcd.conf

sudo killall gpsd
sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock
