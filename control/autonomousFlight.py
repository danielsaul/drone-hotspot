from droneControl import *
import os
from time import *
import time, sys
import threading
from math import *
import ps_drone
import numpy as np

sys.path.insert(0, '/home/pi/drone-hotspot/hardware')
import signalStrength
from gpsCoordinate import *

def displaceXY(lat,lng,theta, distance):
    #Formula for large circle over long distance
    theta = np.float32(theta)
    radius = 6371 #km

    delta = np.divide(np.float32(distance), np.float32(radius))

    theta = np.deg2rad(theta)
    lat1 = np.deg2rad(lat)
    lng1 = np.deg2rad(lng)

    lat2 = np.arcsin( np.sin(lat1) * np.cos(delta) +
                      np.cos(lat1) * np.sin(delta) * np.cos(theta) )

    lng2 = lng1 + np.arctan2( np.sin(theta) * np.sin(delta) * np.cos(lat1),
                              np.cos(delta) - np.sin(lat1) * np.sin(lat2))

    lng2 = (lng2 + 3 * np.pi) % (2 * np.pi) - np.pi

    return [np.rad2deg(lat2), np.rad2deg(lng2)]

def displaceLatLon(lat,lon,bearing,distance):
    #Planar formula for short distance
    bearing = np.deg2rad(bearing)
    dx = distance * sin(bearing)
    dy = distance * cos(bearing)
    delta_lon = dx/(111320*cos(np.deg2rad(lat)))
    delta_lat = dy/110540
    final_lon = lon + delta_lon
    final_lat = lat + delta_lat
    
    return final_lat,final_lon


def autonomousController(drone,destinationLat,destinationLon):
    droneSpeed = 1 / 5
    flightEnd = False
    while not flightEnd:
        # Receive Current GPS Coordinates
        while get_coordinates('Get GPS coordinate\r\n') == (None,None):
            print "waiting for GPS fix"

        currentLat,currentLon = get_coordinates('Get GPS coordinate\r\n')
#        currentLat = 0
#        currentLon = 0

        print "Current Latitude: ", currentLat
        print "Current Longitude: ", currentLon 
        print "Current Signal Strength: ", signalStrength.main()

        flightDistance = haversine(currentLon, currentLat, destinationLon, destinationLat)
        print "Flight distance: " + str(flightDistance)
        flightBearing = gpsBearing(currentLon, currentLat, destinationLon, destinationLat)
        print "Flight bearing: " + str(flightBearing)
            
        flightController(drone,flightBearing,droneSpeed)

        if abs(flightDistance) <= 1 or drone.getKey():
                flightEnd = True

    drone.stop()
    
if __name__ == '__main__':
    # Drone Startup Sequence
    drone = ps_drone.Drone()
    drone.startup()
    drone.reset()
    while (drone.getBattery()[0] == -1): time.sleep(0.1)
    print "Battery: " + str(drone.getBattery()[0]) + "%  " + str(drone.getBattery()[1])
    drone.useDemoMode(False)
    drone.getNDpackage(["demo"])
    time.sleep(1.0)
    drone.trim()
    drone.getSelfRotation(10)

    # Initialise lists to store signal strength and coordinates data
    ssList   = []
    latList  = []
    lonList  = []

    try:
        # Retrieve 4G signal strength
        initialSignalStrength = signalStrength.main()
        print "Initial Signal Strength: ", initialSignalStrength
        ssList.append(initialSignalStrength)
        
        # Retrieve Initial Coordinates
        while get_coordinates('Get GPS coordinate\r\n') == (None,None):
            print "waiting for GPS fix"

        initialLat,initialLon = get_coordinates('Get GPS coordinate\r\n')
        print initialLat,initialLon

#        initialLat = 0
#        initialLon = 0
        lonList.append(initialLon)
        latList.append(initialLat)

        # Calculate 3 additional coordinates 10m away
        flightRadius = 10
        destBearing = 360/3

        for i in range(3):
            dest = displaceLatLon(initialLat,initialLon,i*destBearing,flightRadius)
            latList.append(dest[0])
            lonList.append(dest[1])

        print "Latitudes: ", latList
        print "Longitudes: ", lonList

        # Begin flight sequence
        drone.takeoff()
        while drone.NavData["demo"][0][2]:  time.sleep(0.1)

        # Fly to the pre-determined destinations and measure signal strengths
        for i in range(1,4):
            print "Destination Coordinates: ", latList[i], lonList[i]
            autonomousController(drone, latList[i], lonList[i])
            ssList.append(signalStrength.main()) #TODO: check if ss is None

        print "Signal Strengths: ", ssList
        
        # Compute optimal destination
        optimalLat = 0
        optimalLon = 0
        for i in range(4):
            weighting = ssList[i]/sum(ssList)
            optimalLat = optimalLat + weighting*latList[i]
            optimalLon = optimalLon + weighting*lonList[i]

        print "Optimal Destination: ", optimalLat, optimalLon

        # Fly to the optimised destination
        autonomousController(drone, optimalLat, optimalLon)
        print "Final signal strength" + signalStrength.main()


    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
        print "\nLanding..."
        drone.stop()
        drone.land()

    print "Done.\nExiting."

