""" 
    AN IMPLEMENTATION OF THE RAM MEMORY
    :author: Sofiane DJERBI & Aina PEDERSEN
"""
import logging

from time import sleep, time

from serial import Serial
from serial.serialutil import SerialException

from atmega.command import Command
from atmega.command import CommandError

from sys import platform


log = logging.getLogger("ATMEGA RAM")

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
        self.timeout = timeout
        if port is None:
            self.resolve_com()
        else:
            try:
                self.serial = Serial(port, stopbits=2)
            except SerialException as e:
                log.warning("Connection to {port} failed. Using resolve_com...")
                self.resolve_com()
        self.quality_test()

    def resolve_com(self):
        """ Find available serial device """
        if platform == "win32":
            device = "COM"
        elif "linux" in platform:
            device = "/dev/ttyUSB"
        else:
            raise Exception("Operating system not supported. Cannot find device.")
        for i in range(256):
            try:
                self.serial = Serial(f"{device}{i}", stopbits=2)
                log.info(f"Successfully connected to {device}{i}")
                return
            except SerialException as e:
                log.debug(f"Connection to {device}{i} failed. Trying {device}{i+1}...")
        raise PortError("FTDI port not found.")
    
    def quality_test(self):
        """ i2c Quality communication test """
        log.debug("Performing quality test...")
        counter = 0
        for adr_i2c in range(100):
            self.send_command(Command.QUALITY_TEST, adr_i2c, 0)
            header, body = self.receive_response()
            if header != [Command.QUALITY_TEST, 0, 1]:
                break
            elif body == [adr_i2c]:
                counter += 1
        if counter != 100:
            raise PortError("RS232 connexion failed")

    def change_baudrate(self, baudrate):
        """
            Change the baudrate
            :param baudrate: New baudrate value in decimal (9600/19200/38400/1000000)
        """
        log.info(f"Changing baudrate to {baudrate}...")
        if baudrate == 9600:
            baudrate_cmd = Command.BAUD_9600
        elif baudrate == 19200:
            baudrate_cmd = Command.BAUD_19200
        elif baudrate == 38400:
            baudrate_cmd = Command.BAUD_38400
        elif baudrate == 1000000:
            baudrate_cmd = Command.BAUD_1000000
        else:
            raise CommandError(Command.CHANGE_BAUDRATE, "Invalid baudrate value")
        self.send_command(Command.CHANGE_BAUDRATE, 0, baudrate_cmd)
        sleep(0.1) # Sleep to sync with device
        self.serial.baudrate = baudrate
        try:
            head, body = self.receive_response()
        except PortError as e:
            raise CommandError(Command.CHANGE_BAUDRATE, "Timeout while changing baudrate")
        if head != [Command.CHANGE_BAUDRATE, 0, 1] or body != [0xAA]:
            raise CommandError(Command.CHANGE_BAUDRATE, "Error while changing baudrate")

    def close(self):
        """ Close the USB connection """
        if self.serial.baudrate != 9600:
            self.change_baudrate(9600)
        self.serial.close()
    
    def send_command(self, *args):
        """ Send a command using RS232 protocol """
        self.serial.write(bytearray(args))
        log.debug(f"Sended {args}")

    def get_response(self, length=None):
        """ 
            Receive a command using RS232 protocol

            :param length: length of the data (None = auto)
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

            :param length: length of the data (None = auto)
            :return: the response (int array)
        """
        timeout_counter = 0
        buffer = []
        header = [] # The header is 3 bits: CODE OP / LEN 1 / LEN 2

        # Receive first 3 bits
        while len(header) < 3:
            buffer = self.get_response(length)
            header += buffer
            sleep(0.01)
            timeout_counter += 0.01
            if timeout_counter > self.timeout:
                raise PortError(f"Header timeout: {header}")
        message_len = header[1]*256 + header[2]
        body = header[3:]    # Message body (can be empty)
        header = header[:3]
        # Receive full message
        while len(body) < message_len:
            buffer = self.get_response(length)
            body += buffer
            sleep(0.01)
            timeout_counter += 0.01
            if timeout_counter > self.timeout:
                raise PortError(f"Body timeout: {body} (Header = {header})")
        log.debug(f"Received: {header + body}")
        return header, body


class RAM(RS232):
    """ ATMEGA RAM implementation using RS232 protocol """
    def __init__(self):
        """ Initialize the object """
        super().__init__()
        self.ram_size = 2**14
    
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
        log.info("Resetting ram...")
        self.send_command(Command.RESET_RAM, value, p2)
        header, _ = self.receive_response()
        if header != [Command.RESET_RAM, 0, 0]:
            raise CommandError(Command.RESET_RAM, "Cannot reset ram")

    def read_ram(self, location):
        """ Read ram at emplacement location """
        # Split the adress into two bytes
        [adr1, adr2] = list(location.to_bytes(2, 'big'))
        self.send_command(Command.READ_RAM, adr1, adr2)
        header, res = self.receive_response()
        if header != [Command.READ_RAM, 0, 1]:
            raise CommandError(Command.READ_RAM, "Cannot read ram")
        return res
 
    def read_group_ram(self, adr_start=0, block_size=64):
        """"
            Read a block in the ram
            :param adr_start: adress of the beginning of the block
            :param block_size: size of the wanted block
        """
        # Split the adress into two bytes
        [adr1, adr2] = list(adr_start.to_bytes(2, 'big'))
        self.send_command(Command.READ_GROUP_RAM, adr1, adr2, block_size)
        header, res = self.receive_response()
        if header  != [Command.READ_GROUP_RAM, 0, block_size]:
            raise CommandError(Command.READ_GROUP_RAM, "Cannot read group ram")
        return res

    def dump_ram(self, reserve_stack=0):
        """
            Read the whole ram
            :param reserve_stack: number of bytes to skip at the end of the ram
        """
        adr_ram = 0
        block_size = 128
        res = []
        log.info("Dumping ram...")
        t = time()
        while (adr_ram < self.ram_size - reserve_stack):
            res += self.read_group_ram(adr_ram, block_size)
            adr_ram += block_size
        log.info(f"Ram dumped in {time() - t} seconds")
        return res

    def dump_ram_to_file(self, file, reserve_stack=0):
        """
            Read the whole ram and save it in a file
            :param reserve_stack: number of bytes to skip at the end of the ram
        """
        data = self.dump_ram(reserve_stack)
        f = open(file, "w+")
        for i in range(len(data)):
            f.write("{:04x}:".format(i))
            f.write("{:02x}\n".format(data[i]))
        f.close()
            

if __name__ == "__main__": # Tests
    logging.basicConfig(level=logging.INFO)
    rs = RAM()
    rs.reset_ram(0x69)
    ram_val = rs.read_ram(10000)
    rs.dump_ram_to_file("dump.txt")
    rs.change_baudrate(1000000)
    whole_ram = rs.dump_ram()
    rs.close()
