import serial
import time

#--------------------------FUNCTION DEFINITIONS--------------------------------

#function for serial read
def serialread(str):
    read_serial = SerialPort.readline()
    read_decode = read_serial.decode('utf-8')
    print (read_decode)
    return read_decode

#function for AT SYNC
def format_sync(str):
    at_query = bytes('AT\r\n','utf-8')
    SerialPort.write(at_query)
    return

#function to set response format
def format_set(str):
    at_format = bytes('ATV1\r\n','utf-8')
    SerialPort.write(at_format)
    return

#function to enable echo mode
def format_echo(str):
    at_echo = bytes('ATE1\r\n','utf-8')
    SerialPort.write(at_echo)
    return


#function to enable error result code with verbose (string) values
def format_error(str):
    at_error = bytes('AT+CMEE=2\r\n','utf-8')
    SerialPort.write(at_error)
    return

#function to get baudrate
def format_baudrate(str):
    at_baudrate = bytes('AT+IPR?\r\n','utf-8')
    SerialPort.write(at_baudrate)
    return

#function to set baudrate and store the setting
def format_baudsetting(str):
    at_baudsetting = bytes('AT+IPR=115200;&W\r\n','utf-8')
    SerialPort.write(at_baudsetting)
    return


#function to get module information of Manufacturer ID, Device module and Firmware Version */
def format_information(str):
    at_information = bytes('ATI\r\n','utf-8')
    SerialPort.write(at_information)
    return

#function to query IMEI of module
def format_IMEI(str):
    at_IMEI = bytes('AT+GSN\r\n','utf-8')
    SerialPort.write(at_IMEI)
    return


#function to configure the output port of URC
def format_port(str):
    at_port = bytes('AT+QURCCFG="URCPORT","usbat"\r\n','utf-8')
    SerialPort.write(at_port)
    return

#function to query sim card status
def query_sim(str):
    sim_call = bytes('AT+CPIN?\r\n','utf-8')
    SerialPort.write(sim_call)
    return

#function to enter sim card pin
def enter_pin(str):
    pin_number = input("Enter the pin number: \n") 
    c = bytes('AT+CPIN='+pin_number+'\r\n','utf-8')
    SerialPort.write(c)
    return

#function to enter PUK and new sim pin number
def enter_puk(str):
    puk_number = input("Enter PUK number: \n")
    sim_number = input ("Enter new Sim Pin number: \n")
    d = bytes('AT+CPIN=''"'+puk_number+'"'',''"'+sim_number+'"''\r\n')
    SerialPort.write(d)
    return

#function to query IMSI of SIM card
def format_IMSI(str):
    at_IMSI = bytes('AT+CIMI\r\n','utf-8')
    SerialPort.write(at_IMSI)
    return

#function to query ICCID number of SIM card
def format_ICCID(str):
    at_ICCID = bytes('AT+QCCID\r\n','utf-8')
    SerialPort.write(at_ICCID)
    return

#function to query the signal strength
def format_signal(str):
    at_signal = bytes('AT+CSQ\r\n','utf-8')
    SerialPort.write(at_signal)
    return

#function for querying Network 
def query_network(str):
    query_call = bytes('AT+CREG?\r\n','utf-8')
    SerialPort.write(query_call)
    return

#function for querying PS Network
def ps_network(str):
    ps_call = bytes('AT+CGREG?\r\n','utf-8')
    SerialPort.write(ps_call)
    return

#function to query Network Operator
def format_network(str):
    at_network = bytes('AT+COPS?\r\n','utf-8')
    SerialPort.write(at_network)
    return


