import RPi.GPIO as GPIO
import time

# Configura el modo de GPIO en BCM
GPIO.setmode(GPIO.BCM)

# Define el pin GPIO al que está conectado el sensor analógico
Humedad = 17
bateria = 27

# Configura el pin GPIO como entrada

GPIO.setup(Humedad, GPIO.IN)

def Humedad():

    try:
        while True:
            # Lee el valor analógico del sensor
            valor_analogico = GPIO.input(Humedad)
            
            # Imprime el valor leído
            print("Valor analógico:", valor_analogico)
            

    except KeyboardInterrupt:
        # Maneja una interrupción del teclado (Ctrl+C) para finalizar el programa
        pass

    finally:
        # Limpia los pines GPIO y sale del programa
        GPIO.cleanup()
        
def bateria():
    try:
        while True:
            # Lee el valor analógico del sensor
            valor_analogico = GPIO.input(bateria)
            
            # Imprime el valor leído
            print("Valor analógico:", valor_analogico)
            
            
    except KeyboardInterrupt:
        # Maneja una interrupción del teclado (Ctrl+C) para finalizar el programa
        pass

    finally:
        # Limpia los pines GPIO y sale del programa
        GPIO.cleanup()