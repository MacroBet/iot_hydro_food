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

    def __init__(self, name="ResExample"):
        super(ResExample, self).__init__(name)
        self.payload = "Advanced resource"


    def render_GET(self, request):
        print("\nCOMMAND>")
        if request.payload == "valves":
            Addresses.insertNewAddress(request.source, "valves")
            ResExample.valves = 1
            ob =ObserveSensor(request.source, "obs", 0)
        elif request.payload == "window":
            Addresses.insertNewAddress(request.source, "windows")
            ResExample.windows = 1
            ob =ObserveSensor(request.source, "window", 1)
        return self

    def checkpresenceValves():
        return ResExample.valves

    def checkpresenceWindows():
        return ResExample.windows


    