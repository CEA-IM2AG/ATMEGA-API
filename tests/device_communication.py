"""
    Unit tests
    :author: Sofiane DJERBI
"""
import logging
import unittest
from unittest import TestCase
from atmega.ram import RAM

class TestRAM(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRAM, self).__init__(*args, **kwargs)
        self.dev = RAM()

    def test_reset(self):
        self.dev.reset(0xF0)
        mem = self.dev.read_group(0x1000, 100)
        self.assertEqual(mem, [0xF0]*100)

    def test_write(self):
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
