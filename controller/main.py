import json
from pydoc import cli
from mqttNetwork.dataBase import Database
from mqttNetwork.mqtt_collector import MqttClient
import paho.mqtt.client as mqtt
from datetime import datetime




# if __name__ == "__main__":

#     client = MqttClient()
#     client.mqtt_client()
 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print("recive")
    client.subscribe("status")
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("msg topic: " + str(msg.payload))
    data = json.loads(msg.payload)
    node_id = data["node"]
    temperature = data["temperature"]
    humidity = data["humidity"]
    co2 = data["co2"]
    dt = datetime.now()
    timestamp = datetime.timestamp(dt)
    db = Database()
    connection = db.connect_db()
    cursor = connection.cursor()
    sql = "INSERT INTO `data` (`id_node`, `timestamp`, `temperature`, `humidity`, `co2`) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (node_id, timestamp, temperature, humidity, co2))
    connection.commit()


client = mqtt.Client()
client.on_connect= on_connect
client.on_message= on_message
client.connect("127.0.0.1", 1883, 60)
client.publish("alert", payload="ciao")
client.loop_forever()