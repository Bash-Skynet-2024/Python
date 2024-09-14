import ipaddress
import sys
def subnet_calculator(ip_address, subnet_mask) :
    network = ipaddress.ip_network(ip_address+'/'+subnet_mask, strict=False)
    return {
        'network_address': str(network.network_address),
        'broadcast_address': str(network.broadcast_address),
        'subnet_mask': str(network.netmask),
        'total_hosts': network.num_addresses - 2,
        'cidr_notation' : str(network)
    }
def print_subnet_details(details):
    print("network address : " + details['network_address'])
    print("broadcast address : " + details['broadcast_address'])
    print("subnet mask : " + details['subnet_mask'])
    print("total hosts : " + str(details['total_hosts']))
    print("cidr notation : " + details['cidr_notation'])
def main():
    ip_address = sys.argv[1]
    subnet_mask = sys.argv[2]
    details = subnet_calculator(ip_address, subnet_mask)
    print_subnet_details(details)
if __name__ == "__main__" :
    main()
