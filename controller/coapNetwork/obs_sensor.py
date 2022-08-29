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
        print("debug", data)
        if self.type == 0:
            status = data["status"]
            lane = data["lane"]
            dt = datetime.now()
            self.execute_query(self.address, status, dt, "watering",lane)
            
            print(status)
            
            if str(status) == "1":
                self.mqtt.communicateToSensors(status, "inValues")

            elif str(status) == "0":
                self.mqtt.communicateToSensors(status, "inValues")

            elif str(status) == "2":
                self.mqtt.communicateToSensors(status, "inValues")
        

          
        elif self.type == 1:
            status = data["open"]
            dt = datetime.now()
            self.execute_query(self.address, status, dt, "window", 0)
            if str(status) == "1":
                self.mqtt.communicateToSensors(status, "window")

            elif str(status) == "0":
                self.mqtt.communicateToSensors(status, "window")
        

    def execute_query(self, add, stat, timestamp, table, lane):
        with self.connection.cursor() as cursor:
            cursor = self.connection.cursor()
            if table == "watering":
                sql = "INSERT INTO actuator_" + table + "(`address`, `timestamp`, `status`, `lane`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (str(add), timestamp, stat, lane))
                self.connection.commit()
            else:
                sql = "INSERT INTO actuator_" + table + "(`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (str(add), timestamp, stat))
                self.connection.commit()
        