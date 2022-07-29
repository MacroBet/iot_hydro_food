from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.server.coap import CoAP
from numpy import true_divide

class Post:

    def  changeStatusWatering(status, ad):
        client = HelperClient(ad)
        response = client.post("obs", "mode="+status)
        print(response)
        return response



    def  changeStatusWindows(status, ad):
        client = HelperClient(ad)
        response = client.post("window", "mode="+status)