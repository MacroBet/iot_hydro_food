import json
from datetime import datetime
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from database.dataBase import Database

class ObserveSensor:


    def __init__(self,source_address, resource, type):
        self.db = Database()
        self.connection = self.db.connect_db()
        self.address = source_address
        self.resource = resource
        self.type = type
        self.start_observing()

    def start_observing(self):
        
        self.client = HelperClient(self.address)
        self.client.observe(self.resource, self.observer)
    
    def observer(self, response):
        print("callback called")
        if response.payload is None:
            print("response is none")
        if response.payload is not None:
            print("response:")
            print(response.payload)
        data = json.loads(response.payload)
        if self.type == 0:
            status = data["status"]
            dt = datetime.now()
            self.execute_query(self.address, status, dt, "watering")
            print(status)
        elif self.type == 1:
            status = data["open"]
            dt = datetime.now()
            self.execute_query(self.address, status, dt, "window")
            print(status)

    def execute_query(self, add, stat, timestamp, table):
        with self.connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `actuator_`" + table + "(`address`, `timestamp`, `status`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (str(add), timestamp, stat))
        
        self.connection.commit()


        