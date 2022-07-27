from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.server.coap import CoAP

class Post:

    def  changeStatusWatering(status, ad):
        client = HelperClient(ad)
        path="status"
        response = client.post("obs", "mode="+status)



    def  changeStatusWindows(status, ad):
        client = HelperClient(ad)
        path="window"
        response = client.post("window", "mode="+status)