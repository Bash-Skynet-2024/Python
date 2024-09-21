#!/usr/bin/env python

import re # for examining specific part of output
import subprocess  # run external commands from python script
import optparse  # providing options for handling command-line arguments

def get_arguments():
    parser = optparse.OptionParser()    #create object "parser"
    parser.add_option("-i", "--interface", dest="interface", help="network interface")
    parser.add_option("-m", "--mac address", dest="new_mac", help="new mac address")
    (options, arguments) = parser.parse_args()  # collect arguments in options, arguments variable
    if not options.interface:  # if not entered value show error
        parser.error("Please enter network intrface")
    elif not options.new_mac:
        parser.error("Please enter new mac address")
    return options   # return options variale

def get_current_mac(interface):
    # store output of ifconfig wlan0 after decoding it
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()

    # search for mac address format values and store first found value
    current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result).group(0)
    print("Current mac address : " + current_mac)  # print current mac add

def change_mac(interface, new_mac):

    get_current_mac(interface)  # mac address before executing function

    print("Changing mac address for " + interface + " to " + new_mac + "......")
    subprocess.run(["ifconfig", interface, "down"])  # commands to change mac address
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])

    get_current_mac(interface)  # mac address after executing function

def main(): # collect arguments and run function to change mac
    options = get_arguments()
    change_mac(options.interface, options.new_mac)

if __name__ == "__main__":
    main()
