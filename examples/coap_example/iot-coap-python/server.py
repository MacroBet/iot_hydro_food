#!/usr/bin/env python

import getopt
import sys
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

try:
    server.listen(10)
    while(1) :
        if ResExample.checkpresence:
            add = Addresses.constructAddress()
            print(add)
            

except KeyboardInterrupt:
    print("Server Shutdown")
    server.close()
    print("Exiting...")






