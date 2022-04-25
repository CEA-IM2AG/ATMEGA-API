"""
    AN IMPLEMENTATION OF THE RAM MEMORY
    :author: Sofiane DJERBI, Aina PEDERSEN, Nour LADHARI, Aymes FEJZA
"""
import logging

from time import sleep, time

from serial import Serial
from serial.serialutil import SerialException

from atmega.command import Command
from atmega.command import CommandError

from sys import platform


log = logging.getLogger("ATMEGA RAM")


def list_devices():
    """
        Find available serial devices

        :return: a list of available serial devices names
    """
    """
        Liste tout les USB branchés sur l'ordinateur.
    """
    if platform == "win32": # Cas windows
        prefix = "COM"
    elif "linux" in platform: # Cas linux
        prefix = "/dev/ttyUSB"
    else: # OS inconnu
        raise Exception("Operating system not supported. Cannot find device.")
    device = []
    for i in range(256): # On teste tous les ports
        try: # On a trouvé un device
            serial = Serial(f"{prefix}{i}", stopbits=2)
            log.info(f"Successfully connected to {prefix}{i}")
            device.append(f"{prefix}{i}")
        except SerialException as e:
            log.debug(f"Connection to {prefix}{i} failed. Trying {prefix}{i+1}...")
    return device


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
    def __init__(self, port=None, timeout=5, quality_test=False):
        """
            Initialize the interface.

            :param port: port name (None = Auto)
            :param timeout: timeout in seconds
            :param quality_test: do a quality test ?
        """
        self.timeout = timeout
        if port is None: # Si aucun port est donné on cherche automatiquement
            self.resolve_com()
        else:
            try: # Sinon on essaie le port fourni
                self.serial = Serial(port, stopbits=2)
            except SerialException as _:
                log.warning("Connection to {port} failed. Using resolve_com...")
                self.resolve_com()
        if quality_test: # Si besoin on fait un test de qualité
            self.quality_test()

    def resolve_com(self):
        """ Take the first USB device as serial """
        """ Utilise le premier port usb reconnu en tant que périphérique """
        device = list_devices()
        if device == []: # Si on a rien trouvé
            raise PortError("FTDI port not found.")
        self.serial = Serial(device[0], stopbits=2)

    def quality_test(self):
        """ i2c Quality communication test """
        log.debug("Performing quality test...")
        for adr_i2c in range(100): # On effectue le test de qualité i2c
            self.send_command(Command.QUALITY_TEST, adr_i2c, 0)
            header, body = self.receive_response()
            if header != [Command.QUALITY_TEST, 0, 1] or body != [adr_i2c]:
                raise PortError("RS232 connexion failed")

    def change_baudrate(self, baudrate):
        """
            Change the baudrate

            :param baudrate: New baudrate value in decimal (9600/19200/38400/1000000)
        """
        """ Change la vitesse de communication avec le device """
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
        sleep(0.1) # On attend un peu que le device ce soit synchronisé
        self.serial.baudrate = baudrate
        try:
            head, body = self.receive_response()
        except PortError as e:
            raise CommandError(Command.CHANGE_BAUDRATE, "Timeout while changing baudrate")
        if head != [Command.CHANGE_BAUDRATE, 0, 1] or body != [0xAA]:
            raise CommandError(Command.CHANGE_BAUDRATE, "Error while changing baudrate")

    def close(self):
        """ Close the USB connection """
        if self.serial.baudrate != 9600: # On remet le baudrate à 9600 pour éviter les erreurs
            self.change_baudrate(9600) # reset to initial state
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
        if length is None: # Si aucune taille est spécifiée
            res = self.serial.read(self.serial.in_waiting)
        else: # Sinon
            res = self.serial.read(length)
        return list(res)

    def receive_response(self, length=None):
        """
            Wait for a response using RS232 protocol

            :param length: length of the data (None = auto)
            :return: the response (int array)
        """
        timeout_counter = 0 # Compteur de secondes avant un timeout
        # The header is 3 bits: CODE OP / LEN 1 / LEN 2
        while self.serial.in_waiting < 3: # On attend le header
            sleep(0.01) # Le temps de recevoir les commandes
            timeout_counter += 0.01
            if timeout_counter > self.timeout:
                raise PortError(f"Header timeout: {self.get_response()}")
        header = self.get_response(3) # Header = 3 premiers bits décrivant le message
        message_len = header[1]*256 + header[2]
        # Receive full message
        while self.serial.in_waiting < message_len: # On attend le body
            sleep(0.01)
            timeout_counter += 0.01
            if timeout_counter > self.timeout:
                raise PortError(f"Body timeout: {self.get_response()} (Header = {header})")
        body = self.get_response() # Body = contenu du message
        log.debug(f"Received: [{header}] {body}")
        return header, body


