import paho.mqtt.client as mqtt
import datetime

def on_connect(client, userdata, flags, rc):
    print("Conectado: "+str(rc))
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_publish(client,userdata,result):             #create function for callback
    print("PUBLISHED: "+str(userdata)+"\n")
    pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect("localhost",1883, 60)
TOPIC = 'public'
client.subscribe(TOPIC)

sair = False
id = 0
while not sair:
    msg = input('Mensagem:')
    if msg=='':
        sair = True
        continue
    id+=1
    msg = str(id)+ ' '+msg
    client.publish(topic=TOPIC,payload=msg,qos=1)
