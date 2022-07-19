from pydoc import cli
from mqttNetwork.mqtt_collector import MqttClient

# if __name__ == "__main__":

#     client = MqttClient()
#     client.mqtt_client()
 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("status")
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect= on_connect
client.on_message= on_message
client.connect("127.0.0.1", 1883, 60)
client.publish("alert", payload="ciao")
client.loop_forever()