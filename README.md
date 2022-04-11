# ATMEGA API
Provides an API for ATMEGA microcontroller through FTDI USB device.

# Installation

## Requirements
Install dependencies with pip: `pip install -r requirements.txt`
Install the library with pip: `pip install .`
On linux the user should be in the group `dialout`

# Usage

```python
from atmega.ram import RAM

logging.basicConfig(level=logging.INFO) # Set global logging level

# Create device ram object
dev = RAM()
```