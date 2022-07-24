import json
import socket
import sys
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri


class ObserveSensor:


    def __init__(self,source_address):
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
        data = json.loads(response.payload)
        status = data["status"]
        #last_status = getLastStatus()
        print(status)
        self.client.post(self.resource, str(status))

        