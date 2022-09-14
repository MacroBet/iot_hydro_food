
from itertools import count
import sys
import os
import threading
from time import sleep

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
       return {tempMax,tempMin,humMax,humMin,co2Max,co2Min}
    elif(answer == "no" or answer == "n"):
        return start_configuration()


cfg = start_configuration()
print(cfg[0])