#--------------------------------PROGRAM----------------------------------------
# Main program
def main():
    print('-------------------------------------\r\n')
    print('Connecting to the EC25 module \r\n')
    print('-------------------------------------\r\n')
    sim_start = time.time()
    sim_elapsed = 0
    read_decode = 0
    atsync_count = 0
    while 1:
        sim_end = time.time()
        sim_elapsed = sim_end - sim_start
        if sim_elapsed > 0.5:
            sim_start = time.time()
            format_sync('sent AT every 500ms, if receive OK, SYNC success')
            read_decode = serialread('Reading Serial: \r\n')
            read_decode = serialread('Reading Serial: \r\n')
            if read_decode == 'OK\r\n':
                print('SYNC SUCCESS\r\n')
                break
            else:
                atsync_count = atsync_count + 1
                if atsync_count == 10:
                    print('SYNC FAIL !! restart program \r\n')
                    main()
    print('-------------------------------------\r\n')
    print('proceeding to set the response format\r\n')
    print('-------------------------------------\r\n')
    format_set('Use ATV1 to set the response format\r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == 'OK\r\n':
            break
    print('-------------------------------------\r\n')
    print('proceeding to enable echo mode \r\n')
    print('-------------------------------------\r\n')
    format_echo('Use ATE1 to enable echo mode \r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == 'OK\r\n':
            break
    print('-------------------------------------\r\n')
    print('proceeding to enable result and use verbose values\r\n')
    print('-------------------------------------\r\n')
    format_error('Use AT+CMEE=2 to enable result code and use verbose values \r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == 'OK\r\n':
            break
    print('-------------------------------------\r\n')
    print('proceeding to get the baudrate\r\n')
    print('-------------------------------------\r\n')
    format_baudrate('get the baudrate \r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == '+IPR: 115200\r\n':
            print('115200bps is the default \r\n')
            while 1:
                read_decode = serialread('Reading Serial: \r\n')
                if read_decode == 'OK\r\n':
                    break
            break
    else:
        print('setting baudrate to 115200.....\r\n')
        format_baudsetting('set the baudrate\r\n')
        while 1:
            read_decode = serialread('Reading Serial: \r\n')
            if read_decode == 'OK\r\n':
                break
            break
    print('-------------------------------------\r\n')
    print('proceeding to get module information\r\n')
    print('-------------------------------------\r\n')
    format_information('Use ATI to get module information\r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == 'OK\r\n':
            break
    print('-------------------------------------\r\n')
    print('proceeding to get IMEI of module\r\n')
    print('-------------------------------------\r\n')
    format_IMEI('Use AT+GSN to query the IMEI of module\r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == 'OK\r\n':
            break
    print('-------------------------------------\r\n')
    print('proceeding to configure the output port of the URC\r\n')
    print('-------------------------------------\r\n')
    format_port('format URC port to use USB AT port\r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == 'OK\r\n':
            break
    print('-------------------------------------\r\n')
    print('proceeding to querying pin status\r\n')
    print('-------------------------------------\r\n')
    query_sim('Query the SIM card status\r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == '+CPIN: SIMPIN\r\n':
            enter_pin("Entering Sim Pin Mode\r\n")
            query_sim("Query Sim Status again\r\n")
        if read_decode == '+CPIN: SIMPUK\r\n':
            enter_puk("Entering PUK mode")
            query_sim("Query Sim Status again\r\n")
        if read_decode == '+CPIN: READY\r\n':
            while 1:
                read_decode = serialread('Reading Serial: \r\n')
                if read_decode == 'OK\r\n':
                    break
            break
    print('-------------------------------------\r\n')
    print('proceeding to querying IMSI of the SIM card\r\n')
    print('-------------------------------------\r\n')
    format_IMSI('Use AT+CIMI to query the IMSI of the SIM card\r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == 'OK\r\n':
            break
    print('-------------------------------------\r\n')
    print('proceeding to querying ICCID number of the SIM card\r\n')
    print('-------------------------------------\r\n')
    format_ICCID('Use AT+QCCID to query ICCID number of the SIM card\r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == 'OK\r\n':
            break
    print('-------------------------------------\r\n')
    print('proceeding to query the signal strength of the mobile network\r\n')
    print('-------------------------------------\r\n')
    format_signal('Use AT+CSQ to query current signal quality\r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == 'OK\r\n':
            break
    print('-------------------------------------\r\n')
    print('proceeding to querying the network \r\n')
    print('-------------------------------------\r\n')
    query_network('Use AT+CREG to query the network report\r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == 'OK\r\n':
            break
    print('-------------------------------------\r\n')
    print('proceeding to querying the PS network \r\n')
    print('-------------------------------------\r\n')
    ps_network('Use AT+CGREG to query the network registration status\r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == 'OK\r\n':
            break
    print('-------------------------------------\r\n')
    print('proceeding to querying current Network Operator \r\n')
    print('-------------------------------------\r\n')
    format_network('Use AT+COPS? to query current Network Operator \r\n')
    while 1:
        read_decode = serialread('Reading Serial: \r\n')
        if read_decode == 'OK\r\n':
            break
    print('-------------------------------------\r\n')
    print('EC25 module is connected and Sim Card is READY \r\n')
    print('-------------------------------------\r\n')
    
SerialPort = serial.Serial("COM7", 115200, timeout = 1)
main()


