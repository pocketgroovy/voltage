#!/usr/bin/env bash

set -o errexit # immediately exit on any error


iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -i bond0 -p tcp -s 10.1.0.0/16 --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -i bond0 -p tcp -s 10.0.0.0/8 --dport 6379 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -N LOGGING
iptables -A INPUT -j LOGGING
iptables -A LOGGING -m limit --limit 2/min -j LOG --log-prefix "IPTables-Dropped: " --log-level 4
iptables -A LOGGING -j DROP
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables-save > /etc/network/iptables.rules