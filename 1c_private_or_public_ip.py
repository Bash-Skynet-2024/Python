import ipaddress
def classify_ip(ip):
    ip_obj = ipaddress.ip_address(ip)
    if ip_obj.is_private:
        print(f" ip address : {ip} is private")
    else:
        print(f" ip address : {ip} is public")
def main():
    ip = input("enter ip address : ")
    classify_ip(ip)
if __name__ == "__main__":
    main()
