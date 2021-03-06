from email import message
import paho.mqtt.client as mqtt
from datetime import datetime
from mqttNetwork.dataBase import Database
import controller.main as main
import json
from pydoc import cli


class MqttClientData:


    def on_connect(self, client, userdata, flags, rc):
        print("****** Connected with result code "+str(rc) + " ******\n")
        self.client.subscribe("status_data")
        self.client.subscribe("status_outside")
        self.client.subscribe("actuator_data")


    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        
        if msg.topic == "status_data" :
            self.message = str(msg.payload)
            data = json.loads(msg.payload)
            node_id = data["node"]
            temperature = data["temperature"]
            humidity = data["humidity"]
            co2 = data["co2"]
            dt = datetime.now()
            cursor = self.connection.cursor()
            sql = "INSERT INTO `data` (`id_node`, `timestamp`, `temperature`, `humidity`, `co2`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (node_id, dt, temperature, humidity, co2))
            self.connection.commit()
            
            # cursor = self.connection.cursor()
            # sql = "SELECT watering FROM actuator ORDER BY ID DESC LIMIT 1"
            # cursor.execute(sql)
            # result_set = cursor.fetchall()
            # if result_set == "watering" :
            #      self.client.publish("actuator","wat")
            # else:
            #      self.client.publish("actuator","notWat")

            # cursor = self.connection.cursor()
            # sql = "SELECT value FROM window_actuator ORDER BY ID DESC LIMIT 1"
            # cursor.execute(sql)
            # result_set = cursor.fetchall()
            # if result_set == "open" :
            #      self.client.publish("actuator","open")
            # else:
            #      self.client.publish("actuator","notOpen")
        elif msg.topic == "status_outside" :
            self.message = str(msg.payload)
            data = json.loads(msg.payload)
            node_id = data["node"]
            tempOut = data["tempOut"]
            main.temperatureOutside = tempOut


    def mqtt_client(self):
        self.db = Database()
        self.connection = self.db.connect_db()
        self.message = ""
        self.tempMax = 35
        self.tempMin = 20
        self.humMax = 80
        self.humMin = 35
        self.co2Max = 2000
        self.co2Min = 1000
        print("\n****** Mqtt client Temperature Humidity Co2 starting ******")
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect("127.0.0.1", 1883, 60)
        except Exception as e:
            
           print(str(e))
        self.client.loop_forever()