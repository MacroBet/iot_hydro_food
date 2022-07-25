import datetime
import json
import socket
import sys
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from dataBase import Database

class ObserveSensor:


    def __init__(self,source_address):
        #self.db = Database()
        #self.connection = self.db.connect_db()
        self.address = source_address
        self.resource = "obs"
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
            return
        data = json.loads(response.payload)
        status = data["status"]
        dt = datetime.now()
        self.execute_query(self.address, status, dt)
        print(status)

    def execute_query(self, add, stat, timestamp):
        with self.connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `coap` (`add`, `status`, `timestamp`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (self.aqi, self.ts))
        
        self.connection.commit()


        