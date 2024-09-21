#!/usr/bin/env python
import scapy.all as scapy
import optparse
import ipaddress
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-r", "--ip", dest="ip", help="enter the ip/ip range")
    (options, arguments) = parser.parse_args()
    if not options:
        parser.error("please enter the ip address or ip range")
    return options
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1)[0]
    for element in answered_list:
        print(element[1])


def main():
     options = get_arguments()
     ip = options.ip
     ipaddress.ip_address(ip)
     scan(ip)

if __name__ == "__main__":
    main()

