""" 
    AN IMPLEMENTATION OF THE RAM MEMORY
    :author: Sofiane DJERBI & Aina PEDERSEN
"""
from time import sleep

from serial import Serial
from serial.serialutil import SerialException

from command import Command
from command import CommandError


class PortError(Exception):
    """ Any error related to hardware ports """
    def __init__(self, message="Unknown Port Error"):
        """ Init the error message """
        self.message = message

    def __str__(self):
        """ Convert to string """
        return self.message



class RS232:
    """ RS232 protocol object """
    def __init__(self, port=None, timeout=5):
        """
            Initialize the interface.
            
            :param port: Port name (None = Auto)
            :param timeout: timeout in seconds
        """
        self.timeout = 10
        if port is None:
            self.resolve_com()
        else:
            try:
                self.serial = Serial(port, stopbits=2)
            except SerialException as e:
                print("Connection to {port} failed. Using resolve_com...")
                self.resolve_com()

    def resolve_com(self):
        for i in range(256):
            try:
                self.serial = Serial(f"COM{i}", stopbits=2)
                print(f"Successfully connected to COM{i}")
                return
            except SerialException as e:
                print(f"Connection to COM{i} failed. Trying COM{i+1}...")
        raise PortError("FTDI port not found.")

    def close(self):
        """ Close the USB connection """
        self.serial.close()
    
    def send_command(self, *args):
        """ Send a command using RS232 protocol """
        self.serial.write(bytearray(args))
        print(f"Sended {args}")

    def get_response(self, length=None):
        """ 
            Receive a command using RS232 protocol

            :param: length of the data (None = auto)
            :return: the response (int array)
        """
        if length is None:
            res = self.serial.read(self.serial.in_waiting)
        else:
            res = self.serial.read(length)
        return list(res)

    def receive_response(self, length=None):
        """ 
            Wait for a response using RS232 protocol

            :param: length of the data (None = auto)
            :return: the response (int array)
        """
        timeout_counter = 0
        buffer = []
        res = []
        # Receive first 3 bits
        while len(res) < 3:
            buffer = self.get_response(length)
            res += buffer
            sleep(0.01)
            timeout_counter += 0.01
            if timeout_counter > self.timeout:
                raise PortError(f"Header timeout: {res}")
        message_len = res[1]*256 + res[2]
        # Receive full message
        while len(res) < message_len + 3:
            buffer = self.get_response(length)
            res += buffer
            sleep(0.01)
            timeout_counter += 0.01
            if timeout_counter > self.timeout:
                raise PortError(f"Body timeout: {res}")
        print(f"Received: {tuple(res)}")
        return res

class RAM(RS232):
    """ ATMEGA RAM implementation using RS232 protocol """
    def __init__(self):
        """ Initialize the object """
        super().__init__()
    
    def reset_ram(self, value=0x00, increment=False, complement=False):
        """
            Set all ram values to value
            :param increment: bool that tells if the ram will be incremented by the value
            :param completment: bool that tells if the ram will be complemented
        """
        p2 = 0
        if increment:
            p2 = 1
        if complement:
            p2 = p2 | 2
        self.send_command(Command.RESET_RAM, value, p2)
        cmd = self.receive_response()
        if cmd != [Command.RESET_RAM, 0, 0]:
            raise CommandError(Command.RESET_RAM, "Cannot reset ram")

    def read_ram(self, location):
        """ Read ram at emplacement location """
        # Split the adress into two bytes
        [adr1, adr2] = list(location.to_bytes(2, 'big'))
        self.send_command(Command.READ_RAM, adr1, adr2)
        cmd = self.receive_response(3)

        return [self.receive_response(3), self.receive]
 
    def read_group_ram(self, adr_start=0, block_size=64):
        """"
            Read a block in the ram
            :param adr_start: adress of the beginning of the block
            :param block_size: size of the wanted block
        """
        # Split the adress into two bytes
        [adr1, adr2] = list(adr_start.to_bytes(2, 'big'))
        self.send_command(Command.READ_GROUP_RAM, adr1, adr2, block_size)

if __name__ == "__main__": # Tests
    rs = RAM()
    rs.reset_ram(0x03)
    rs.close()
