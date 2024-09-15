import ipaddress
def calculate_subnets(ip_network, new_prefix):
    network = ipaddress.ip_network(ip_network, strict=False)
    print(f" original network/ CIDR notation : {network}")
    print(f" network address : {network.network_address} ")
    print(f" broadcast address : {network.broadcast_address}")
    print(f" subnet mask : {network.netmask}")
    subnets = list(network.subnets(new_prefix=new_prefix))
    print("\n subnets : ")
    for subnet in subnets:
        print("============================================")
        print(f" subnet/CIDR notation : {subnet}")
        print(f" network_address : {subnet.network_address}")
        print(f" broadcast address : {subnet.broadcast_address}")
        print(f" subnet mask : {subnet.netmask}")
        print(f" total hosts : {subnet.num_addresses - 2} ")
def calculate_supernets(ip_networks):
    networks = [ipaddress.ip_network(network, strict=False) for network in ip_networks]
    supernets = ipaddress.collapse_addresses(networks)
    for supernet in supernets:
        print("=============================================")
        print(f" supernet / CIDR notation : {supernet}")
        print(f" network address : {supernet.network_address}")
        print(f" broadcast address : {supernet.broadcast_address}")
        print(f" subnet mask : {supernet.netmask}")
        print(f" total hosts : {supernet.num_addresses -2 }")
def main():
    choice = int(input(" enter choice : 1 for subnetting, 2 for supernetting : "))
    if choice == 1:
        ip_network = input("enter the network ip address : ")
        new_prefix = int(input("enter new prefix for subnets : "))
        calculate_subnets(ip_network, new_prefix)
    elif choice == 2:
        num_networks = int(input("enter number of networks : "))
        networks = [input(f" enter network {i+1} : " ) for i in range(num_networks)]
        calculate_supernets(networks)
    else:
        print("invalid choice")
if __name__ == "__main__":
    main()

