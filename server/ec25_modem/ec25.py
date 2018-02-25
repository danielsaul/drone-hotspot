import serial

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

    def getSignalStrength(self):
        pass

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
        while line != "OK":
            line = self.ser.readline().decode('utf-8').rstrip()
            if line:
                response.append(line)

        return response

