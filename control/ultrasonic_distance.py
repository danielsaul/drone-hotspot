#Libraries
import RPi.GPIO as GPIO
import time

import ps_drone

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 17
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    drone = ps_drone.Drone()						         # Start using drone					
    drone.printBlue("Battery: ")
    drone.startup()	# Connects to drone and starts subprocesses
    drone.reset()       # Always good, at start

    while drone.getBattery()[0] == -1:	time.sleep(0.1)		# Waits until the drone has done its reset
    time.sleep(0.5)											# Give it some time to fully awake 
    drone.printBlue("Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1]))	# Gives a battery-status
	
    stop = False

    while not stop:
        dist = distance()
        print dist
        if dist < 50:
            stop = True

        key = drone.getKey()
        if key == " ":
            if drone.NavData["demo"][0][2] and not drone.NavData["demo"][0][3]:	drone.takeoff()
            else:																drone.land()
	elif key == "0":	drone.hover()
	elif key == "w":	drone.moveForward()
    	elif key == "s":	drone.moveBackward()
    	elif key == "a":	drone.moveLeft()
    	elif key == "d":	drone.moveRight()
    	elif key == "q":	drone.turnLeft()
    	elif key == "e":	drone.turnRight()
    	elif key == "7":	drone.turnAngle(-10,1)
    	elif key == "9":	drone.turnAngle( 10,1)
    	elif key == "4":	drone.turnAngle(-45,1)
    	elif key == "6":	drone.turnAngle( 45,1)
    	elif key == "1":	drone.turnAngle(-90,1)
    	elif key == "3":	drone.turnAngle( 90,1)
    	elif key == "8":	drone.moveUp()
    	elif key == "2":	drone.moveDown()
    	elif key == "*":	drone.doggyHop()
    	elif key == "+":	drone.doggyNod()
    	elif key == "-":	drone.doggyWag()
    	elif key != "":		stop = True
        
        time.sleep(0.1)

    print "Batteries: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])	# Gives a battery-status


#    try:
#        while True:
#            dist = distance()
#            print ("Measured Distance = %.1f cm" % dist)
#            time.sleep(1)
 
#        # Reset by pressing CTRL + C
#    except KeyboardInterrupt:
#        print("Measurement stopped by User")
#        GPIO.cleanup()
