#!/usr/bin/env python
import re
import subprocess
import optparse
import ipaddress

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-s", "--start_range", dest="start_range", help="enter beginning of ip range")
    parser.add_option("-e", "--end_range", dest="end_range", help="enter ending of ip range")
    (options, arguments) = parser.parse_args()
    if not options.start_range:
        parser.error("please enter beginning of ip range")
    elif not options.end_range:
        parser.error("please enter ending of ip range")
    return options

def scan_ip(start_range, end_range):
    result = subprocess.run(["sudo", "fping", "-a", "-g", start_range, end_range, "2>/dev/null"], capture_output=True, text=True)


def get_mac_addresses():
    output = subprocess.check_output(["arp", "-n"]).decode()
    for line in output.splitlines():
        ip = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", line)
        mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", line)
        if ip and mac:
            #ip1 = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", str(ip))
            #mac1 = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(mac))
            ip1 = ip.group(0)
            mac1 = mac.group(0)
            print(f"ip : {ip1} \t\t mac : {mac1}")



def main():
    options = get_arguments()
    ipaddress.ip_address(options.start_range)
    ipaddress.ip_address(options.end_range)
    scan_ip(options.start_range, options.end_range)
    get_mac_addresses()

if __name__ == "__main__":
    main()
