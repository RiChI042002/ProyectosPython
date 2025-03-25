import socket
import keyboard


cliente = socket.socket()


host_ip = "192.168.0.28"

print('HOST IP:',host_ip)

port2 = 9998

socket_address2 = (host_ip,port2)

cliente.connect(socket_address2)
while True:
    
    dato = cliente.recv(64)
    if not dato:
        print("desconectado")
        break
    else:
        dato = dato.decode('utf-8')
        if dato == "a": print("lo recibi")
            