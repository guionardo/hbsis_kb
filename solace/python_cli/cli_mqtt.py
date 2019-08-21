import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Conectado: "+str(rc))
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883, 60)
TOPIC = 'public'
client.subscribe(TOPIC,1)
client.loop_forever()