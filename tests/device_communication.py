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
        """
            Test read_group and reset functions
        """
        self.dev.reset(0xF0)
        mem = self.dev.read_group(0x1000, 100)
        self.assertEqual(mem, [0xF0]*100)

    def test_write(self):
        """
            Test write and read functions
        """
        self.dev.reset(0x34)
        self.dev.write(0xF1, 0x32F5)
        self.assertEqual(0xF1, self.dev.read(0x32F5))
        self.assertEqual(0x34, self.dev.read(0x32F4))
        self.assertEqual(0x34, self.dev.read(0x32F6))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
