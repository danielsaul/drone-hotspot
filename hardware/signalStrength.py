import serial
#--------------------------FUNCTION DEFINITIONS--------------------------------

#function for serial read
def serialread(str):
    read_serial = SerialPort.readline()
    read_decode = read_serial.decode('utf-8')
    print (read_decode)
    return read_decode

#function to query the signal strength
def format_signal(str):
    at_signal = bytes('AT+CSQ\r\n','utf-8')
    SerialPort.write(at_signal)

#--------------------------------PROGRAM----------------------------------------
# Main program
def main():
    signal_dbm = 0
    print('-------------------------------------\r\n')
    print('Getting signal strength of EC25 module \r\n')
    print('-------------------------------------\r\n')
    format_signal('get RSI values of the EC25 module\r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode[:5] == '+CSQ:':
            print('-------------------------------------\r\n')
            print('Signal Strength:\r\n')
            if read_decode[7] == ',':
                signal_strength = read_decode[6:7]
            if read_decode[8] == ',':
                signal_strength = read_decode[6:8]
            if read_decode[9] == ',':
                signal_strength = read_decode[6:9]
            print(signal_strength)
            print('-------------------------------------\r\n')
            print('Signal Strength in dBm:\r\n')
            if read_decode[7] == ',':
                signal_strength = read_decode[6:7]
            if read_decode[8] == ',':
                signal_strength = read_decode[6:8]
            if read_decode[9] == ',':
                signal_strength = read_decode[6:9]
            if int(signal_strength) == 0:
                signal_dbm = 113
            if int(signal_strength) == 1:
                signal_dbm = 111
            if 2 <= int(signal_strength) <= 30:
                signal_dbm = (2*int(signal_strength))-113
            if int(signal_strength) == 31:
                signal_dbm = -51
            if int(signal_strength) == 99:
                print('Not Known or Undectable! Ignore dBm\r\n')
            if int(signal_strength) == 100:
                signal_dbm = -116
            if int(signal_strength) == 101:
                signal_dbm = -115
            if 102 <= int(signal_strength) <= 190:
                signal_dbm = int(signal_strength)-216
            if int(signal_strength) == 191:
                signal_dbm = -25
            if int(signal_strength) == 199:
                print('Not Known or Undectable! Ignore dBm\r\n')
            print(signal_dbm)
            print('-------------------------------------\r\n')
            print('Bit Error Rate RXQUAL values:\r\n')
            if read_decode[7] == ',':
                bit_error = read_decode[8:]
            if read_decode[8] == ',':
                bit_error = read_decode[9:]
            if read_decode[9] == ',':
                bit_error = read_decode[10:]
            print(bit_error)
            print('-------------------------------------\r\n')
            print('Bit Error Rate percentage values:\r\n')
            if read_decode[7] == ',':
                bit_error = read_decode[8:]
            if read_decode[8] == ',':
                bit_error = read_decode[9:]
            if read_decode[9] == ',':
                bit_error = read_decode[10:]
            if bit_error == '0':
                print('Less than 0.1%')
            if bit_error == '1':
                print('between 0.26% to 0.3%')
            if bit_error == '2':
                print('between 0.51% to 0.64%')
            if bit_error == '3':
                print('between 1.0% to 1.3%')
            if bit_error == '4':
                print('between 1.9% to 2.7%')
            if bit_error == '5':
                print('between 3.8% to 5.4%')
            if bit_error == '6':
                print('between 7.6% to 11.0%')
            if bit_error == '7':
                print('Greater than 15.0%')
            if bit_error == '99':
                print('Not known or undetectable')
        if read_decode == 'OK\r\n':
            break

SerialPort = serial.Serial("/dev/ttyUSB3", 115200, timeout = 1)
main()


