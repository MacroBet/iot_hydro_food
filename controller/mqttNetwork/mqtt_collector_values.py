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
            self.tempIn = temperature
            self.co2In = co2
            dt = datetime.now()
            cursor = self.connection.cursor()
            sql = "INSERT INTO `data` (`id_node`, `timestamp`, `temperature`, `humidity`, `co2`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (node_id, dt, temperature, humidity, co2))
            self.connection.commit()
            self.checkActuatorWatering(temperature, humidity, co2)
           
        elif msg.topic == "status_outside" :
            self.message = str(msg.payload)
            data = json.loads(msg.payload)
            node_id = data["node"]
            tempOut = data["tempOut"]
            self.checkActuatorWindow(tempOut)

             

    def checkActuatorWindow(self, tempOut):

        if self.co2In is not None and self.tempIn is not None:
            
            delta_inTemp = abs(self.tempIn - self.tempMax) + abs(self.tempIn - self.tempMin)

            delta_outTemp = abs(tempOut - self.tempMax) + abs(tempOut - self.tempIn)

            if self.co2In < self.co2Max-200 and delta_inTemp > delta_outTemp:
                
                self.openWindow()

    def openWindow(self):
            return


    def checkActuatorWatering(self, temp, hum, co2):
        if self.shouldOpenWatering(temp, hum, self.tempMax, self.humMax, self.humMin) :
            self.startWatering()
        elif temp < (self.tempMin + 2) and hum >= ((self.humMax*70)/100) :
            self.stopWatering()
        
    def stopWatering(self):

        for ad in Addresses.adValves :
            print(ad)
            status = self.executeLastState(ad)
            if status is None:
                return
            elif status == "1":
                status = "0"
                Post.changeStatus(status, ad)
                dt = datetime.now()
                cursor = self.connection.cursor()
                sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (str(ad), dt, "0"))
                print("\nSTATUS = " + status)
                self.connection.commit()
                self.communicateToSensors("0")
            else:
                return
           

    def communicateToSensors(self, status):
    
        print("communicate")
        if status == "1":
            self.client.publish("actuator_data","wat")
        if status == "0" :
            self.client.publish("actuator_data","notWat")
                

    
    def startWatering(self):

        for ad in Addresses.adValves :
            print(ad)
            status = self.executeLastState(ad)
            if status is not None:
                if status == "0":
                    status = "1"
                    Post.changeStatus(status, ad)
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(ad), dt, "1"))
                    print("\nSTATUS = " + status)
                    self.connection.commit()
                    self.communicateToSensors(status)
                if status == "2" or status == "1":
                    return
            else:
                status = "1"
                Post.changeStatus(status, ad)
                dt = datetime.now()
                cursor = self.connection.cursor()
                sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (str(ad), dt, "1"))
                print("\nSTATUS = " + status)
                self.connection.commit()
                self.communicateToSensors(status)


    def executeLastState(self, address) :
        cursor = self.connection.cursor()
        sql = "SELECT status FROM actuator_watering WHERE address = %s ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(sql, str(address))
        result_set = cursor.fetchall()
        if not result_set :
            print("vuoto")
            return None
        else:
            for row in result_set:
                print(row["status"])
                return row["status"]
     

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
        self.tempIn = None
        self.co2In = None
        print(self.humMax)
        print("\n****** Mqtt client Temperature Humidity Co2 starting ******")
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect("127.0.0.1", 1883, 60)
        except Exception as e:
            
           print(str(e))
        self.client.loop_forever()