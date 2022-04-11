# ATMEGA API
Provides an API for ATMEGA microcontroller through an FTDI USB device.

# Installation

## Requirements
**Install dependencies** with pip: `pip install -r requirements.txt`  
**Install the library** with pip: `pip install .`  
**Note:** On linux the user should be in the group `dialout`  
**Run tests:** `python setup.py test`

# Usage

```python
import logging
from atmega.ram import RAM

# Set global logging level
logging.basicConfig(level=logging.INFO)

# Create device ram object
dev = RAM()

# Reset ram to 0x11
dev.reset(0x11)

# Set high baudrate
dev.change_baudrate(1000000)

# Dump ram into file
dev.dump_to_file("dump.txt")

# Close device
dev.close()
```