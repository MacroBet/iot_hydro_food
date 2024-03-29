import json
from datetime import datetime
from time import time
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from mqttNetwork.mqqt_collector_bath_float import MqttClientBathFloat
from mqttNetwork.mqtt_collector_values import MqttClientData
from database.dataBase import Database
from globalStatus import globalStatus

class ObserveSensor:

    def __init__(self,source_address, resource, type):
        self.db = Database()
        self.connection = self.db.connect_db()
        self.address = source_address
        self.resource = resource
        self.type = type
        self.mqtt = None
        self.start_observing()
       

    def start_observing(self):
        self.client = HelperClient(self.address)
        self.mqtt = MqttClientData()
        self.mqtt.mqtt_client(None, None, None, None, None, None, "communicate")
        self.client.observe(self.resource, self.observer)
    
    def observer(self, response):
        data = json.loads(response.payload)
        
        if self.type == 0:
            status = data["status"]
            dt = datetime.now()
            self.execute_query(self.address, status, dt, "watering")
            
            if str(status) == "1":
                if globalStatus.chageVal == 0: print("\n💦💦💦💦 START WATERING 💦💦💦💦\n")
                globalStatus.setStatusValve(1)
                self.mqtt.communicateToSensors(status, "inValues")

            elif str(status) == "0":
                if globalStatus.chageVal == 0: print("\n🚫🚫🚫🚫 VALVES DEFAULT STATE 🚫🚫🚫🚫\n")
                globalStatus.setStatusValve(0)
                self.mqtt.communicateToSensors(status, "inValues")

            elif str(status) == "2":
                if globalStatus.chageVal == 0: print("\n🛁🛁🛁🛁 OPEN CHARGE TANK 🛁🛁🛁🛁\n")
                globalStatus.setStatusValve(2)
                self.mqtt.communicateToSensors(status, "inValues")
        

          
        elif self.type == 1:
            status = data["open"]
            dt = datetime.now()
            self.execute_query(self.address, status, dt, "window")
            if str(status) == "1":
                if globalStatus.chageVal == 0: print("\n💨💨💨💨 OPENING WINDOW 💨💨💨💨\n")
                globalStatus.setStatusWindow(1)
                self.mqtt.communicateToSensors(status, "window")

            elif str(status) == "0":
                if globalStatus.chageVal == 0: print("\n🚫🚫🚫🚫 WINDOWS DEFAULT STATE 🚫🚫🚫🚫\n")
                globalStatus.setStatusWindow(0)
                self.mqtt.communicateToSensors(status, "window")
        

    def execute_query(self, add, stat, timestamp, table):
        
        with self.connection.cursor() as cursor:
            cursor = self.connection.cursor()
            sql = "INSERT INTO actuator_" + table + "(`address`, `timestamp`, `status`, `manual`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (str(add), timestamp, stat, "1"))
            self.connection.commit()
           