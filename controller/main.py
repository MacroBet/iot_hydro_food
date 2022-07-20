
from pydoc import cli
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
        mex = client.message
        print(client.message)
        try:
            while True:
                if(mex != client.message):
                    print("Press ctrl + C to exit \n")
                    print(client.message)
        except KeyboardInterrupt:
         return
            
    elif command == "!change values of thresholds":
           print("......")
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
    else:
        print("Command not found")
        listOfcommands()

def showInfo():

    print("check log of sensors ---> check message that the sensord send to the application \n"\
          "change values of threshold ---> change value of temperature humidity and Co2 that has been setted at the start\n"\
          "change value co2 ---> chack only the values of Co2\n"\
          "change value humidity ---> check only the values of humidity\n"\
          "change value temperature ---> check only the values of temperature\n"\
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
    
    client = MqttClient()
    client.tempMax = tempMax
    client.tempMin = tempMin
    client.humMax = humMax
    client.humMin = humMin
    client.co2Max = co2Max
    client.co2Min = co2Min
    thread = threading.Thread(target=client.mqtt_client, args=(), kwargs={})
    thread.start()

    time.sleep(5)
    print("System is running--->\n ")
    while 1:
        command = input("COMMAND>")
        command = command.lower()
        checkCommand(command, client)
        

