#!/bin/bash
#Add "sudo sh /etc/init.d/CustomNetworkConfig.sh" to /etc/rc.local
chmod 755 /etc/init.d/CustomNetworkConfig.sh
chmod a+x /etc/init.d/CustomNetworkConfig.sh
chmod 777 /etc/init.d/CustomNetworkConfig.sh

chmod +x ./ppp-creator.sh
sudo ./ppp-creator.sh EVERYWHERE ttyUSB3
sudo pppd call gprs&
sleep 5
sudo route add default dev ppp0

sudo sed -i '/denyinterfaces/s/^/#/' /etc/dhcpcd.conf
sudo service dhcpcd restart
sleep 10
sudo service dnsmasq start
sudo sed -i '/^#.*denyinterfaces /s/^#//' /etc/dhcpcd.conf
