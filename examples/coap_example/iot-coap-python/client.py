import socket
import sys
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri


def observer(self, response):
    print("callback called")
    if response.payload is None:
        print("response is none")
    if response.payload is not None:
        print("response:")
        print(response.payload)
   

host = "127.0.0.1"
port = 5683

path="/hello"

client = HelperClient(server=(host, port))
client.observe("obs", client.observer)

#response = client.get(path)
#print(response.pretty_print())
client.stop()
