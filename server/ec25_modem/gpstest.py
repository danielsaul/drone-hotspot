from ec25 import Modem
import time

m = Modem("/dev/ttyUSB2")

m.start()

m.turnOnGPS()

while 1:
	print m.getSignalStrength()
	print m.getGPSCoordinates()
	time.sleep(3)
