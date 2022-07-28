import getopt
import imp
import json
import sys
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.server.coap import CoAP
from coapNetwork.obs_sensor import ObserveSensor
from coapthon.resources.resource import Resource
from coapNetwork.addresses import Addresses


class ResExample(Resource):
    
    valves = 0
    windows = 0

    def __init__(self, name="ResExample", coap_server=None):
        super(ResExample, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)

        self.payload = "Basic Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        if request.payload == "valves":
            Addresses.insertNewAddress(request.source, "valves")
            ResExample.valves = 1
        #ob =ObserveSensor(request.source)
        elif request.payload == "window":
            Addresses.insertNewAddress(request.source, "windows")
            ResExample.windows = 1
        return self

    def checkpresenceValves():
        return ResExample.valves

    def checkpresenceWindows():
        return ResExample.windows


    