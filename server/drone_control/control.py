import time
import datetime
import ps_drone
import ec25_modem
import utils
from controlstate import ControlState
from dronestate import DroneState

class Control(object):
    def __init__(self, drone_state_dict, pipe):
        self.pipe = pipe
        self.drone = ps_drone.Drone()
        self.modem = ec25_modem.Modem("/dev/ttyUSB3") 

        self.control_state = ControlState()
        self.drone_state = DroneState()
        self.drone_state_dict = drone_state_dict
        self.prev_data_count = 0
        self.app_connected = False
        self.app_disconnected_timer = None
        self.drone_connected = False
        self.drone_calibrated = False
        self.returning = False
        self.modem_connected = False

        self.running = True

    def start(self):
        # Connect to drone
        print "Waiting for drone"
        while not self.drone_connected:
            self.consumeControlQueue()
            self.startDrone()
            time.sleep(3)
        
        print "Drone connected."

        # Connect to modem
        self.modem_connected = self.modem.start()
        if self.modem_connected:
            print "Modem connected."
            self.modem.turnOnGPS()
        else:
            print "Modem *not* connected."

        # Enter control loop
        self.loop()

    def loop(self):
        while self.running:
            self.iteration()
            time.sleep(0.01)

    def iteration(self):

        # Consume control messages from socket/app
        self.consumeControlQueue()

        # Get latest drone data
        self.getDroneData()

        # If app is not connected
        if not self.connectionCheck():
            return

        # Get GPS location
        self.getGPS()

        # Get distance
        self.getDistance()

        # Get 4G Signal strength
        self.getSignal()
        
        # Send updated drone state to socket/app
        self.drone_state_dict.update(self.drone_state.state)

        # Drone is flying, instruct it
        if self.drone_state.state['status'] == 'flying':
            
            if self.returning:
                # TODO: Return to home functionality
                pass

            elif self.control_state.state['mode'] == 'manual':
                # Manual control
                self.flyManual()

            elif self.control_state.state['mode'] == 'flytopoint':
                self.flyToPoint()
                pass

            elif self.control_state.state['mode'] == 'autonomous':
                # TODO: Autonomous
                pass

    def flyToPoint(self):
        ftp = self.control_state.state['flytopoint']
        drone_loc = self.drone_state.state['location']
        if not ftp['location'] or not ftp['altitude'] or not drone_loc['latitude']:
            self.drone.stop()
            return

        distance = utils.distanceBetweenPoints(drone_loc, ftp['location'])
        altitude = ftp['altitude'] - (self.drone_state.state['altitude'])
        if distance <= 3 and altitude <= 1:
            self.drone.stop()
            return

        # Turn to correct bearing
        current_bearing = self.drone.NavData["demo"][2][2]
        current_bearing = (current_bearing + 360) % 360
        target_bearing = utils.bearingBetweenPoints(drone_loc, ftp['location'])
        angle = target_bearing - current_bearing
        if angle > 180:
            angle -= 360
        elif angle < -180:
            angle += 180
        self.drone.turnAngle(angle, 1, 0.1)

        # Move forward and up at proportional speed
        forward_speed = max(min(distance/30.0, 1.0), 0.1)
        up_speed = max(min(altitude/10.0, 1.0), -1.0)
        self.drone.move(0.0, forward_speed, up_speed, 0.0)

    def flyManual(self):
        m = self.control_state.state['manual']
        
        if m['move']['x'] == 0.0 and m['move']['y'] == 0.0 and m['altitude'] == 0.0 and m['yaw'] == 0.0:
            self.drone.stop()
        else:
            self.drone.move(m['move']['x']/2, m['move']['y']/2, m['altitude']/2, m['yaw']/2)

    def getDistance(self):
        drone_loc = self.drone_state.state['location']
        app_loc = self.control_state.state['location']

        if not drone_loc['latitude'] or not app_loc['latitude']:
            return

        distance = {
            'distance': utils.distanceBetweenPoints(drone_loc, app_loc)
        }
        self.drone_state.update_state(distance)

    def getSignal(self):
        if not self.modem_connected:
            return

        res = self.modem.getSignalStrength()
        if res:
            signal = {
                'signal': res
            }
            self.drone_state.update_state(signal)

    def getGPS(self):
        if not self.modem_connected:
            return
        
        res = self.modem.getGPSCoordinates()
        if res:
            coords = {
                'location': {
                    'latitude': res[0],
                    'longitude': res[1]
                }
            }
            self.drone_state.update_state(coords)

    def getDroneData(self):
        n = self.drone.NavDataCount
        if self.prev_data_count >= n:
            return
        
        self.prev_data_count = n
        new = {}

        #if self.drone.NavData['demo'][0][2]:    # Landed/Waiting
        #    new['status'] = "waiting"
        #elif self.drone.NavData['demo'][0][3]:  # Flying
        #    new['status'] = "flying"
        #elif self.drone.NavData['demo'][0][4]:  # Landing
        #    new['status'] = "landing"
        
        if self.drone.State[0]:
            new['status'] = "flying"
        else:
            new['status'] = "waiting"

        new['battery'] = int(self.drone.NavData['demo'][1])
        new['altitude'] = round(self.drone.NavData['demo'][3] / 100, 2)
        new['speed'] = round(self.drone.NavData['demo'][4][0] / 1000, 2)

        self.drone_state.update_state(new)

    def connectionCheck(self):
        # If app not connected and flying, stop drone
        if not self.app_connected and self.drone_state.state['status'] == 'flying':
            self.drone.stop()
            if not self.app_disconnected_timer:
                self.app_disconnected_timer = datetime.datetime.now()
            elif self.app_disconnected_timer + datetime.timedelta(minutes = 2) < datetime.datetime.now():
                self.drone.land()
        else:
            self.app_disconnected_timer = None
                
        return self.app_connected

    def startDrone(self):
        try:
            self.drone.startup()
        except SystemExit:
            # Startup failed
            return

        self.drone.reset()

        # Wait for reset to complete
        i=0
        while self.drone.getBattery()[0] == -1:
            time.sleep(0.1)
            if i >= 20:
                # Been more than 2 seconds, give up
                self.drone.shutdown()
                return
            i+=1

        # Navdata x times per sec
        self.drone.useDemoMode(True)
        self.drone.getNDpackage(["demo"])

        # Set to outdoor mode
        self.drone.setConfig('control:outdoor', 'True') 

        self.drone_connected = True

    def takeoffDrone(self):
        if not self.drone_calibrated:
            # Calibrate level and gyro
            self.drone.trim()
            self.drone.getSelfRotation(5)

        self.drone.takeoff()

        # Wait for takeoff to complete
        while self.drone.NavData["demo"][0][2]:
            time.sleep(0.1)

        #if not self.drone_calibrated:
            # Calibrate magnetometer
        #    self.drone.mtrim()
        #    self.drone_calibrated = True

    def consumeControlQueue(self):
        action = None
        
        # Loop over messages from phone app
        while self.pipe.poll(): 
            cmd, data = self.pipe.recv()
            if cmd == 'connected':
                if data and not self.app_connected:
                    print "App Connected"
                elif not data and self.app_connected:
                    print "App Disconnected"
                self.app_connected = data
            if cmd == 'action':
                action = data
            if cmd == 'update_all':
                self.control_state.update_state(data)
            if cmd == 'update_location':
                self.control_state.update_location(data)
            if cmd == 'update_manual':
                self.control_state.update_manual(data)
            if cmd == 'update_flytopoint':
                self.control_state.update_flytopoint(data)
            if cmd == 'set_mode':
                self.control_state.set_mode(data)

        # Only perform the most recent action
        if action:
            self.processAction(action)

    def processAction(self, action):
        print "Action: " + action
        if not self.drone_connected:
            return

        if action == 'takeoff' and self.drone_state.state['status'] == 'waiting':
            self.takeoffDrone()
        if action == 'land' and self.drone_state.state['status'] == 'flying':
            self.drone.land()
        if action == 'return' and self.drone_state.state['status'] == 'flying':
            self.returning = True
        if action == 'abort' and self.drone_state.state['status'] == 'flying':
            drone.thrust(0,0,0,0)
            self.running = False

