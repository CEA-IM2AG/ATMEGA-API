# ATMEGA API
Provides an API for ATMEGA microcontroller through FTDI USB device.

# Installation

## Requirements
Install dependencies with pip: `pip install -r requirements.txt`
Install the library with pip: `pip install .`
On linux the user should be in the group `dialout`

# Usage

```python
import logging
from atmega.ram import RAM

# Set global logging level
logging.basicConfig(level=logging.INFO)

# Create device ram object
dev = RAM()

# Set high baudrate
dev.change_baudrate(1000000)

# Dump ram into file
dev.dump_ram_to_file("dump.txt")

# Close device
dev.close()
```