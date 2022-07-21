from email import message
import paho.mqtt.client as mqtt
from datetime import datetime
from mqttNetwork.dataBase import Database
import json
from pydoc import cli


class MqttClient:

    message = "dio povero"
    tempMax = 35
    tempMin = 20
    humMax = 80
    humMin = 35
    co2Max = 2000
    co2Min = 1000

    def on_connect(self, client, userdata, flags, rc):
        print("****** Connected with result code "+str(rc) + "******\n")
        self.client.subscribe("status")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        #print("msg topic: " + str(msg.payload))
        self.message = str(msg.payload)
        data = json.loads(msg.payload)
        node_id = data["node"]
        temperature = data["temperature"]
        humidity = data["humidity"]
        co2 = data["co2"]
        dt = datetime.now()
        timestamp = datetime.timestamp(dt)
        cursor = self.connection.cursor()
        sql = "INSERT INTO `data` (`id_node`, `timestamp`, `temperature`, `humidity`, `co2`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (node_id, dt, temperature, humidity, co2))
        self.connection.commit()


    
    def mqtt_client(self):
        self.db = Database()
        self.connection = self.db.connect_db()
        self.message = "ciao"
        print("\n****** Mqtt client starting ******")
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect("127.0.0.1", 1883, 60)
        except Exception as e:
            
           print(str(e))
        self.client.loop_forever()