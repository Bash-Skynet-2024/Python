from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
def scan_network(ip_network, iface):
    arp = ARP(pdst=ip_network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = arp/ether
    result = srp(packet, timeout=10, verbose=0, iface=iface)[0]
    devices = []
    for sent, recieved in result:
        devices.append({'ip': recieved.psrc, 'mac': recieved.hwsrc})
    return devices
def print_devices(devices):
    print("ip address\t\tmac address")
    print("============================================================")
    for device in devices:
        print(f"{device['ip']} \t\t {device['mac']}")
def main():
    ip_network = input("enter network ip address : ")
    iface = input("enter network interface : ")
    devices = scan_network(ip_network, iface)
    print_devices(devices)
if __name__ == "__main__":
    main()





