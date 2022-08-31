from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.server.coap import CoAP


class Post:

    clients = {} # ad[0] => client
    def getClient(ad):
        address= ad[0]
        print("ad",ad)
        if(address not in Post.clients):
            newClient = HelperClient(ad)
            Post.clients[address]= newClient
        client = Post.clients[address]
        return client

    def changeStatusWatering(status, ad):
        response = Post.getClient(ad).post("obs", "mode="+status)
        print(response.code)
        if response.code == 67:
            return 1
        else:
            return 0

    def  changeStatusWindows(status, ad):
        response = Post.getClient(ad).post("window", "mode="+status)
        print(response.code)
        if response.code == 67:
            return 1
        else:
            return 0


