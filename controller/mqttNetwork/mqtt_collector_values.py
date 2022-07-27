from ast import Return
from email import message
import paho.mqtt.client as mqtt
from datetime import datetime
from database.dataBase import Database
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
            #self.checkActuatorWatering(temperature, humidity, co2)
           
        elif msg.topic == "status_outside" :
            self.message = str(msg.payload)
            data = json.loads(msg.payload)
            node_id = data["node"]
            tempOut = data["tempOut"]
            print(tempOut)
            #self.checkActuatorWindow(tempOut)

             

#/----------window methods to open and close the windows--------------\

    def closeWindow(self):
        
        for ad in Addresses.adWindows :
            print(ad)
            open = self.executeLastState(ad, "window")
            if open is None:
                return
            elif open == "1":
                open = "0"
                Post.changeStatusWindows(open, ad)
                dt = datetime.now()
                cursor = self.connection.cursor()
                sql = "INSERT INTO `actuator_window` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (str(ad), dt, "0"))
                print("\OPEN = " + open)
                self.connection.commit()
                self.communicateToSensors("0")
         

    def openWindow(self):

        for ad in Addresses.adWindows:
            print(ad)
            open = self.executeLastState(ad,"window")
            if open is not None:
                if open == "0":
                    open = "1"
                    Post.changeStatusWindows(open, ad)
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_window` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(ad), dt, open))
                    print("\OPEN = " + open)
                    self.connection.commit()
                    self.communicateToSensors("1", "window")
                elif open == 1:
                    return

            elif open is None:
                open = "1"
                Post.changeStatusWindows(open, ad)
                dt = datetime.now()
                cursor = self.connection.cursor()
                sql = "INSERT INTO `actuator_window` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (str(ad), dt, open))
                print("\OPEN = " + open)
                self.connection.commit()
                self.communicateToSensors("1", "window")

#/---------------------------------------------------------------------------\

#/----------watering methods to open and close the watering valves--------------\
    
    def stopWatering(self):

        for ad in Addresses.adValves :
            print(ad)
            status = self.executeLastState(ad, "watering")
            if status is None:
                return
            elif status == "1":
                status = "0"
                Post.changeStatusWatering(status, ad)
                dt = datetime.now()
                cursor = self.connection.cursor()
                sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (str(ad), dt, "0"))
                print("\nSTATUS = " + status)
                self.connection.commit()
                self.communicateToSensors("0", "inValues")
            else:
                return
           

    
    def startWatering(self):

        for ad in Addresses.adValves :
            print(ad)
            status = self.executeLastState(ad, "watering")
            if status is not None:
                if status == "0":
                    status = "1"
                    Post.changeStatusWatering(status, ad)
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(ad), dt, "1"))
                    print("\nSTATUS = " + status)
                    self.connection.commit()
                    self.communicateToSensors(status, "inValues")
                if status == "2" or status == "1":
                    return
            else:
                status = "1"
                Post.changeStatusWatering(status, ad)
                dt = datetime.now()
                cursor = self.connection.cursor()
                sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (str(ad), dt, "1"))
                print("\nSTATUS = " + status)
                self.connection.commit()
                self.communicateToSensors(status, "inValues")

#/---------------------------------------------------------------------------\

#/----------methods to retrive last state of the actuator--------------\


    def executeLastState(self, address, table) :
        cursor = self.connection.cursor()
        sql = "SELECT status FROM actuator_{}".format(table) + "WHERE address = %s ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(sql, str(address))
        result_set = cursor.fetchall()
        if not result_set :
            print("vuoto")
            return None
        else:
            for row in result_set:
                print(row["status"])
                return row["status"]


#/---------------------------------------------------------------------------\


#/----------methods to notify state changement on the actuator--------------\
   

    def communicateToSensors(self, status, type):
    
        if type == "inValues":

            if status == "1":
                self.client.publish("actuator_data","wat")
            elif status == "0" :
                self.client.publish("actuator_data","notWat")

        elif type == "window":

                if status == "1":
                     self.client.publish("actuator_data","Open")
                elif status == "0":
                     self.client.publish("actuator_data","notOpen")
                    
#/---------------------------------------------------------------------------\


#/----------methods to check if actuator must be enabled--------------\


    def shouldOpenWatering(self, t, h, t_max, h_max, h_min):
        return h < (h_min) or (t > (t_max) and h < (h_max))
    

    def checkActuatorWatering(self, temp, hum, co2):
        if self.shouldOpenWatering(temp, hum, self.tempMax, self.humMax, self.humMin) :
            self.startWatering()
        elif temp < (self.tempMin + 2) and hum >= ((self.humMax*70)/100) :
            self.stopWatering()



    def checkActuatorWindow(self, tempOut):

        if self.co2In is not None and self.tempIn is not None:
            
            delta_inTemp = abs(self.tempIn - self.tempMax) + abs(self.tempIn - self.tempMin)

            delta_outTemp = abs(tempOut - self.tempMax) + abs(tempOut - self.tempIn)

            if self.co2In < self.co2Max-200 and delta_inTemp > delta_outTemp:
                
                self.openWindow()

            elif self.co2In < (self.co2Max+self.co2Min)/2 and delta_inTemp < delta_outTemp:

                self.closeWindow()

#/---------------------------------------------------------------------------\



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