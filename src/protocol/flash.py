""" 
    AN IMPLEMENTATION OF THE FLASH MEMORY 
    Somewhat wrapping spiflash's interface
    :author: Sofiane DJERBI
"""
from spiflash.serialflash import SerialFlashManager
from spiflash.serialflash import SerialFlash


class Flash:
    """ Flash interface object """
    def __init__(self, url, mhz=8):
        """
            Initialize the interface.
            
            :param url: Url of the interface
            :param mhz: Frequency in mhz (FTDI) 
        """
        self.frequency = mhz*1E6
        # Open SPI interface
        manager = SerialFlashManager()
        self.spi = SpiController()
        self.spi.configure(url, frequency=self.frequency)
        # Get a port to a slave
        self.slave = self.interface.get_port(cs=0, freq=self.frequency)
        # Setting interface constants
        self.interface.read_data_set_chunksize(512)

    def close(self):
        """ Close the USB connection """
        self.spi.close()


if __name__ == "__main__": # Tests
    from ftdi import *
    # Choose device
    devices = list_urls()
    print("Please choose your device:")
    for i in range(len(devices)):
        print(f"{i+1}: {devices[i][0]}")
    pid = int(input("Choice: ")) - 1
    url = devices[pid][0]
    device = SPI(url)
    device.close()

