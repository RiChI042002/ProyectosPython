# Importamos librerias
from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np
import paho.mqtt.client as mqtt



def cambiar(dato):
   
    if (dato[0] == "v"):
        
        velocidad.set(dato[1:])
        
    elif(dato[0] == "b"):
        
        Bateria.set(dato[1:])
    
    elif(dato[0] == "h"):
        Humedad.set(dato[1:])


def enviar():
    
    print ("Enviar")
    asd=str("d"+slider1.get())+","+str(slider11.get())
    MiMQTT.publish("Carro",asd)
    


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
            lblVideo.after(10, visualizar)

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
    Variable=0
    


# Funcion iniciar
def iniciar():
    global cap
    # Elegimos la camara
    cap = cv2.VideoCapture(0)
    visualizar()
    

# Funcion finalizar
def finalizar():
    cap.release()
    cv2.DestroyAllWindows()
    

    



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
imagenF = PhotoImage(file="/Users/richi4/universidad/semestre VIII/Robotica/Rover/Imagenes/Fondo.png")
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
imagenBI = PhotoImage(file="/Users/richi4/universidad/semestre VIII/Robotica/Rover/Imagenes/Inicio.png")
inicio = Button(pantalla, text="Iniciar", image=imagenBI, height="40", width="200", command=iniciar)
inicio.place(x = 100, y = 580)

# Finalizar Video
imagenBF = PhotoImage(file="/Users/richi4/universidad/semestre VIII/Robotica/Rover/Imagenes/Finalizar.png")
fin = Button(pantalla, text="Finalizar", image= imagenBF, height="40", width="200", command=finalizar)
fin.place(x = 980, y = 580)

# Velocidad


velocidad =crearCuadroTextoPequeño(1050,150,980,150,"Velocidad")


#Bateria

Bateria = crearCuadroTextoPequeño(1050,200,980,200,"Bateria")



#Humedad

Humedad = crearCuadroTextoPequeño(1050,250,980,250,"Humedad")

# Sliders-botones

# Velocidad 

veloCarro=Label(pantalla, text="Velocidad:")
veloCarro.place(x=150, y= 140)

slider1 = Scale(pantalla, from_ = 0, to = 255, orient=HORIZONTAL)
slider1.place(x = 80, y = 180)

slider11 = Scale(pantalla, from_ = 0, to = 255, orient=HORIZONTAL)
slider11.place(x = 190, y = 180)


# luces

Luces=Label(pantalla, text="Luces:")
Luces.place(x=150, y= 240)

on=Button(pantalla,text="on",width=7,command=lambda:enviar())
on.place(x=80,y=280)

off=Button(pantalla,text="off",width=7,command=lambda:luzp)
off.place(x=190,y=280)


auto=Button(pantalla,text="autodestruccion",width=23,command=lambda:luzp)
auto.place(x=80,y=340)


# Video
lblVideo = Label(pantalla)
lblVideo.place(x = 320, y = 50)

lblVideo2 = Label(pantalla)
lblVideo2.place(x = 470, y = 500)



    


def ConectarMQTT(client, userdata, flags, rc):
    print("Conencando al Servidor - " + str(rc))
    MiMQTT.subscribe("PC")


def MensajeMQTT(client, userdata, msg):
    print(f"Mensaje secreto: {msg.topic} - {str(msg.payload)}")
    h=str(msg.payload.decode("utf-8"))
    
    cambiar(h)
    print(type(h))
    


def EnviandoMQTT(client, obj, mid):
    print("Mesaje: " + str(mid))


def SubcribiendoMQTT(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def LogMQTT(client, obj, level, string):
    print(f"Log: {string}")

print("algo")
MiMQTT = mqtt.Client()
MiMQTT.on_connect = ConectarMQTT
MiMQTT.on_publish = EnviandoMQTT
MiMQTT.on_message = MensajeMQTT
MiMQTT.on_subscribe = SubcribiendoMQTT
MiMQTT.on_log = LogMQTT


    
MiMQTT.username_pw_set("roveralv", "JustMe")
MiMQTT.connect("roveralv.cloud.shiftr.io", 1883)

MiMQTT.loop_start()



pantalla.mainloop()

