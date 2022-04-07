""" 
    ALL ATMEGA RAM COMMANDS
    :author: Sofiane DJERBI & Aina PEDERSEN
"""
from enum import Enum


class Command(Enum):
    """ Enum of all commands """
    INIT_RAM  = 0x55
    WRITE_RAM = 0x22
    READ_RAM  = 0x66    
