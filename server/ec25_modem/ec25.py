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

