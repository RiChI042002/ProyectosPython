# Creado ChepeCarlos de ALSW
# Tutorial Completo en https://nocheprogramacion.com
# Canal Youtube https://youtube.com/alswnet?sub_confirmation=1

import paho.mqtt.client as mqtt
import time


def ConectarMQTT(client, userdata, flags, rc):
    print("Conencando al Servidor - " + str(rc))
    MiMQTT.subscribe("PC")


def MensajeMQTT(client, userdata, msg):
    print(f"Mensaje secreto: {msg.topic} - {str(msg.payload)}")


def EnviandoMQTT(client, obj, mid):
    print("Mesaje: " + str(mid))


def SubcribiendoMQTT(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def LogMQTT(client, obj, level, string):
    print(f"Log: {string}")

print("algo")
MiMQTT = mqtt.Client(client_id="yo", clean_session=True)
MiMQTT.on_connect = ConectarMQTT
MiMQTT.on_publish = EnviandoMQTT
MiMQTT.on_message = MensajeMQTT
MiMQTT.on_subscribe = SubcribiendoMQTT
MiMQTT.on_log = LogMQTT

    
MiMQTT.username_pw_set("roveralv", "JustMe")
MiMQTT.connect("roveralv.cloud.shiftr.io", 1883)

while True:
    dato=input("type somenting: ")
    MiMQTT.publish("PC",dato)
    
    
    
    
    
MiMQTT.loop_forever()
