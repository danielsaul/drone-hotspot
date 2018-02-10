#! /usr/bin/python

import os
from gps import *
from time import *
import time, sys
import threading
from math import *
import ps_drone
import ultrasonic_distance
import RPi.GPIO as GPIO
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins for Ultrasonic sensor
GPIO_TRIGGER = 18
GPIO_ECHO = 17
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

sys.path.insert(0, '/home/pi/drone-hotspot/hardware')
import signalStrength
from gpsCoordinate import *

os.system('clear')  # clear the terminal (optional)

gpsd = None  # setting the global variable

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd  # bring it in scope
        gpsd = gps(mode=WATCH_ENABLE)  # starting the stream of info
        self.current_value = None
        self.running = True  # setting the thread running to true

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()  # this will continue to loop and grab EACH set of gpsd info to clear the buffer


def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles

    # return the distance between 2 GPS coordinates
    return c * r * 1000

def gpsBearing(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    x = sin(dlon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(dlon))

    initial_bearing = atan2(x, y)

    # Normalise the angle to compass bearing
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def flightController(drone, flight_bearing, drone_speed):
    # Retrieve Drone NavData
    NDC = drone.NavDataCount
    while drone.NavDataCount == NDC: time.sleep(0.001)

    drone_yaw = drone.NavData["demo"][2][2]
    print "drone angle" , drone_yaw
    drone_yaw = (drone_yaw + 360) % 360
    turning_angle = flight_bearing - drone_yaw
    if turning_angle > 180:
        turning_angle = turning_angle - 360
    elif turning_angle < -180:
        turning_angle = turning_angle + 360
    print "turning angle" , turning_angle
    drone.turnAngle(turning_angle, 1, 1)
    time.sleep(0.1)
    # drone.move(0.0,drone_speed,0.0,turning_angle)
    drone.moveForward()
    time.sleep(1.0)
    print "moving..."

if __name__ == '__main__':   
    # Drone startup sequence
    drone = ps_drone.Drone()
    drone.startup()
    drone.reset()
    while (drone.getBattery()[0] == -1): time.sleep(0.1)
    print "Battery: " + str(drone.getBattery()[0]) + "%  " + str(drone.getBattery()[1])
    drone.useDemoMode(False)
    drone.getNDpackage(["demo"])
    time.sleep(1.0)
    drone.trim()
    drone.getSelfRotation(5)
    
    # Create gps thread
    #gpsp = GpsPoller()
    #gpsp.start()

    try:
        # os.system('clear')
        
        # Retrieve 4G signal strength
        droneSignalStrength = signalStrength.main()
        print "initial signal strength:" , droneSignalStrength
        
        # Start flight sequence
#        while gpsd.fix.latitude == 0 or gpsd.fix.longitude == 0 or \
#              isnan(gpsd.fix.latitude) or isnan(gpsd.fix.longitude):
#            time.sleep(0.1)
#            print "Waiting for GPS fix"

        while get_coordinates('Get GPS coordinate\r\n') == (None,None):
            print "waiting for GPS fix"
        initialLat,initialLon = get_coordinates('Get GPS coordinate\r\n')
        print initialLat, initialLon

        drone.takeoff()
        while drone.NavData["demo"][0][2]:  time.sleep(0.1)

        flightTime = 10
        refTime = time.time()
        flightEnd = False

        # Assume the drone max speed is 5m/s
        droneSpeed = 0.1 / 5
        drone.setSpeed(droneSpeed)

        while not flightEnd:
            # Receive Destination GPS Coordinates
            destinationLon = -0.13826
            destinationLat = 51.52699
#            currentLon = -0.13814
#            currentLat = 51.52689

            # Receive Current GPS Coordinates
            currentLat,currentLon = get_coordinates('Get GPS coordinate\r\n')
#            print "Current Latitude: ", currentLat,
#            print "Current Longitude: ", currentLon 
#            currentLat = gpsd.fix.latitude
#            currentLon = gpsd.fix.longitude
#            while currentLat == None or currentLon == None:
#                print "waiting for coordinate"
#                drone.stop()

            # Compute actual distance and direction
            flightDistance = haversine(currentLon, currentLat, destinationLon, destinationLat)
            print "Flight distance: " + str(flightDistance)
            flightBearing = gpsBearing(currentLon, currentLat, destinationLon, destinationLat)
            print "Flight bearing: " + str(flightBearing)
            
            # Retrieve ultrasound sensor distance
#            dist = ultrasonic_distance.distance()/100
#            print "obstacle distance: " + str(dist)

            flightController(drone, flightBearing, droneSpeed)
            
            # Retrieve 4G signal strength
            droneSignalStrength = signalStrength.main()
            print "current signal strength:" , droneSignalStrength                   
            if abs(flightDistance) <= 1 or drone.getKey() \
               or time.time() - refTime >= flightTime:
                flightEnd = True

        drone.stop()
        #drone.land()

    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
        print "\nKilling Thread..."
        drone.stop()
        drone.land()
        #gpsd.running = False
        #gpsd.join()  

    print "Done.\nExiting."
