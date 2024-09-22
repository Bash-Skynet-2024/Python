#!/usr/bin/env python
import re
import subprocess
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("--ip", dest="target_ip", help="enter ip address of device")
    (options, arguments) = parser.parse_args()
    return options.target_ip

def get_mac_addresses(target_ip):
    output = subprocess.check_output(["arp", "-n"]).decode()
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
    print(devices[target_ip])

def main():
    options = get_arguments()
    target_ip = str(options)
    get_mac_addresses(target_ip)

if __name__ == "__main__":
    main()
