

from ast import Add

class Addresses:

    adWindows = []
    adValves = []

    def insertNewAddress(source, str) :
        
        if str == "valves":
            Addresses.adValves.append(source)
        elif str == "windows":
             Addresses.adWindows.append(source)
             
    
    def constructAddress():
        if Addresses.address is not None:
            return Addresses.address
        else :
            return None