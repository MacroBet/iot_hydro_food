
from pydoc import cli
import threading
import time
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
import time



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
        "!Change values sensors Temperature\n"\
        "!Change values sensors Humidity\n"\
        "!Change values sensors Co2\n"\
        "activate\n"\
        "log\n"\
        "bath\n"\
        "exit\n\n")

def checkCommand(command, client, client1):
   
    if command == "help":
           showInfo()
    elif command == "log":
        mex = client.message
        mex1 = client1.message
        print(client.message+"\n"+mex1)
        try:
            while True:
                if(mex != client.message):
                    print("\nPress ctrl + C to exit \n")
                    print(mex+"\n"+mex1)
                    mex = client.message
                    mex1 = client1.message
        except KeyboardInterrupt:
         return

    elif command == "bath":
        mex = client.message
        mex1 = client1.message
        print(client.message+"\n"+mex1)
        try:
            while True:
                if(mex != client.message):
                    print("\nPress ctrl + C to exit \n")
                    print(mex+"\n"+mex1)
                    mex = client.message
                    mex1 = client1.message
        except KeyboardInterrupt:
            return
  
    elif command == "activate":
        client.publish("actuator_data","start")
        client.publish("actuator_bathFloat","start")
        client.publish("actuator_outside","start")
        print("Start command sent")

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
            else:
                answer = input(">")
                answer = answer.lower()


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
                
    elif command == "exit":
        thread.join()
        thread1.join()
        thread2.join()
        server.close()
        print("SHUTDOWN")
    else:
        print("Command not found")
        listOfcommands()



def showInfo():

    print("log ---> check message that the sensord send to the application \n"\
          "change value co2 ---> chack only the values of Co2\n"\
          "change value humidity ---> check only the values of humidity\n"\
          "change value temperature ---> check only the values of temperature\n"\
          "bath ---> check level of the bath float\n"\
          "help ---> show the commands that can be promted\n")


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
    print("\nValues for tresholds: \n Max Temperature = {},\n Min Temperature = {},\n Max Humidity = {},\n Min Humidity = {}, \n Max Co2 ={},\n Min Co2 = {}", str(tempMax), str(tempMin),str(humMax), str(humMin),str(co2Max),str(co2Min) )
    print("\nDo you want to continue with this values [y/n]?")
    
    answer = input(">")
    answer = answer.lower()
    if(answer == "yes" or answer == "y"):
        return {"tempMax":tempMax,"tempMin":tempMin,"humMax":humMax,"humMin":humMin,"co2Max":co2Max,"co2Min":co2Min}
    elif(answer == "no" or answer == "n"):
        return start_configuration()

if __name__ == "__main__":
    cfg=  {"tempMax":35,"tempMin":20,"humMax":80,"humMin":35,"co2Max":2000,"co2Min":1000}
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
    
    time.sleep(5)
    
    print("System is running--->\n ")
    try:
        while 1:
            command = input("COMMAND>")
            command = command.lower()
            checkCommand(command, client, client1)
        
    except KeyboardInterrupt:
        thread.join()
        thread1.join()
        thread2.join()
        server.close()
        print("SHUTDOWN")

        