class RAM(RS232):
    """ ATMEGA RAM implementation using RS232 protocol """
    def __init__(self, port=None, timeout=5, quality_test=False,
                 ram_size=2**14):
        """
            Initialize the RS232 object

            :param port: RS232 FTDI port
            :param timeout: communication timeout in seconds
            :param quality_test: do a quality test ?
            :param ram_size: size of the ram
        """
        super().__init__(port, timeout, quality_test)
        self.ram_size = ram_size # Support atmega différente ram

    def reset(self, value=0x00, increment=False, complement=False):
        """
            Set all ram values to value

            :param value: value that will be set (int)
            :param increment: bool that tells if the ram will be incremented by the value
            :param completment: bool that tells if the ram will be complemented
        """
        """ Reset/complémente/incrémente la ram avec "value" """
        p = 0 # Nature de la commande
        if increment: # Si on incrémente au lieu de reset, p = 1
            p = 1
        if complement: # Si on complémente au lieu de reset, p = p | 2 (complémente)
            p = p | 2
        log.info("Resetting ram...")
        self.send_command(Command.RESET_RAM, value, p)
        header, _ = self.receive_response()
        if header != [Command.RESET_RAM, 0, 0]: # Si le header n'est pas correct
            raise CommandError(Command.RESET_RAM, "Cannot reset ram")

    def write(self, value, location):
        """
            Write value at emplacement location

            :param value: value to write
            :param location: location to write
        """
        """ Ecrit un seul octet dans la ram """
        [adr1, adr2] = list(location.to_bytes(2, 'big')) # On convertit notre message en bit
        self.send_command(Command.WRITE_RAM, adr1, adr2, value)
        header, res = self.receive_response()
        if header != [Command.WRITE_RAM, 0, 0]: # Si le header n'est pas correct
            raise CommandError(Command.WRITE_RAM, "Cannot write to single address")
        return res

    def read(self, location):
        """
            Read ram at a single location

            :param location: location to read
        """
        """ Lis 1 octet dans la ram """
        [adr1, adr2] = list(location.to_bytes(2, 'big')) # On convertit l'addresse en bytes
        self.send_command(Command.READ_RAM, adr1, adr2)
        header, res = self.receive_response()
        if header != [Command.READ_RAM, 0, 1]:
            raise CommandError(Command.READ_RAM, "Cannot read ram")
        return res[0]

    def read_group(self, adr_start=0, block_size=64):
        """"
            Read a block in the ram

            :param adr_start: adress of the beginning of the block
            :param block_size: size of the wanted block
        """
        """ Lis un block de plusieurs octets dans la ram """
        # Split the adress into two bytes
        [adr1, adr2] = list(adr_start.to_bytes(2, 'big')) # On convertit l'addresse en bytes
        self.send_command(Command.READ_GROUP_RAM, adr1, adr2, block_size)
        header, res = self.receive_response()
        if header  != [Command.READ_GROUP_RAM, 0, block_size]:
            raise CommandError(Command.READ_GROUP_RAM, "Cannot read group ram")
        return res

    def dump(self, reserve_stack=0, block_size=128):
        """
            Read the whole ram

            :param reserve_stack: number of bytes to skip at the end of the ram
        """
        """ Dump toute la ram dans une liste python """
        adr_ram = 0
        res = []
        log.info("Dumping ram...")
        t = time()
        while (adr_ram < self.ram_size - reserve_stack): # On lit par groupe de block_size
            res += self.read_group(adr_ram, block_size)
            adr_ram += block_size
        log.info(f"Ram dumped in {time() - t} seconds")
        return res

    def dump_to_file(self, file, reserve_stack=0, block_size=64):
        """
            Read the whole ram and save it in a file

            :param file: dump file to create/overwrite
            :param reserve_stack: number of bytes to skip at the end of the ram
        """
        """ Dump la ram dans un fichier """
        data = self.dump(reserve_stack, block_size)
        f = open(file, "w+")
        for i in range(len(data)): # On écrit chaque ligne en format hex:val (xxxx:xx)
            f.write("{:04x}:".format(i))
            f.write("{:02x}\n".format(data[i]))
        f.close()


if __name__ == "__main__": # Tests
    logging.basicConfig(level=logging.INFO)
    rs = RAM()
    rs.change_baudrate(1000000)
    rs.reset(0x10)
    rs.write(0x52, 0x34F2)
    for i in range(10):
        x = rs.read(0x34F0 + i)
        print(x)
    rs.close()
