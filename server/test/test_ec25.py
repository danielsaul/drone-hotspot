import unittest
import mock

from ec25_modem.ec25 import Modem

class TestModem(unittest.TestCase):
    def setUp(self):
        self.m = Modem()
