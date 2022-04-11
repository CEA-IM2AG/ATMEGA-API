""" 
    ALL ATMEGA RAM COMMANDS
    :author: Sofiane DJERBI, Aina PEDERSEN, Nour LADHARI, Aymes FEJZA
"""

class CommandError(Exception):
    """ Any error related to hardware ports """
    def __init__(self, code, message="Unknown Command Error"):
        """ Init the error message """
        self.message = message
        self.code = hex(code)

    def __str__(self):
        """ Convert to string """
        return f"Command {self.code} error: {self.message}"


class Command:
    """ Command codes """
    RESET_RAM         = 0x55           # Reset all the ram
    WRITE_RAM         = 0x33           # Write in a single emplacement
    READ_RAM          = 0x22           # Read a single emplacement
    READ_GROUP_RAM    = 0x66           # Read multiple emplace
    QUALITY_TEST      = 0xAA           # Perform a i2c quality test
    CHANGE_BAUDRATE   = 0xFF           # Change the value of the baudrate
    BAUD_9600         = 0xCF           # Baudrate 9600
    BAUD_19200        = 0x67           # Baudrate 19200
    BAUD_38400        = 0x33           # Baudrate 38400
    BAUD_1000000      = 0x01           # Baudrate 1000000