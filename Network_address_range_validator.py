import ipaddress
def validate_ip_in_network(ip, network):
    ip_obj = ipaddress.ip_address(ip)
    net_obj = ipaddress.ip_network(network)
    return ip_obj in net_obj
def main():
    ip_add = input("enter ip address : ")
    network = input("enter network with cidr notation : ")
    if validate_ip_in_network(ip_add, network):
        print(f" ip address : {ip_add} is present in network : {network}")
    else:
        print(f" ip address : {ip_add} not found  in network : {network}")
if __name__ == "__main__":
    main()
