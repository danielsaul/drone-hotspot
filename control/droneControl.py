#! /usr/bin/python

import os
from gps import *
from time import *
import time, sys
import threading
from math import *
from gpsdData import GpsPoller
import ps_drone

def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles

    #return the distance between 2 GPS coordinates
    return c * r

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

if __name__ == '__main__':

  #Drone startup sequence
  drone = ps_drone.Drone()
  drone.startup()

  drone.reset()
  while (drone.getBattery()[0] == -1):  time.sleep(0.1)
  print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])
  drone.useDemoMode(False)
  drone.getNDpackage(["demo"])
  time.sleep(1.0)

  #Create gps thread
  gpsp = GpsPoller() 

  try:
    gpsp.start() # start it up
    os.system('clear')

    #Receive Destination GPS Coordinates
    destinationLat   = 0
    destinationLon   = 0

    #Receive Current GPS Coordinates
    currentLat       = gpsd.fix.latitude
    currentLon       = gpsd.fix.longtitude

    #Compute actual distance and direction
    flightDistance   = haversine(currentLon, currentLat, destinationLon, DestinationLat)
    flightBearing    = gpsBearing(currentLon, currentLat, destinationLon, DestinationLat )

    #Retrieve drone NavData
    NDC = drone.NavDataCount
    while drone.NavDataCount == NDC: time.sleep(0.001)
    #Pitch/Roll/Yaw
    aptitude = drone.NavData["demo"][2]

    #Start flight sequence
    #TODO: input to start the sequence
    drone.takeoff()
    #Assume the drone maxspeed is 5m/s
    droneSpeed   = 1/5 #set to 1m/s
    drone.setSpeed(droneSpeed)
    flightTime   = flightDistance/(droneSpeed*5)
    #Rotate the drone to the flight direction
    droneYaw     = aptitude[2]
    turningAngle = flightBearing - droneYaw
    drone.turnAngle(turningAngle,1,1)
    #Start the flight
    refTime      = time.time()
    flightEnd    = False
    drone.moveForward()
    while not flightEnd:
        if time.time() - refTime >= flightTime: end = True
    drone.stop()
    drone.land()

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing

  print "Done.\nExiting."
