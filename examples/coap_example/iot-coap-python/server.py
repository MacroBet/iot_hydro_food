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

address = None
class ResExample(Resource):

    def __init__(self, name="Resources"):
        super(ResExample, self).__init__(name)

        self.payload = "Basic Resource"

    def render_GET(self, request):
        if request.payload is None:
            print("empty payload")
            ob = ObserveSensor(request.source)
            return self
        else :
            ob = ObserveSensor(request.source)
            return self

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port), False)
        self.add_resource("registry", ResExample())
      


ip = "::"
port = 5683


server = CoAPServer(ip, port)

try:
    server.listen(1)
except KeyboardInterrupt:
    print("Server Shutdown")
    server.close()
    print("Exiting...")



