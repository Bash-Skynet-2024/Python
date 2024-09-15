# import socket library
import socket
#fucntion to start server which will send and recieve data
def start_server(port):
    # with is used to close connection after work is done
    # s is the socket object used for server
    # socket.AF_INET means ipv4 , socket.SOCK_STREAM means tcp protocol
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # port - on the port where we want to listen which was found open
        # 0.0.0.0 means accepting connection from all interfaces
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f" server is listening on port : {port}")
        # s.accept() for accepting any incoming connection request
        #create socket object "conn" with address "addr" of client to communicate
        conn, addr = s.accept()
        print(f"connection from {addr} has been successfully established")
        for i in range(100):
            data = conn.recv(16*16*16*1024*1024) # data recieved will be stored , max size 1024 bytes

            # utf-8 for conversion of data from unicode to ascii
            print(f" recieved from client : {data.decode('utf-8')}")
            message = input("enter message to send : ")
            conn.sendall(message.encode('utf-8')) # use conn obj to send data by encoding
        conn.close()

if __name__ == "__main__":
    port = int(input("enter port number to listen on : "))
    start_server(port)

