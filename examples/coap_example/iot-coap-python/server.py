#!/usr/bin/env python

import getopt
import sys
import threading
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.server.coap import CoAP
from obs_sensor import ObserveSensor
from coapthon.resources.resource import Resource
from addresses import Addresses
from resExample import ResExample



class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port), False)
        self.add_resource("registry", ResExample())


ip = "::"
port = 5683

server = CoAPServer(ip, port)
print("ciao")
thread = threading.Thread(target=server.listen, args=(), kwargs={})
thread.start()
print("ciao")    
while(1) :
    if ResExample.checkpresence == 1:
        add = Addresses.constructAddress()
        print(add)
    else :
        print("vuoto")
        if add is not None :
            for address in add :
                print(address)
                client = HelperClient(address)
                path="status"
                response = client.post("obs", "mode=0")
    
    
        





