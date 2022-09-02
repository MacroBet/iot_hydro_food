
import json
from pydoc import cli
import threading
import time
import os
from coapNetwork.addresses import Addresses
from mqttNetwork.mqtt_collector_values import MqttClientData
from mqttNetwork.mqqt_collector_bath_float import MqttClientBathFloat
import paho.mqtt.client as mqtt
import threading
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.messages.request import Request
from coapthon.messages.response import Response
from coapthon.client.helperclient import HelperClient
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapNetwork.resExample import ResExample
import pixel_art as pa
import time
import os




ip = "::"
port = 5683

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port), False)
        self.add_resource("registry", ResExample())

def listOfcommands():
    print("AVAILABLE COMMANDS--->\n")
    print(
        "help \n"\
        "activate\n"\
        "log\n"\
        "bath\n"\
        "sim\n"\
        "change val\n"
        "exit\n\n")



def extractValuesFromClient(client,client1):
    
    level = client1.levIn if client1.levIn  else 50
    humidity = client.humIn if client.humIn else 50
    temperature = client.tempIn if client.tempIn else 30
    co2 = client.co2In if client.co2In else 1400
    tempOut = client.tempOut if client.tempOut else 30

    return [temperature,tempOut,humidity,co2,level]


            

def checkCommand(command, client, client1):
   
    if command == "help":
           showInfo()

    elif command == "log":
        try:
            msg= str(client.message)
            print("\nPress ctrl + C to exit \n")
            while True:
                time.sleep(1)
                if(str(client.message)!= msg):
                    print(str(client.message)+"\n"+str(client1.message)+"\n"+str(client.message1))
                    msg= str(client.message)
        except KeyboardInterrupt:
         return

    elif command == "bath":
        try:
            print("\nPress ctrl + C to exit \n")
            msg= client1.message
            while True:
                time.sleep(1)
                if(client1.message!= msg):
                    print(client1.message)
                    msg= client1.message
        except KeyboardInterrupt:
            return
  
    elif command == "activate":
        client.communicateToSensors("start","inValues")
    
    elif command == "sim":
        
        try:
            data = extractValuesFromClient(client,client1)
            while True:
                ad = Addresses.adValves[0]
                ad1 = Addresses.adWindows[0]
               
                statWat = client.executeLastState(ad, "watering", "status") if ad  else "0"
                statWind = client.executeLastState(ad1, "window", "status") if ad1 else "0"


                data = extractValuesFromClient(client,client1)
        
                os.system('cls' if os.name == 'nt' else 'clear')
                print(pa.greenhouse[statWat][statWind].format(data[0],data[1],data[2],data[3],data[4]))
                print("\nPress ctrl + C to exit \n")

                        
              
                time.sleep(0.5)


        except KeyboardInterrupt:
            return

    elif command == "change val":

        cfg = start_configuration()
        client.tempMax = cfg["tempMax"]   
        client.tempMin = cfg["tempMin"]
        client.humMax = cfg["humMax"]
        client.humMin = cfg["humMin"]
        client.co2Max = cfg["co2Max"]
        client.co2Min = cfg["co2Min"]

    elif command == "exit":
        # thread.join()
        # thread1.join()
        # server.close()
        # thread2.join()
        print("SHUTDOWN")
        os._exit(0)
    else:
        print("Command not found")
        listOfcommands()



def showInfo():

    print("log ---> to check message that the sensord send to the application \n"\
          "change val ---> to change the current values of the tresholds\n"\
          "bath ---> to check level of the bath float\n"\
          "sim ---> to show simulation of the greenhouse\n"\
          "activate ---> to activate all the sensors in the network\n"
          "help ---> to show the commands that can be promted\n")



def validate(field,defaultValue):
    if(field.isnumeric()):
        return int(field)
    return defaultValue



def start_configuration():

    print("Define tresholds for the parameters Temperature, Humidity, Co2 :\n")
    tempMax = validate(input("TRESHOLD MAX TEMPERATURE  (default value 35C) : "),35)
    tempMin = validate(input("TRESHOLD MIN TEMPERATURE  (default value 20C) : "),20)
    humMax = validate(input("TRESHOLD MAX HUMIDITY %  (defalut value 80%) : "),80)
    humMin = validate(input("TRESHOLD MIN HUMIDITY %  (default value 30%) : "),35)
    co2Max = validate(input("TRESHOLD MAX CO2  (default value 2000ppm) : "),2000)
    co2Min = validate(input("TRESHOLD MIN CO2  (default value 1000ppm) : "),1000)
    
    print("You choose these values:\n")
    print("\nValues for tresholds: \n Max Temperature = {},\n Min Temperature = {},\n Max Humidity = {},\n Min Humidity = {}, \n Max Co2 ={},\n Min Co2 = {}".format( str(tempMax), str(tempMin),str(humMax), str(humMin),str(co2Max),str(co2Min) ))
    print("\nDo you want to continue with this values [y/n]?")
    
    answer = input(">")
    answer = answer.lower()
    if(answer == "yes" or answer == "y"):
        return {"tempMax":tempMax,"tempMin":tempMin,"humMax":humMax,"humMin":humMin,"co2Max":co2Max,"co2Min":co2Min}
    elif(answer == "no" or answer == "n"):
        return start_configuration()









if __name__ == "__main__":
    cfg=  {"tempMax":35,"tempMin":20,"humMax":80,"humMin":35,"co2Max":1800,"co2Min":1200}
    should_configure = input("Welcome to Idrofood simulator 🚀 \nDo you want to configure parameters? (y/n)").lower()
    if(should_configure == "yes" or should_configure == "y"):
        cfg = start_configuration()

    print("\nWelcome\n")
    listOfcommands()

    print("System is going to start----->\n")
    time.sleep(5)
    
    client = MqttClientData()
    thread = threading.Thread(target=client.mqtt_client, args=(cfg["tempMax"], cfg["tempMin"], cfg["humMax"], cfg["humMin"], cfg["co2Max"], cfg["co2Min"],"check"), kwargs={})
    thread.start()
    client1 = MqttClientBathFloat()
    thread1 = threading.Thread(target=client1.mqtt_client, args=(), kwargs={})
    thread1.start()

    server = CoAPServer(ip, port)
    thread2 = threading.Thread(target=server.listen, args=(), kwargs={})
    thread2.start()
    
    time.sleep(20)
    start = 0

    try:
        while 1:
            if ResExample.valves == 1 and ResExample.windows == 1:

                   
                    if start == 0:
                        print("\n🖥  🖥  System is running  🖥  🖥\n\n ")
                        print("Use command 'activate' to start sensor node\n\n ")
                        start = 1
                    command = input("COMMAND>")
                    command = command.lower()
                    
                    checkCommand(command, client, client1)
            else:
 
                print("\n⌛️ ⌛️ ⌛️ Controller is wating for all the sensors ⌛️ ⌛️ ⌛️\n ")
                time.sleep(5)

        
    except KeyboardInterrupt:
        # thread.join()
        # thread1.join()
        # server.close()
        # thread2.join()
        print("SHUTDOWN")
        os._exit(0)




