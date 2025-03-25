import socket
import keyboard


server_socket2 = socket.socket()

host_name  = socket.gethostname()

host_ip = "192.168.0.28"


port2 = 9998

socket_address2 = (host_ip,port2)

server_socket2.bind(socket_address2)

server_socket2.listen(5)
print("LISTENING 2 AT:",socket_address2)

while True:
    client_socket,addr = server_socket2.accept()
    print("conectado")
    
    while True:
        h=input().encode("utf-8")
        client_socket.send(h)

    server_socket2.close()        
        
    
    