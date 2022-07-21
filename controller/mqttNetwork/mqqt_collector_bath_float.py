from email import message
import paho.mqtt.client as mqtt
from datetime import datetime
from mqttNetwork.dataBase import Database
import json
from pydoc import cli


class MqttClientBathFloat:

    def on_connect(self, client, userdata, flags, rc):
        print("****** Connected with result code "+str(rc) + " ******\n")
        self.client.subscribe("status_bathFloat")
        self.client.subscribe("actuator_bathFloat")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        #print("msg topic: " + str(msg.payload))
        self.message = str(msg.payload)
        data = json.loads(msg.payload)
        node_id = data["node"]
        level = data["level"]
        dt = datetime.now()
        timestamp = datetime.timestamp(dt)
        cursor = self.connection.cursor()
        sql = "INSERT INTO `bath_float` (`id_node`, `timestamp`, `level`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (node_id, dt, level))
        self.connection.commit()
        
        # cursor = self.connection.cursor()
        # sql = "SELECT value FROM watering_actuator ORDER BY ID DESC LIMIT 1"
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


    def mqtt_client(self):
        self.db = Database()
        self.connection = self.db.connect_db()
        self.message = ""
        self.level = 80
        print("\n****** Mqtt client bath float starting ******")
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect("127.0.0.1", 1883, 60)
        except Exception as e:
            
           print(str(e))
        self.client.loop_forever()