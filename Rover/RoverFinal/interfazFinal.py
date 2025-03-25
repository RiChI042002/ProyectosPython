# Importamos las librerías necesarias
from tkinter import *
from PIL import Image, ImageTk
import imutils
import socket, cv2, pickle, struct
import threading, keyboard

# Creamos un socket del cliente
cliente = socket.socket()

# Definimos la dirección IP del Rover
host_ip = "192.168.0.4"

# Definimos el puerto para la comunicación
port2 = 9998

# Creamos una tupla con la dirección IP y el puerto
socket_address2 = (host_ip, port2)

# Inicializamos algunas variables
h = True
Defecto1 = "100"
Defecto2 = "100"

# Función para capturar video desde la cámara del rover


def teclas():
    ver=True
    while True:
        
        if keyboard.is_pressed("w") and ver:
            cliente.send("w".encode("utf-8"))
            ver=False
        elif keyboard.is_pressed("a") and ver:
            cliente.send("a".encode("utf-8"))
            ver=False
        elif keyboard.is_pressed("s") and ver:
            cliente.send("s".encode("utf-8"))
            ver=False
        elif keyboard.is_pressed("d") and ver:
            cliente.send("d".encode("utf-8"))
            ver=False
        else:
            ver=True
        
            

def camera():
    
    
    global pantalla, frame, host_ip
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
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
        

        

# Función para mostrar el video en la interfaz de usuario
def visualizar():


    # Leemos la captura de video
    if cap is not None:
        ret, frame = cap.read()

        # Si la lectura es exitosa
        if ret == True:
            # Convertimos el formato de color de BGR a RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Redimensionamos el video
            frame = imutils.resize(frame, width=640)

            # Convertimos el video a formato compatible con GUI
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            # Mostramos la imagen en la ventana GUI
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, camera)
        else:
            cap.release()

# Función para crear cuadros de texto pequeños en la interfaz
def crearCuadroTextoPequeño(x1, y1, x2, y2, coso):
    nombre = StringVar()

    cuadroName = Entry(pantalla, textvariable=nombre)
    cuadroName.place(x=x1, y=y1)

    nameLabel = Label(pantalla, text=coso + ":")
    nameLabel.place(x=x2, y=y2)

    return nombre

# Función para controlar la luz del rover
def luzp():
    cliente.send("w".encode("utf-8"))

# Función para solicitar apagar la luz del rover
def luso():
    cliente.send("j".encode("utf-8"))
    
def finalizar():
    cliente.close()

    if cap is not None:     
        cap.release()

# Función para iniciar la captura de video y comunicación de datos con el rover
def iniciar():
    hr = threading.Thread(target=camera)
    hr.start()

    cliente.connect(socket_address2)

    da = threading.Thread(target=Datasw)
    da.start()


# Función para enviar datos al rover
def Datasw():
    global Defecto1, Defecto2
    while True:
        ahoras1 = str(slider1.get())
        ahoras2 = str(slider11.get())
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

# Variables
cap = None


# Creación de la ventana principal
pantalla = Tk()
pantalla.title("Rover-1.0")
pantalla.geometry("1280x720")  # Definimos las dimensiones de la ventana

# Fondo de la ventana
imagenF = PhotoImage(file="/Users/richi4/universidad/semestreVIII/Robotica/Rover/RoverFinal/Imagenes/Fondo.png")
background = Label(image=imagenF, text="Fondo")
background.place(x=0, y=0, relwidth=1, relheight=1)

# Interfaz de usuario
texto1 = Label(pantalla, text="Video: ")
texto1.place(x=580, y=10)

texto2 = Label(pantalla, text="Datos: ")
texto2.place(x=1010, y=100)

texto3 = Label(pantalla, text="Variables: ")
texto3.place(x=110, y=100)

# Botones
# Iniciar Video

imagenBI = PhotoImage(file="/Users/richi4/universidad/semestreVIII/Robotica/Rover/RoverFinal/Imagenes/Inicio.png")
inicio = Button(pantalla, text="Iniciar", image=imagenBI, height="40", width="200", command=iniciar)
inicio.place(x = 100, y = 580)

# Finalizar Video
imagenBF = PhotoImage(file="/Users/richi4/universidad/semestreVIII/Robotica/Rover/RoverFinal/Imagenes/Finalizar.png")
fin = Button(pantalla, text="Finalizar", image= imagenBF, height="40", width="200", command=finalizar)
fin.place(x = 980, y = 580)

# Velocidad
velocidad = crearCuadroTextoPequeño(1050, 150, 980, 150, "Velocidad")
velocidad.set("0")

# Batería
Bateria = crearCuadroTextoPequeño(1050, 200, 980, 200, "Bateria")
Bateria.set("0")

# Humedad
Humedad = crearCuadroTextoPequeño(1050, 250, 980, 250, "Humedad")
Humedad.set("0")

# Sliders y botones
veloCarro = Label(pantalla, text="Velocidad:")
veloCarro.place(x=150, y=140)

slider1 = Scale(pantalla, from_=0, to=100, orient=HORIZONTAL)
slider1.place(x=80, y=180)
slider1.set(Defecto1)

slider11 = Scale(pantalla, from_=0, to=100, orient=HORIZONTAL)
slider11.place(x=190, y=180)
slider11.set(Defecto2)

on = Button(pantalla, text="Enviar", width=7, command=lambda: luzp())
on.place(x=80, y=280)

off = Button(pantalla, text="Pedir", width=7, command=lambda: luso())
off.place(x=190, y=280)

auto = Button(pantalla, text="algo", width=10, command=lambda: luzp)
auto.place(x=80, y=340)

# Ventana de video
lblVideo = Label(pantalla)
lblVideo.place(x=320, y=50)

ky = threading.Thread(target=teclas)
ky.start()


# Iniciamos la aplicación
pantalla.mainloop()