import serial
import time

class Modem(object):
    def __init__(self, port):
        self.port = port
        self.ser = None
        
        self.ser_connected = False

    def start(self):
        try:
            self.ser = serial.Serial(self.port, 115200, timeout=1)
            self.ser_connected = True
        except serial.SerialException:
            print "EC25 serial port error connecting: %s" % self.port

        return self.ser_connected

    def turnOnGPS(self):
        res = False
        state = self.getGPSState()
        if state == 0: # GPS is off
            if self.setGPSState(True):
                res = True
        elif state == 1: # GPS is already on
            res = True
        return res

    def turnOffGPS(self):
        res = False
        state = self.getGPSState()
        if state == 1: # GPS is on
            if self.setGPSState(False):
                res = True
        elif state == 0: # GPS is already off
            res = True
        return res

    def setGPSState(self, state):
        cmd = "AT+QGPS=1" if state else "AT+QGPSEND"
        if not self.serWriteLine(cmd):
            return None

        response = self.serRead()
        res = None
        for line in response:
            if line == "OK":
                res = True
                break

        return res

    def getGPSState(self):
        if not self.serWriteLine("AT+QGPS?"):
            return None

        response = self.serRead()
        res = None
        for line in response:
            if line.startswith("+QGPS:"):
                try:
                    state = int(line[7:])
                except (IndexError, ValueError):
                    continue
                res = state
                break

        return res

    def getGPSCoordinates(self):
        if not self.serWriteLine("AT+QGPSLOC=2"):
            return None

        response = self.serRead()
        res = None
        for line in response:
            if line.startswith("+QGPSLOC:"):
                try:
                    fields = line[9:].split(',')
                    lat,lon = map(float, fields[1:3])
                except (IndexError, ValueError):
                    continue
                res = (lat,lon)
                break
        
        return res

    def getSignalStrength(self):
        if not self.serWriteLine("AT+CSQ"):
            return None

        response = self.serRead()
        res = None
        for line in response:
            if line.startswith("+CSQ:"):
                try:
                    rssi,ber = map(int, line[6:].split(','))
                except (IndexError, ValueError):
                    continue
                res = self.mapRSSItodBm(rssi)
                break

        return res

    def mapRSSItodBm(self, rssi):
        dBm = None
        if rssi >= 0 and rssi <= 31:
            dBm = rssi*2 - 113
        if rssi >= 100 and rssi <= 191:
            dBm = rssi - 216

        return dBm

    def serWriteLine(self, string):
        encoded = bytes(string+"\r\n").encode('utf-8')
        res = False
        try:
            self.ser.write(encoded)
            res = True
        except serial.SerialTimeoutException:
            res = False

        return res

    def serRead(self):
        # Expect \r\n<RESPONSE>\r\n
        response = []
        line = ""
        timeout = time.time() + 2
        while line != "OK":
            line = self.ser.readline().decode('utf-8').rstrip()
            if line:
                response.append(line)
            if timeout < time.time():
                break

        return response

