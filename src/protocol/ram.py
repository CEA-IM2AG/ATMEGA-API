""" 
    AN IMPLEMENTATION OF THE RAM MEMORY
    :author: Sofiane DJERBI & Aina PEDERSEN
"""
from serial import Serial
from serial.serialutil import SerialException


class RS232:
    """ RS232 protocol object """
    def __init__(self, url=None):
        """
            Initialize the interface.
            
            :param url: Port name (None = Auto)
        """
        if url is None:
            self.resolve_com()
        else:
            self.serial = Serial(url, stopbits=2)

    def resolve_com(self):
        for i in range(256):
            try:
                self.serial = Serial(f"COM{i}", stopbits=2)
            except SerialException as e:
                print("Error: ", e)

    def close(self):
        """ Close the USB connection """
        self.serial.close()
    
    def send_command(self, *args):
        """ Send a command using RS232 protocol """
        self.serial.write(bytes(bytearray(args)))

    def receive_command(self, length=None)
        """ 
            Receive a command using RS232 protocol

            :param: length of the data (None = auto)
        """
        if length is None:
            self.serial.read(dev.in_waiting)
        else:
            self.serial.read(length)



if __name__ == "__main__": # Tests
    

