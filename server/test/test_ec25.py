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

    @mock.patch.object(Modem, 'serWriteLine')
    @mock.patch.object(Modem, 'serRead')
    def test_getGPSState_writefail(self, r, w):
        w.return_value = False

        res = self.m.getGPSState()

        w.assert_called_once_with("AT+QGPS?")
        r.assert_not_called()
        self.assertEquals(res, None)

    @mock.patch.object(Modem, 'serWriteLine')
    @mock.patch.object(Modem, 'serRead')
    def test_getGPSState_readempty(self, r, w):
        w.return_value = True
        r.return_value = []

        res = self.m.getGPSState()

        w.assert_called_once_with("AT+QGPS?")
        r.assert_called_once()
        self.assertEquals(res, None)

    @mock.patch.object(Modem, 'serWriteLine')
    @mock.patch.object(Modem, 'serRead')
    def test_getGPSState_readfail(self, r, w):
        w.return_value = True
        r.return_value = ["+QGPS:BLA"]

        res = self.m.getGPSState()

        w.assert_called_once_with("AT+QGPS?")
        r.assert_called_once()
        self.assertEquals(res, None)

    @mock.patch.object(Modem, 'serWriteLine')
    @mock.patch.object(Modem, 'serRead')
    def test_getGPSState_success(self, r, w):
        w.return_value = True
        r.return_value = ["+QGPS: 1"]

        res = self.m.getGPSState()

        w.assert_called_once_with("AT+QGPS?")
        r.assert_called_once()
        self.assertEquals(res, 1)

    @mock.patch.object(Modem, 'serWriteLine')
    @mock.patch.object(Modem, 'serRead')
    def test_getSignalStrength_writefail(self, r, w):
        w.return_value = False

        res = self.m.getSignalStrength()

        w.assert_called_once_with("AT+CSQ")
        r.assert_not_called()
        self.assertEquals(res, None)

    @mock.patch.object(Modem, 'serWriteLine')
    @mock.patch.object(Modem, 'serRead')
    def test_getSignalStrength_readempty(self, r, w):
        w.return_value = True
        r.return_value = []

        res = self.m.getSignalStrength()

        w.assert_called_once_with("AT+CSQ")
        r.assert_called_once()
        self.assertEquals(res, None)

    @mock.patch.object(Modem, 'serWriteLine')
    @mock.patch.object(Modem, 'serRead')
    def test_getSignalStrength_readfail(self, r, w):
        w.return_value = True
        r.return_value = ["+CSQ:BLA"]

        res = self.m.getSignalStrength()

        w.assert_called_once_with("AT+CSQ")
        r.assert_called_once()
        self.assertEquals(res, None)

    @mock.patch.object(Modem, 'serWriteLine')
    @mock.patch.object(Modem, 'serRead')
    @mock.patch.object(Modem, 'mapRSSItodBm')
    def test_getSignalStrength_success(self, rssi, r, w):
        w.return_value = True
        r.return_value = ["+CSQ: 30,99"]
        rssi.return_value = -53

        res = self.m.getSignalStrength()

        w.assert_called_once_with("AT+CSQ")
        r.assert_called_once()
        rssi.assert_called_once_with(30)
        self.assertEquals(res, -53)

    def test_mapRSSItodBm(self):
        self.assertEquals(self.m.mapRSSItodBm(0), -113)
        self.assertEquals(self.m.mapRSSItodBm(1), -111)
        self.assertEquals(self.m.mapRSSItodBm(2), -109)
        self.assertEquals(self.m.mapRSSItodBm(30), -53)
        self.assertEquals(self.m.mapRSSItodBm(31), -51)
        self.assertEquals(self.m.mapRSSItodBm(99), None)

        self.assertEquals(self.m.mapRSSItodBm(100), -116)
        self.assertEquals(self.m.mapRSSItodBm(101), -115)
        self.assertEquals(self.m.mapRSSItodBm(102), -114)
        self.assertEquals(self.m.mapRSSItodBm(190), -26)
        self.assertEquals(self.m.mapRSSItodBm(191), -25)
        self.assertEquals(self.m.mapRSSItodBm(199), None)

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
