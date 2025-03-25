# Importación de módulos necesarios
import RPi.GPIO as GPIO
import time
from pyPS4Controller.controller import Controller
import socket, cv2, pickle, struct, imutils
import threading, random

# Creación de sockets para comunicación
serverVideo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverDatos = socket.socket()

# Configuración de la dirección IP y puertos
host_name = socket.gethostname()
host_ip = "192.168.0.4"
port = 9999
port2 = 9998
socket_address = (host_ip, port)
socket_address2 = (host_ip, port2)

# Enlace de sockets a direcciones IP y puertos
serverVideo.bind(socket_address)
serverDatos.bind(socket_address2)

# Escucha en los sockets
serverVideo.listen(5)
serverDatos.listen(5)
print("LISTENING 1 AT:", socket_address)
print("LISTENING 2 AT:", socket_address2)


# Configuración de pines GPIO para control de motores
GPIO.setmode(GPIO.BOARD)

motor_pins = [12, 11, 15, 16]

for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

GPIO.setup(32, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

pwma = GPIO.PWM(32, 1000)
pwmb = GPIO.PWM(33, 1000)

pwma.start(0)
pwmb.start(0)

#variables Rover

velder=1
velizq=1


def EnviarDatos(cliente):
    cliente.send(("H{}".format(random.randrange(-100, 100))).encode("utf-8"))
    time.sleep(0.1)
    cliente.send(("B{}".format(random.randrange(-100, 100))).encode("utf-8"))
    time.sleep(0.1)
    cliente.send(("V{}".format(random.randrange(-100, 100))).encode("utf-8"))

    

# Función para transmitir video desde la cámara
def Trasmitir():
    while True:
        client_socket, addr = serverVideo.accept()
        print('GOT CONNECTION FROM:', addr)
        if client_socket:
            vid = cv2.VideoCapture(0)
            while vid.isOpened():
                img, frame = vid.read()
                frame = imutils.resize(frame, width=320)
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()

# Inicia la función de transmisión de video en un hilo
def empiece(cliente):
    Video = threading.Thread(target=Trasmitir) 
    Video.start()

    

# Funciones para controlar el movimiento del rover


def controlar_movimiento(velocidad_izquierda, velocidad_derecha):
    
    GPIO.output(motor_pins[0], GPIO.HIGH if velocidad_izquierda > 0 else GPIO.LOW)
    GPIO.output(motor_pins[1], GPIO.HIGH if velocidad_izquierda < 0 else GPIO.LOW)
    GPIO.output(motor_pins[2], GPIO.HIGH if velocidad_derecha > 0 else GPIO.LOW)
    GPIO.output(motor_pins[3], GPIO.HIGH if velocidad_derecha < 0 else GPIO.LOW)
    pwma.ChangeDutyCycle(abs(velocidad_izquierda)*velizq)
    pwmb.ChangeDutyCycle(abs(velocidad_derecha)*velder)



# Clase que maneja el controlador de PS4
class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    # Callback cuando se presiona el botón R2
    def on_R2_press(self, value):
       value = value + 32800
       value = value * 100 / 65600
       print(int(value))
       return value

    # Callback cuando se suelta el botón R2
    def on_R2_release(self):
       print("Quieto")

# Inicializa el controlador de PS4
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

Ya=True

# Bucle principal
while True:
    
    Datos, addr = serverDatos.accept()
    # Inicia la función de transmisión de video una vez
    if Ya:
        empiece(Datos)
        Ya = False
    
    # Maneja la conexión de datos
    
    print("conectado")
    
    while True:
        dato = Datos.recv(64)
        
        if not dato:
            print("desconectado")
            break
        else:
            dato = dato.decode('utf-8')
            
            # Controla el movimiento del rover según los datos recibidos
            if dato == "w": 
                controlar_movimiento(40,40)
                
                
            elif dato == "d": 
                controlar_movimiento(80,-80)
                
            elif dato == "a": 
                controlar_movimiento(-80,80)
                
            elif dato == "s": 
                controlar_movimiento(-40,-40)
                
            elif dato[0:1] == "vd": 
                velder=int(dato[2:])/100
                print("cambio")
                
            elif dato[0:1] == "vi": 
                velizq=int(dato[2:])/100
                
            elif dato == "p":
                controlar_movimiento(0,0)
            
            elif dato == "j": 
                
                Da = threading.Thread(target=EnviarDatos(Datos)) 
                Da.start()
        