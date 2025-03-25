#Funciones de movimiento para el Rover

import RPi.GPIO as GPIO
import time
from pyPS4Controller.controller import Controller
import keyboard
import socket, cv2, pickle,struct,imutils
import threading



# Socket Create
serverVideo = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverDatos = socket.socket()

host_name  = socket.gethostname()
host_ip = "192.168.0.4"
print('HOST IP:',host_ip)
port = 9999
port2 = 9998
Ya=True
socket_address = (host_ip,port)
socket_address2 = (host_ip,port2)

# Socket Bind
serverVideo.bind(socket_address)
serverDatos.bind(socket_address2)


# Socket Listen
serverVideo.listen(5)
serverDatos.listen(5)
print("LISTENING 1 AT:",socket_address)
print("LISTENING 2 AT:",socket_address2)

def datos():
    while True:
        client_socket,addr = serverDatos.accept()
        print("conectado")



                

GPIO.setmode(GPIO.BOARD)

h=True

motor1a=12
motor1b=11
motor2a=15
motor2b=16	

GPIO.setup(motor1a, GPIO.OUT)
GPIO.setup(motor1b, GPIO.OUT)
GPIO.setup(motor2a, GPIO.OUT)
GPIO.setup(motor2b, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

pwma=GPIO.PWM(32, 1000)
pwmb=GPIO.PWM(33, 1000)

pwma.start(0)
pwmb.start(0)

def Trasmitir():
    
    while True:
        client_socket,addr = serverVideo.accept()
        print('GOT CONNECTION FROM:',addr)
        if client_socket:
            vid = cv2.VideoCapture(0)
            
            while(vid.isOpened()):
                img,frame = vid.read()
                frame = imutils.resize(frame,width=320)
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                
                key = cv2.waitKey(1) & 0xFF
                if key ==ord('q'):
                    client_socket.close()


def empiece():
    Video=threading.Thread(target=Trasmitir) 
    Video.start()


def quieto(velocidad):
    GPIO.output(motor1a, GPIO.LOW)
    GPIO.output(motor1b, GPIO.LOW)
    GPIO.output(motor2a, GPIO.LOW)
    GPIO.output(motor2b, GPIO.LOW)    
    pwma.ChangeDutyCycle(0)
    pwmb.ChangeDutyCycle(0)

def adelante(velocidad):
    GPIO.output(motor1a, GPIO.HIGH)
    GPIO.output(motor1b, GPIO.LOW)
    GPIO.output(motor2a, GPIO.HIGH)
    GPIO.output(motor2b, GPIO.LOW)    
    pwma.ChangeDutyCycle(velocidad)
    pwmb.ChangeDutyCycle(velocidad)

def atras(velocidad):
    GPIO.output(motor1a, GPIO.LOW)
    GPIO.output(motor1b, GPIO.HIGH)
    GPIO.output(motor2a, GPIO.LOW)
    GPIO.output(motor2b, GPIO.HIGH)    
    pwma.ChangeDutyCycle(velocidad)
    pwmb.ChangeDutyCycle(velocidad)


def derrape(velocidad):
    GPIO.output(motor1a, GPIO.HIGH)
    GPIO.output(motor1b, GPIO.LOW)
    GPIO.output(motor2a, GPIO.LOW)
    GPIO.output(motor2b, GPIO.HIGH)    
    pwma.ChangeDutyCycle(velocidad)
    pwmb.ChangeDutyCycle(velocidad)
    
def derizquierda(velocidad):
    GPIO.output(motor1a, GPIO.LOW)
    GPIO.output(motor1b, GPIO.HIGH)
    GPIO.output(motor2a, GPIO.HIGH)
    GPIO.output(motor2b, GPIO.LOW)    
    pwma.ChangeDutyCycle(velocidad)
    pwmb.ChangeDutyCycle(velocidad)

def izquierda(velocidad):
    GPIO.output(motor1a, GPIO.HIGH)
    GPIO.output(motor1b, GPIO.LOW)
    GPIO.output(motor2a, GPIO.HIGH)
    GPIO.output(motor2b, GPIO.LOW)    
    pwma.ChangeDutyCycle(velocidad*0)
    pwmb.ChangeDutyCycle(velocidad)

def derecha(velocidad):
    GPIO.output(motor1a, GPIO.HIGH)
    GPIO.output(motor1b, GPIO.LOW)
    GPIO.output(motor2a, GPIO.HIGH)
    GPIO.output(motor2b, GPIO.LOW)    
    pwma.ChangeDutyCycle(velocidad)
    pwmb.ChangeDutyCycle(velocidad*0)
    
    
    


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_R2_press(self, value):
       value = value+32800
       value = value * 100 / 65600
       print(int(value))
       return value
       

    def on_R2_release(self):
       print("Quieto")

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window


while True:
    
    if Ya:
        empiece()
        Ya=False
        
    Datos,addr = serverDatos.accept()
    print("conectado")
    
    while True:
        dato = Datos.recv(64)
        
        
        if not dato:
            print("desconectado")
            break
        else:
            dato = dato.decode('utf-8')
            
            if dato == "w": 
                adelante(40)
                print("alante")
                Datos.send("a".encode("utf-8"))
            elif dato == "d": 
                derrape(80)
                print("derecha")
            elif dato == "a": 
                derizquierda(80)
                print("alante")
            elif dato == "s": 
                atras(40)
                print("alante")
            else:
                adelante(0)
    