

from ast import Add


class Addresses:

    address = []

    def insertNewAddress(source) :
            
        Addresses.address.append(source)
    
    def constructAddress():
        if Addresses.address is not None:
            return Addresses.address
        else :
            return None