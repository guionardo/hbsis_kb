import avro.schema
import base64


import paho.mqtt.client as mqtt
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter


cs = '''{"namespace": "example.avro",
 "type": "record",
 "name": "User",
 "fields": [
     {"name": "name", "type": "string"},
     {"name": "favorite_number",  "type": ["int", "null"]},
     {"name": "favorite_color", "type": ["string", "null"]}
 ]
}'''

schema = avro.schema.Parse(cs)
writer = DataFileWriter(open("users.avro", "wb"), DatumWriter(), schema)
writer.append({"name": "Alyssa", "favorite_number": 256})
writer.append({"name": "Ben", "favorite_number": 7, "favorite_color": "red"})
writer.close()

reader = DataFileReader(open("users.avro", "rb"), DatumReader())
for user in reader:
    print(base64.encodebytes(user))
reader.close()


def on_connect(client, userdata, flags, rc):
    print("Conectado: "+str(rc))
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883, 60)
client.subscribe('public')
msg = client.publish('public','Teste')
print(msg)
# client.loop_forever()