import unittest
import mock
import serial
from ec25_modem.ec25 import Modem

class TestModem(unittest.TestCase):
    def setUp(self):
        self.port = "/dev/testport"
        self.m = Modem(self.port)
        self.m.ser = mock.Mock()

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

    def test_serWriteLine(self):
        res = self.m.serWriteLine("AT")

        self.m.ser.write.assert_called_once()

    def test_serRead_withOK(self):
        fake = [
            "\r\n",
            "+CSQ: 10,10\r\n",
            "\r\n",
            "OK\r\n"
        ]
        self.m.ser.readline.side_effect = fake

        res = self.m.serRead()

        self.assertEquals(self.m.ser.readline.call_count, 4)
        self.assertEquals(res, ["+CSQ: 10,10", "OK"])

    @mock.patch('time.time')
    def test_serRead_timeout(self, t):
        fake = [
            "\r\n",
            "+CSQ: 10,10\r\n",
            "\r\n",
            "\r\n"
        ]
        self.m.ser.readline.side_effect = fake
        t.side_effect = [0, 0.5, 1, 1.5, 3]


        res = self.m.serRead()

        self.assertEquals(self.m.ser.readline.call_count, 4)
        self.assertEquals(res, ["+CSQ: 10,10"])
