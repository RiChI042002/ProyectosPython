
import paho.mqtt.client as mqtt
import numpy as np
import threading


class ELPC():
    def __init__(self, user="roveralv", password="JustMe", host="roveralv.cloud.shiftr.io", port=1883) -> None:
        
        
        self.pc=mqtt.Client(client_id="INTERFAZ", clean_session=True)
        self.pc.on_connect = self.Conectar
        
        self.pc.username_pw_set(user, password)
        self.pc.connect(host, port)
        
        
        t=threading.Thread(target=self.suscribe)       # make a thread to loop for subscribing
        t.start()
        
    def suscribe(self):
        self.pc.loop_start()
        
        
    def Conectar(self,client, userdata, flags, rc):
        self.pc.subscribe("PC")
    
    
    def enviar(self,topic,mens):
        self.pc.publish(topic, mens)
   
        
    
 
     
        
        
 


        
        
        
        
    
        