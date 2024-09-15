import socket
def scan_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.01)  # Set timeout for the connection
        result = s.connect_ex((host, port))  # Try to connect to the port
        return result == 0
def main():
    host = input("Enter the hostname or IP address: ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))
    print(f"Scanning ports from {start_port} to {end_port} on {host}...")
    for port in range(start_port, end_port + 1):
        if scan_port(host, port):
            print(f"Port {port} is open")
if __name__ == "__main__":
    main()
