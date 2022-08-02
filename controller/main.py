
from pydoc import cli
import threading
import time
from mqttNetwork.mqtt_collector_values import MqttClientData
from mqttNetwork.mqqt_collector_bath_float import MqttClientBathFloat
import paho.mqtt.client as mqtt
import getopt
import sys
import threading
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapNetwork.addresses import Addresses
from coapNetwork.resExample import ResExample
import time



ip = "::"
port = 5683

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port), False)
        self.add_resource("registry", ResExample())

def listOfcommands():

    print("AVAILABLE COMMANDS--->\n")

    print("!Change values sensors Temperature\n"\
          "!Change values sensors Humidity\n"\
          "!Change values sensors Co2\n"\
          "!Check sensors log\n"\
          "!List of commands\n"\
          "!Check bath float level\n"  
          "!Start watering\n"
          "!Stop watering\n"
          "!Open windows\n"
          "!Close windows\n"
          "!Charge the tanks\n"
          "!Info commands\n\n")

def checkCommand(command, client, client1):
   
    if command == "!info commands":
           showInfo()
    elif command == "!check sensors log":
        mex = client.message
        print(client.message)
        try:
            while True:
                if(mex != client.message):
                    print("\nPress ctrl + C to exit \n")
                    print(client.message)
                    mex = client.message
        except KeyboardInterrupt:
         return

    elif command == "!check bath float level":
        level = client1.message
        print(client1.message)
        try:
            while True:
                if(level != client1.message):
                    print("\nPress ctrl + C to exit \n")
                    print(client1.message)
                    level = client1.message
        except KeyboardInterrupt:
         return        
  
    elif command == "!change value co2":

        while 1:
            client.co2Max = input("Insert new Max value for co2: ")
            client.co2Min = input("Insert new Min value for co2: ")
            print("New max/min value for co2 are : "+ client.co2Max +", " + client.co2Min)
            print("Do you want continue with this value[y/n]?")
            answer = input(">")
            answer = answer.lower()
            if(answer == "yes" or answer == "y"):
                print("Value saved\n")
                break
            elif(answer == "no" or answer == "n"):
                print("Insert new value\n")
                continue

    elif command == "!change value humidity":
          
           while 1:
            client.co2Max = input("Insert new Max value for humidity: ")
            client.co2Min = input("Insert new Min value for humidity: ")
            print("New max/min value for co2 are : "+ client.humMax +", " + client.humMin)
            print("Do you want continue with this value[y/n]?")
            answer = input(">")
            answer = answer.lower()
            if(answer == "yes" or answer == "y"):
                print("Value saved\n")
                break
            elif(answer == "no" or answer == "n"):
                print("Insert new value\n")
                continue

    elif command == "!change value temperature":
            
            while 1:
                client.co2Max = input("Insert new Max value for temperature: ")
                client.co2Min = input("Insert new Min value for temprature: ")
                print("New max/min value for co2 are : "+ client.tempMax +", " + client.tempMin)
                print("Do you want continue with this value[y/n]?")
                answer = input(">")
                answer = answer.lower()
                if(answer == "yes" or answer == "y"):
                    print("Value saved\n")
                    break
                elif(answer == "no" or answer == "n"):
                    print("Insert new value\n")
                    continue

    elif command == "!list of commands":
            listOfcommands()
    elif command == "!start watering":
        client.startWatering()
    elif command == "!stop watering":
        client.stopWatering()
    elif command == "!open window":
        client.openWindow()
    elif command == "!close window":
        client.closeWindow()
    else:
        print("Command not found")
        listOfcommands()



def showInfo():

    print("check sensors log ---> check message that the sensord send to the application \n"\
          "change value co2 ---> chack only the values of Co2\n"\
          "change value humidity ---> check only the values of humidity\n"\
          "change value temperature ---> check only the values of temperature\n"\
          "check bath float level ---> check level of the bath float\n"\
          "list of commands ---> show the commands that can be promted\n")



if __name__ == "__main__":

    while 1:
        print("Define tresholds for the parameters Temperature, Humidity, Co2 :\n")
        tempMax = input("TRESHOLD MAX TEMPERATURE  (default value 35C) : ")
        if tempMax == "":
            tempMax =  35 
        tempMin = input("TRESHOLD MIN TEMPERATURE  (default value 20C) : ")
        if tempMin == "":
            tempMin = 20 
        humMax = input("TRESHOLD MAX HUMIDITY %  (defalut value 80%) : ")
        if humMax == "":
            humMax = 80 
        humMin = input("TRESHOLD MIN HUMIDITY %  (default value 30%) : ")
        if humMin == "":
            humMin = 35 
        co2Max = input("TRESHOLD MAX CO2  (default value 2000ppm) : ")
        if co2Max == "": 
            co2Max = 2000
        co2Min = input("TRESHOLD MIN CO2  (default value 1000ppm) : ")
        if co2Min == "":
            co2Min = 1000
        
        print("You choose these values:\n")
        print("\nValues for tresholds: \n Max Temperature = " + str(tempMax) + ",\n Min Temperature = " \
            + str(tempMin) + " ,\n Max Humidity = " + str(humMax) + ",\n Min Humidity = " + str(humMin) +",\
                    \n Max Co2 = "+ str(co2Max) +", \n Min Co2 = "+ str(co2Min)\
                    +"\n\nDo you want to continue with this values [y/n]?")
        
        answer = input(">")
        answer = answer.lower()
        if(answer == "yes" or answer == "y"):
            print("\nWelcome\n")
            break
        elif(answer == "no" or answer == "n"):
            print("Insert new value\n")
            continue

    listOfcommands()

    print("System is going to start----->\n")
    time.sleep(5)
    
    client = MqttClientData()
    thread = threading.Thread(target=client.mqtt_client, args=(tempMax, tempMin, humMax, humMin, co2Max, co2Min,), kwargs={})
    thread.start()
    client1 = MqttClientBathFloat()
    thread1 = threading.Thread(target=client1.mqtt_client, args=(), kwargs={})
    thread1.start()

    server = CoAPServer(ip, port)
    thread = threading.Thread(target=server.listen, args=(), kwargs={})
    thread.start()
    
    time.sleep(5)
    
    print("System is running--->\n ")
    while 1:
        command = input("COMMAND>")
        command = command.lower()
        checkCommand(command, client, client1)
        

