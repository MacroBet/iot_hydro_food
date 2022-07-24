#!/usr/bin/env python

import getopt
import sys
from coapthon.server.coap import CoAP
from obs_sensor import ObserveSensor
from coapthon.resources.resource import Resource

class ResExample(Resource):

    def __init__(self, name="ResExample", coap_server=None):
        super(ResExample, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)

        self.payload = "Basic Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

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
        self.client.post(self.resource, "0")


ip = "::"
port = 5683


server = CoAPServer(ip, port)

try:
    server.listen(100)
except KeyboardInterrupt:
    print("Server Shutdown")
    server.close()
    print("Exiting...")



