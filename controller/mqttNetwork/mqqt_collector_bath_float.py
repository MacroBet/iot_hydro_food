from time import sleep
import paho.mqtt.client as mqtt
from datetime import datetime
from database.dataBase import Database
import json
from pydoc import cli
from coapNetwork.addresses import Addresses
from coapNetwork.sendpost import Post


class MqttClientBathFloat:

    def on_connect(self, client, userdata, flags, rc):
        print("****** Connected with result code "+str(rc) + " ******\n")
        self.client.subscribe("status_bathFloat")
        self.client.subscribe("actuator_bathFloat")

    def update_watering_status(self, ad, status):
        dt = datetime.now()
        cursor = self.connection.cursor()
        sql = "INSERT INTO `actuator_watering` (`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (str(ad), dt, status))
        print("\nSTATUS = " + status)
        self.connection.commit()

    def update_bath_float_level(self, node_id, level):
        dt = datetime.now()
        cursor = self.connection.cursor()
        sql = "INSERT INTO `bath_float` (`node_id`, `timestamp`, `level`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (node_id, dt, level))
        self.connection.commit()


    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        if msg.topic == "status_bathFloat":
            self.message = str(msg.payload)
            data = json.loads(msg.payload)
            node_id = data["node"]
            level = data["level"]
            self.update_bath_float_level(node_id,level)
            self.checkActuatorLevel(level)
        else:
            return

#/----------methods to open/close the charge valve--------------\
    
    def closeCharge(self):
        for ad in Addresses.adValves :
            status = self.executeLastState(ad, "watering", "status")
            if status == "2":
                status = "0"
                sleep(2)
                success = Post.changeStatusWatering(status, ad)
                if success == 1:
                    self.update_watering_status(str(ad),"0")
                    print("**********************\nCLOSE CHARGE TANK\n**********************\n")
                    print("\nSTATUS = " + status)
                    self.connection.commit()
                    self.communicateToSensors("0")
            else:
                return


    def openCharge(self):
        for ad in Addresses.adValves :
            status = self.executeLastState(ad, "watering", "status")
            
            if status == "0":
                status = "2"
                success = Post.changeStatusWatering(status, ad)
                if success == 1:
                    self.update_watering_status(ad, status)
                    print("**********************\nOPEN CHARGE TANK\n**********************\n")
                    self.communicateToSensors("2")

            if status is None:
                status = "2"
                success = Post.changeStatusWatering(status, ad)
                if success == 1:
                    self.update_watering_status(ad, status)
                    print("**********************\nOPEN CHARGE TANK\n**********************\n")
                    self.communicateToSensors("2")

#/---------------------------------------------------------------------------\

#/----------methods to retrive last state and address of the actuator--------------\


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

#/----------methods to check level of the bath float--------------\

      
    def checkActuatorLevel(self, level):
        if level < 20:
            self.openCharge()
        elif level > 80:
            self.closeCharge()
        else:
            return 

#/---------------------------------------------------------------------------\

#/----------methods to notify state changement on the actuator--------------\
   

    def communicateToSensors(self,status):

        if status == "2":
            self.client.publish("actuator_bathFloat","charge")
        elif status == "0" :
                self.client.publish("actuator_bathFloat","stop")

                    
#/---------------------------------------------------------------------------\

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