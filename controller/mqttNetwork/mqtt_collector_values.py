from ast import Return
from email import message
import paho.mqtt.client as mqtt
from datetime import datetime
from database.dataBase import Database
#import main as main
import json
from pydoc import cli
from coapNetwork.addresses import Addresses
from coapNetwork.sendpost import Post

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
            self.checkActuator(temperature, humidity, co2)
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
        # elif msg.topic == "status_outside" :
        #     self.message = str(msg.payload)
        #     data = json.loads(msg.payload)
        #     node_id = data["node"]
        #     tempOut = data["tempOut"]
        #     main.temperatureOutside = tempOut

    def checkActuator(self, temp, hum, co2):
        if self.shouldOpenWatering(temp, hum, self.tempMax, self.humMax, self.humMin) :
            self.startWatering()
        
    
    def startWatering(self):

        for ad in Addresses.address :
            print(ad)
            status = self.executeLastState(ad)
            if status is not None:
                if status == 0:
                    Post.changeStatus(status, ad)
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (ad, dt, 1))
                    print("\nSTATUS = " + status)
                    self.connection.commit()
                if status == 2:
                    return
            else:
                Post.changeStatus(status, ad)
                dt = datetime.now()
                cursor = self.connection.cursor()
                sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (ad, dt, 1))
                print("\nSTATUS = " + status)
                self.connection.commit()


    def executeLastState(self, address) :
        cursor = self.connection.cursor()
        sql = "SELECT status FROM actuator_watering WHERE address = %s ORDER BY address DESC LIMIT 1"
        cursor.execute(sql, str(address))
        result_set = cursor.fetchall()
        rows = [x.values() for x in result_set]
        if rows[0] is not None :
            print("result set"+rows[0])
        else:
            print("vuoto")
        if rows is None:
            return None
        else: 
            return rows[0]


    def shouldOpenWatering(self, t, h, t_max, h_max, h_min):
        return h < (h_min) or (t > (t_max) and h < (h_max))
    

    def mqtt_client(self, tempMax, tempMin, humMax, humMin, co2Max, co2Min):
        self.db = Database()
        self.connection = self.db.connect_db()
        self.message = ""
        self.tempMax = tempMax
        self.tempMin = tempMin
        self.humMax = humMax
        self.humMin = humMin
        self.co2Max = co2Max
        self.co2Min = co2Min
        print("\n****** Mqtt client Temperature Humidity Co2 starting ******")
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect("127.0.0.1", 1883, 60)
        except Exception as e:
            
           print(str(e))
        self.client.loop_forever()