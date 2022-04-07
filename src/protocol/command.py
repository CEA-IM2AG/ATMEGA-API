""" 
    ALL ATMEGA RAM COMMANDS
    :author: Sofiane DJERBI & Aina PEDERSEN
"""
from enum import Enum


class CommandError(Exception):
    """ Any error related to hardware ports """
    def __init__(self, code, message="Unknown Port Error"):
        """ Init the error message """
        self.message = message
        self.code = hex(code)

    def __str__(self):
        """ Convert to string """
        return f"Command {self.code} error: {self.message}"

class Command(Enum):
    """ Enum of all commands """
    RESET_RAM  = 0x55          # Reset all the ram
    WRITE_RAM = 0x22           # Write in a single emplacement
    READ_RAM = 0x22            # Read a single emplacement
    READ_GROUP_RAM  = 0x66     # Read multiple emplacement
