import serial
import time

#function for sending
def Sending(message, sender):
    SerialPort = serial.Serial("COM14",115200, timeout = 1)
    SerialPort.write(b'AT+CMGF=1\r')
    time.sleep(1)
    b = bytes('AT+CMGS="'+sender+'"\r\n', 'utf-8')
    SerialPort.write(b)
    time.sleep(1)
    a = bytes(message+"\x1A", 'utf-8')
    SerialPort.write(a)
    #while 1:
    read_2 = SerialPort.readline()
    print (read_2)
    print('message sent')

x = input("type the number: \n")
y = input("type the message: \n")


Sending(y,x)

#function for calling
def Calling(number):
    SerialPort = serial.Serial("COM14",115200, timeout = 1)
    c = bytes('ATD'+number+';\r\n','utf-8')
    SerialPort.write(c)
    while 1:
        read_1 = SerialPort.readline()
        print (read_1)
        print('Calling......')

z = input("type the number: \n")

Calling(z)


#function for checking signal strength
#def Signal(test):
    #SerialPort = serial.Serial("COM14", 115200, timeout = 1)
    #d = bytes('AT+CSQ\r\n', 'utf-8')
    #SerialPort.write(d)
    #while 1:
        #read_3 = SerialPort.readline()
        #print (read_3)
        #print('checking signal strength')
    

#a = input('type anything here: \n')
#Signal(a)
