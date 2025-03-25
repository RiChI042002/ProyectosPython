# Importamos librerias
from tkinter import *
from PIL import Image, ImageTk
import imutils
import socket,cv2, pickle,struct
import threading
import socket



cliente = socket.socket()
host_ip = "192.168.0.4"
port2 = 9998
socket_address2 = (host_ip,port2)

h=True
Defecto1="100"
Defecto2="100"


    
def camera():
    
    
    global pantalla, frame, rgb, hsv, gray, slival1, slival11, slival2, slival22, slival3, slival33, slival4, slival44
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.0.4' # paste your server ip address here
    port = 9999
    client_socket.connect((host_ip,port)) # a tuple
    data = b""
    payload_size = struct.calcsize("Q")
    
    
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)
            if not packet: break
            data+=packet
            
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
            
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        
        frame = imutils.resize(frame, width=640)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

                # Mostramos en el GUI
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizar)
        key = cv2.waitKey(1) & 0xFF
    client_socket.close()
    
    
    
    


# Funcion Visualizar
def visualizar():
    
    
    global pantalla, frame, rgb, hsv, gray, slival1, slival11, slival2, slival22, slival3, slival33, slival4, slival44
    # Leemos la videocaptura
    if cap is not None:
        ret, frame = cap.read()

        # Si es correcta
        if ret == True:

            
            # Color BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            


            # Rendimensionamos el video
            frame = imutils.resize(frame, width=640)

            # Convertimos el video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            # Mostramos en el GUI
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, camera)

        else:
            cap.release()


def crearCuadroTextoPequeño(x1,y1,x2,y2,coso):

	nombre=StringVar()

	cuadroName=Entry(pantalla,textvariable=nombre)
	cuadroName.place(x=x1,y=y1)
	


	nameLabel=Label(pantalla, text=coso+":")
	nameLabel.place(x=x2,y=y2)
	


	return nombre

def luzp():
    cliente.send("w".encode("utf-8"))
    


# Funcion iniciar
def iniciar():
    global comoes 
    comoes=True
    hr=threading.Thread(target=camera) 
    hr.start()
    
    cliente.connect(socket_address2)
    
    da=threading.Thread(target=Datasw)
    da.start()

    

def Datasw():
    global Defecto1,Defecto2
    while True:

        ahoras1=str(slider1.get())
        ahoras2=str(slider11.get())
        if ahoras1 != Defecto1: 
            cliente.send(ahoras1.encode("utf-8"))
            Defecto1 = ahoras1

        if ahoras2 != Defecto2: 
            cliente.send(ahoras2.encode("utf-8"))
            Defecto2 = ahoras2
            
        dato = cliente.recv(64)
        
        if not dato:
            print("desconectado")
        else:
            dato = dato.decode('utf-8')
            if dato[0] == "V": velocidad.set(dato[1:])
            elif dato[0] == "B": Bateria.set(dato[1:])
            elif dato[0] == "H": Humedad.set(dato[1:])    
         
               



def luso():
    cliente.send("j".encode("utf-8"))



# Variables
cap = None
hsv = 0
gray = 0
rgb = 1
detcolor = 0





#  Ventana Principal

# Pantalla
pantalla = Tk()
pantalla.title("Rover-1.0")
pantalla.geometry("1280x720")  # Asignamos la dimension de la ventana

# Fondo
imagenF = PhotoImage(file="Imagenes/Fondo.png")
background = Label(image = imagenF, text = "Fondo")
background.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# Interfaz
texto1 = Label(pantalla, text="Video: ")
texto1.place(x = 580, y = 10)

texto2 = Label(pantalla, text="Datos: ")
texto2.place(x = 1010, y = 100)

texto3 = Label(pantalla, text="Variables: ")
texto3.place(x = 110, y = 100)

# Botones
# Iniciar Video
imagenBI = PhotoImage(file="Imagenes/Inicio.png")
inicio = Button(pantalla, text="Iniciar", image=imagenBI, height="40", width="200", command=iniciar)
inicio.place(x = 520, y = 580)


# Velocidad


velocidad =crearCuadroTextoPequeño(1050,150,980,150,"Velocidad")
velocidad.set("0")


#Bateria

Bateria = crearCuadroTextoPequeño(1050,200,980,200,"Bateria")
Bateria.set("0")


#Humedad

Humedad = crearCuadroTextoPequeño(1050,250,980,250,"Humedad")
Humedad.set("0")

# Sliders-botones

# Velocidad 

veloCarro=Label(pantalla, text="Velocidad:")
veloCarro.place(x=150, y= 140)

slider1 = Scale(pantalla, from_ = 0, to = 100, orient=HORIZONTAL)
slider1.place(x = 80, y = 180)
slider1.set(Defecto1)

slider11 = Scale(pantalla, from_ = 0, to = 100, orient=HORIZONTAL)
slider11.place(x = 190, y = 180)
slider11.set(Defecto2)


# luces


on=Button(pantalla,text="Enviar",width=7,command=lambda:luzp())
on.place(x=80,y=280)

off=Button(pantalla,text="Pedir",width=7,command=lambda:luso())
off.place(x=190,y=280)


auto=Button(pantalla,text="algo",width=10,command=lambda:luzp)
auto.place(x=80,y=340)


# Video
lblVideo = Label(pantalla)
lblVideo.place(x = 320, y = 50)

lblVideo2 = Label(pantalla)
lblVideo2.place(x = 470, y = 500)


    


    


pantalla.mainloop()

