#!/usr/bin/env bash
set -o errexit # immediately exit on any error

./CustomServices.sh

systemctl start firewalld
systemctl enable firewalld

firewall-cmd --zone=internal --change-interface=eth0 --permanent
firewall-cmd --zone=internal --add-source=10.1.0.0/16 --permanent
firewall-cmd --zone=internal --add-service=ssh --permanent
firewall-cmd --zone=internal --add-service=redis --permanent
firewall-cmd --zone=internal --add-service=mongo --permanent
firewall-cmd --zone=public --change-interface=eth1 --permanent
firewall-cmd --zone=public --add-icmp-block=echo-reply --permanent
firewall-cmd --zone=public --add-service=http --permanent
firewall-cmd --zone=public --add-service=https --permanent
firewall-cmd --zone=public --remove-service=ssh --permanent
firewall-cmd --reload