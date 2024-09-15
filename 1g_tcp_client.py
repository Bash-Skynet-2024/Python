import socket
#enter server ip address and port on which server is listening
def communicate_with_server(host, port):
    # socket object s with ipv4 and tcp to connect to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1800) # try till 5 seconds to establish connection
        s.connect((host, port)) #send connection request
        print(f" connected to server : {host} on port {port} ")
        for i in range(100):
            message =  input("enter message to send : ")

            s.sendall(message.encode('utf-8'))
            data = s.recv(16*16*16*1024*1024)

            print(f"server : {data.decode('utf-8')}")
if __name__ == "__main__":
    host = input("enter server ip address : ")
    port = int(input("enter port number : "))
    communicate_with_server(host, port)

