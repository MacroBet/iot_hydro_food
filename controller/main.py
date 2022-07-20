
import threading
import time
from mqttNetwork.mqtt_collector import MqttClient
import paho.mqtt.client as mqtt

def listOfcommands():

    print("AVAILABLE COMMANDS--->\n")
    print("!Check values sensors Temperature\n"\
          "!Check values sensors Humidity\n"\
          "!Check values sensors Co2\n"\
          "!Change values of thresholds\n"
          "!Check log of sensors\n"\
          "!List of commands\n"\
          "!Info commands\n\n")

def checkCommand(command, client):
   
    if command == "!info commands":
           showInfo()
    elif command == "!check log of sensors":
            print(client.message)
    elif command == "!change values of thresholds":
           print("......")
    elif command == "!check values sensors co2":
            print("......")
    elif command == "!check values sensors humidity":
           print("......")
    elif command == "!check values sensors temperature":
            print("......")
    elif command == "!list of commands":
            listOfcommands()
    else:
        print("Command not found")
        listOfcommands()

def showInfo():

    print("check log of sensors ---> check message that the sensord send to the application \n"\
          "change values of threshold ---> change value of temperature humidity and Co2 that has been setted at the start\n"\
          "check values sensors co2 ---> chack only the values of Co2\n"\
          "check values sensors humidity ---> check only the values of humidity\n"\
          "check values sensors temperature ---> check only the values of temperature\n"\
          "list of commands ---> show the commands that can be promted\n")



if __name__ == "__main__":

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
        humMin = 350 
    co2Max = input("TRESHOLD MAX CO2  (default value 2000ppm) : ")
    if co2Max == "": 
        co2Max = 2000
    co2Min = input("TRESHOLD MIN CO2  (default value 1000ppm) : ")
    if co2Min == "":
        co2Min = 1000
    print("\nValues for tresholds: \n Max Temperature = " + str(tempMax) + ",\n Min Temperature = " + str(tempMin) + " ,\n Max Humidity = " + str(humMax) + ",\n Min Humidity = " + str(humMin) +",\
                \n Max Co2 = "+ str(co2Max) +", \n Min Co2 = "+ str(co2Min)+"\n\n")
    
    listOfcommands()

    print("System is going to start----->\n")
    time.sleep(5)
    
    client = MqttClient()
    thread = threading.Thread(target=client.mqtt_client, args=(), kwargs={})
    thread.start()
    time.sleep(5)
    print("System is running--->")
    while 1:
        command = input(">")
        command = command.lower()
        checkCommand(command, client)
        

