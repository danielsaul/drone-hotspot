import unittest
import mock
import serial
from ec25_modem.ec25 import Modem

class TestModem(unittest.TestCase):
    def setUp(self):
        self.port = "/dev/testport"
        self.m = Modem(self.port)

    @mock.patch('ec25_modem.ec25.serial.Serial')
    def test_start_serialsuccess(self, s):
        res = self.m.start()

        s.assert_called_once_with(self.port, 115200, timeout=1)
        self.assertEquals(res, True)
        self.assertEquals(self.m.ser_connected, True)

    @mock.patch('ec25_modem.ec25.serial.Serial')
    def test_start_serialfail(self, s):
        s.side_effect = serial.SerialException()

        res = self.m.start()

        s.assert_called_once_with(self.port, 115200, timeout=1)
        self.assertEquals(res, False)
        self.assertEquals(self.m.ser_connected, False)
