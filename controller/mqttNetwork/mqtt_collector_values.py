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
        self.client.subscribe("status_data") # temp in
        self.client.subscribe("status_outside") # temp out 
        self.client.subscribe("actuator_outside") # notify window opening to external temp sensor
        self.client.subscribe("actuator_data") # notify window opening to internal temp sensor
        self.client.subscribe("actuator_bathFloat") # bathfloat


    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
      
        if msg.topic == "status_data" :
            self.message = msg.payload
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
            self.message = msg.payload
            data = json.loads(msg.payload)
            node_id = data["node"]
            tempOut = data["tempOut"]
            self.checkActuatorWindow(tempOut)
   
             

#/----------window methods to open and close the windows--------------\

    def closeWindow(self):
        
        for ad in Addresses.adWindows :
            open = self.executeLastState(ad, "window", "status", "status")
            manual = self.executeLastState(ad, "window", "manual")
            if manual=='1' and open != '0':
                return
            if open == "1":
                open = "0"
                success = Post.changeStatusWindows(open, ad)
                if success == 1:
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_window` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(ad), dt, "0"))
                    print("\OPEN = " + open)
                    self.connection.commit()
                    self.communicateToSensors("0", "window")
               
         

    def openWindow(self):

        for ad in Addresses.adWindows:
            open = self.executeLastState(ad,"window", "status")
            manual = self.executeLastState(ad, "window", "manual")
            if manual=='1' and open != '0':
                return
            if open is not None:
                if open == "0":
                    open = "1"
                    success = Post.changeStatusWindows(open, ad)
                    if success == 1:
                        dt = datetime.now()
                        cursor = self.connection.cursor()
                        sql = "INSERT INTO `actuator_window` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                        cursor.execute(sql, (str(ad), dt, open))
                        print("**********************\nOPENING WINDOW\n**********************\n")
                        print("\OPEN = " + open)
                        self.connection.commit()
                        self.communicateToSensors("1", "window")
                    
            elif open is None:
                open = "1"
                success = Post.changeStatusWindows(open, ad)
                if success == 1:
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_window` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(ad), dt, open))
                    print("**********************\nOPENING WINDOW\n**********************\n")
                    print("\OPEN = " + open)
                    self.connection.commit()
                    self.communicateToSensors("1", "window")
              

#/---------------------------------------------------------------------------\

#/----------watering methods to open and close the watering valves--------------\
    
    def stopWatering(self):
        for ad in Addresses.adValves :
            status = self.executeLastState(ad, "watering", "status")
            manual = self.executeLastState(ad, "watering", "manual")
            if manual=='1' and status != '0':
                return
            if status == "1":
                status = "0"
                success = Post.changeStatusWatering(status, ad)
                if success == 1:
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(ad), dt, "0"))
                    print("**********************\nSTOP WATERING\n**********************\n")
                    print("\nSTATUS = " + status)
                    self.connection.commit()
                    self.communicateToSensors("0", "inValues")
    
    def startWatering(self):

        for ad in Addresses.adValves :
            manual = self.executeLastState(ad, "watering", "manual")
            status = self.executeLastState(ad, "watering", "status")
            if manual=='1' and status != '0':
                return
            if status is  None:
                status = "1"
                success = Post.changeStatusWatering(status, ad)
                if success == 1:
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(ad), dt, "1"))
                    print("**********************\nSTART WATERING\n**********************\n")
                    print("\nSTATUS = " + status)
                    self.connection.commit()
                    self.communicateToSensors(status, "inValues")
            if status == "0":
                status = "1"
                success = Post.changeStatusWatering(status, ad)
                if success == 1:
                    dt = datetime.now()
                    cursor = self.connection.cursor()
                    sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(ad), dt, "1"))
                    print("**********************\nSTART WATERING\n**********************\n")
                    print("\nSTATUS = " + status)
                    self.connection.commit()
                    self.communicateToSensors(status, "inValues")


#/---------------------------------------------------------------------------\

#/----------methods to retrive last state of the actuator--------------\


    def executeLastState(self, address, table, column) :
        cursor = self.connection.cursor()
        sql = "SELECT * FROM actuator_"+table+ " WHERE address = %s ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(sql, str(address))
        result_set = cursor.fetchall()
        if not result_set :
            return None
        else:
            for row in result_set:
                return row[column]


#/---------------------------------------------------------------------------\


#/----------methods to notify state changement on the actuator--------------\
   

    def communicateToSensors(self, status, type):

        if type == "inValues":

            if str(status) == "1":
                self.client.publish("actuator_data","wat")
                self.client.publish("actuator_bathFloat","wat")
            elif str(status) == "0" :
                self.client.publish("actuator_data","notWat")
                self.client.publish("actuator_bathFloat","stop")
            elif str(status) == "2" :
                self.client.publish("actuator_data","notWat")
                self.client.publish("actuator_bathFloat","charge")
            elif str(status) == "start":
                self.client.publish("actuator_data","start")
                self.client.publish("actuator_bathFloat","start")
                self.client.publish("actuator_outside","start")
                print("Start command sent")

        elif type == "window":

            if str(status) == "1":
                    self.client.publish("actuator_data","Open")
            elif str(status) == "0":
                    self.client.publish("actuator_data","notOpen")
           

                    
#/---------------------------------------------------------------------------\


#/----------methods to check if actuator must be enabled--------------\

    def shouldOpenWatering(self, t, h, t_max, h_max, h_min):
        if(t>t_max and h<h_max): return True  
        if(h<h_min): return True 
        return False

    def checkActuatorWatering(self, temp, hum, co2):
        
        if self.shouldOpenWatering(int(temp), int(hum), self.tempMax, self.humMax, self.humMin) :
            self.startWatering()
        else:
            self.stopWatering()


    def checkActuatorWindow(self, tempOut):
        open = 0
        close = 0
        if self.co2In is None or self.tempIn is  None: return
            
        if self.tempIn > self.tempMax and tempOut < self.tempIn:
            open = 1
        elif self.tempIn > (self.tempMin + 5) and tempOut < self.tempIn:
            close = 1

        if self.co2In > (self.co2Max - 100):
            open = 1
        elif self.co2In < (self.co2Min + 100):
            close = 1

        if open == 1 :  
            self.openWindow()

        elif close == 1:
            self.closeWindow()


#/---------------------------------------------------------------------------\

    client = None

    def mqtt_client(self, tempMax, tempMin, humMax, humMin, co2Max, co2Min, type):
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
        self.type = type
        if type == "check":
            print("\n****** Mqtt client Temperature Humidity Co2 starting ******")
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        if type == "check":
            self.client.on_message = self.on_message
        try:
            self.client.connect("127.0.0.1", 1883, 60)
        except Exception as e:
            
            print(str(e))
        if type == "check":
            self.client.loop_forever()