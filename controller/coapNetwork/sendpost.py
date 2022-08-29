from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.server.coap import CoAP


class Post:

    def  changeStatusWatering(status, ad):
        client = HelperClient(ad)
        response = client.post("obs", "mode="+status)
        print(response.code)
        if response.code == 67:
            return 1
        else:
            return 0



    def  changeStatusWindows(status, ad):
        client = HelperClient(ad)
        response = client.post("window", "mode="+status)
        print(response.code)
        if response.code == 67:
            return 1
        else:
            return 0


