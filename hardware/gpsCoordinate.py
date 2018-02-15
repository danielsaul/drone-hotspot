import serial
#--------------------------FUNCTION DEFINITIONS--------------------------------

SerialPort = serial.Serial("/dev/ttyUSB3", 115200, timeout = 1)

#function for serial read
def serialread(str):
    read_serial = SerialPort.readline()
    read_decode = read_serial.decode('utf-8')
##    print (read_decode)
    return read_decode

#function to query the turn on gps
def gps_on(str):
    at_on = bytes('AT+QGPS=1\r\n').encode('utf-8')
    SerialPort.write(at_on)


#function to query the turn get coordinates
def get_coordinates(str):
    at_coordinates = bytes('AT+QGPSLOC=2\r\n').encode('utf-8')
    SerialPort.write(at_coordinates)

    blank = serialread('Reading Serial: \r\n')
    response = serialread('Reading Serial: \r\n')
    blank = serialread('Reading Serial: \r\n')
    ok = serialread('Reading Serial: \r\n')  
    blank = serialread('Reading Serial: \r\n')
    ok = serialread('Reading Serial: \r\n')   
    print response

    if "ERROR" in response:
        return None, None

    coords = response.split(',')
    lat = float(coords[1])
    lon = float(coords[2])
    return lat,lon

#function to query the turn off gps
def gps_off(str):
    at_off = bytes('AT+QGPSEND\r\n').encode('utf-8')
    SerialPort.write(at_off)

if __name__ == '__main__':    
    #gps_on('Turn GPS on\r\n')
    #read_decode = serialread('Reading Serial: \r\n')
    #print read_decode
    while get_coordinates('Get GPS coordinate\r\n') == (None,None):
        print "waiting for GPS fix"

    lat,lon = get_coordinates('Get GPS coordinate\r\n')
    print lat,lon


