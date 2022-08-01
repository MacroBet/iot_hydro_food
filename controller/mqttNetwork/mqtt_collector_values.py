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
        self.client.subscribe("actuator_bathFloat")


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

             

#/----------window methods to open and close the windows--------------\

    def closeWindow(self):
        
        for ad in Addresses.adWindows :
            open = self.executeLastState(ad, "window")
            if open is None:
                return
            elif open == "1":
                open = "0"
                success = Post.changeStatusWatering(status, ad)
                if success == 1:
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_window` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(ad), dt, "0"))
                    print("\OPEN = " + open)
                    self.connection.commit()
                    self.communicateToSensors("0", "window")
                else:
                    return
         

    def openWindow(self):

        for ad in Addresses.adWindows:
            open = self.executeLastState(ad,"window")
            if open is not None:
                if open == "0":
                    open = "1"
                    success = Post.changeStatusWatering(open, ad)
                    if success == 1:
                        dt = datetime.now()
                        cursor = self.connection.cursor()
                        sql = "INSERT INTO `actuator_window` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                        cursor.execute(sql, (str(ad), dt, open))
                        print("\OPEN = " + open)
                        self.connection.commit()
                        self.communicateToSensors("1", "window")
                    else:
                        return
                elif open == "1":
                    return

            elif open is None:
                open = "1"
                success = Post.changeStatusWatering(open, ad)
                if success == 1:
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_window` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(ad), dt, open))
                    print("\OPEN = " + open)
                    self.connection.commit()
                    self.communicateToSensors("1", "window")
                else:
                    return

#/---------------------------------------------------------------------------\

#/----------watering methods to open and close the watering valves--------------\
    
    def stopWatering(self):

        for ad in Addresses.adValves :
            status = self.executeLastState(ad, "watering")
            if status is None:
                return
            elif status == "1":
                status = "0"
                success = Post.changeStatusWatering(status, ad)
                if success == 1:
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(ad), dt, "0"))
                    print("\nSTATUS = " + status)
                    self.connection.commit()
                    self.communicateToSensors("0", "inValues")
                else:
                    return
            else:
                return
           

    
    def startWatering(self):

        for ad in Addresses.adValves :
            status = self.executeLastState(ad, "watering")
            if status is not None:
                if status == "0":
                    status = "1"
                    success = Post.changeStatusWatering(status, ad)
                    if success == 1:
                        dt = datetime.now()
                        cursor = self.connection.cursor()
                        sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                        cursor.execute(sql, (str(ad), dt, "1"))
                        print("\nSTATUS = " + status)
                        self.connection.commit()
                        self.communicateToSensors(status, "inValues")
                    else:
                        return
                if status == "2" or status == "1":
                    return
            else:
                status = "1"
                success = Post.changeStatusWatering(status, ad)
                if success == 1:
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(ad), dt, "1"))
                    print("\nSTATUS = " + status)
                    self.connection.commit()
                    self.communicateToSensors(status, "inValues")
                else:
                    return

#/---------------------------------------------------------------------------\

#/----------methods to retrive last state of the actuator--------------\


    def executeLastState(self, address, table) :
        cursor = self.connection.cursor()
        sql = "SELECT status FROM actuator_"+table+ " WHERE address = %s ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(sql, str(address))
        result_set = cursor.fetchall()
        if not result_set :
            return None
        else:
            for row in result_set:
                return row["status"]


#/---------------------------------------------------------------------------\


#/----------methods to notify state changement on the actuator--------------\
   

    def communicateToSensors(self, status, type):
    
        if type == "inValues":

            if status == "1":
                self.client.publish("actuator_data","wat")
                self.client.publish("actuator_bathFloat","wat")
            elif status == "0" :
                self.client.publish("actuator_data","notWat")
                self.client.publish("actuator_bathFloat","notWat")

        elif type == "window":

                if status == "1":
                     self.client.publish("actuator_data","Open")
                elif status == "0":
                     self.client.publish("actuator_data","notOpen")
                    
#/---------------------------------------------------------------------------\


#/----------methods to check if actuator must be enabled--------------\


    def shouldOpenWatering(self, t, h, t_max, h_max, h_min):
        return int(h) < int(h_min) or (int(t) > int(t_max) and int(h) < int(h_max))
    

    def checkActuatorWatering(self, temp, hum, co2):
        if self.shouldOpenWatering(temp, hum, self.tempMax, self.humMax, self.humMin) :
            self.startWatering()
        elif temp < ((self.tempMin + self.tempMax)/2)+3 and hum >= ((self.humMax*60)/100) :
            self.stopWatering()
        elif temp < self.tempMin+2:
             self.stopWatering()



    def checkActuatorWindow(self, tempOut):

        open = 0
        close = 0
     
        if self.co2In is not None and self.tempIn is not None:
            
            if self.tempIn > self.tempMax and tempOut < self.tempIn:
                open = 1
            elif self.tempIn > (self.tempMin + 5) and tempOut < self.tempIn:
                close = 1

            elif self.co2In > (self.co2Max - 100):
                open = 1
            elif self.co2In < (self.co2Min + 100):
                close = 1

            if open == 1 and close == 1 :  
                self.openWindow()
            elif open == 1 and close == 0:
                self.openWindow()
            elif open == 0 and close == 1:
                self.closeWindow()
            else:
                return

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
        print("\n****** Mqtt client Temperature Humidity Co2 starting ******")
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect("127.0.0.1", 1883, 60)
        except Exception as e:
            
           print(str(e))
        self.client.loop_forever()