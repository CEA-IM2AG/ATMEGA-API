""" LOW-LEVEL FTDI TOOLS """
from pyftdi.ftdi import Ftdi
from pyftdi.ftdi import UsbTools


def list_urls():
    """ 
        A wrapper for Ftdi.list_devices 
    
        :return: A list of tuples (url, name)
    """
    devices = Ftdi.list_devices() # Get devices
    # Parse devices with UsbTools
    return UsbTools.build_dev_strings("ftdi", 
               Ftdi.VENDOR_IDS, 
               Ftdi.PRODUCT_IDS, 
               devices)

