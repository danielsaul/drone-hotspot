import time
import datetime
import ps_drone
from controlstate import ControlState
from dronestate import DroneState

class Control(object):
    def __init__(self, drone_state_dict, pipe):
        self.pipe = pipe
        self.drone = ps_drone.Drone()

        self.control_state = ControlState()
        self.drone_state = DroneState()
        self.drone_state_dict = drone_state_dict
        self.prev_data_count = 0
        self.app_connected = False
        self.app_disconnected_timer = None
        self.drone_connected = False
        self.drone_calibrated = False
        self.returning = False

    def start(self):
        # Connect to drone
        print "Waiting for drone"
        while not self.drone_connected:
            self.startDrone()
            time.sleep(3)
        
        print "Drone connected."

        # Enter control loop
        self.loop()

    def loop(self):
        while True:
            self.iteration()

    def iteration(self):

        # Consume control messages from socket/app
        self.consumeControlQueue()

        # If app is not connected
        if not self.connectionCheck():
            return

        # Get latest drone data
        self.getDroneData()

        # TODO: Get GPS location
        # Update state with GPS and distance

        # TODO: Get 4G Signal strength
        
        # Send updated drone state to socket/app
        self.drone_state_dict.update(self.drone_state.state)

        # Drone is flying, instruct it
        if self.drone_state.state['status'] == 'flying':
            
            if returning:
                # TODO: Return to home functionality
                pass

            elif self.control_state.state['mode'] == 'manual':
                # Manual control
                self.flyManual()

            elif self.control_state.state['mode'] == 'flytopoint':
                # TODO: Fly to point
                pass

            elif self.control_state.state['mode'] == 'autonomous':
                # TODO: Autonomous
                pass

    def flyManual(self):
        m = self.control_state.state['manual']
        
        if m['move']['x'] == 0.0 and m['move']['y'] == 0.0 and m['altitude'] == 0.0 and m['yaw'] == 0.0:
            self.drone.stop()
        else:
            self.drone.move(m['move']['x'], m['move']['y'], m['altitude'], m['yaw'])

    def getDroneData(self):
        if self.prev_data_count >= self.drone.NavDataCount:
            return
        
        self.prev_data_count = self.drone.NavDataCount
        new = {}

        if self.drone.NavData['demo'][0][2]:    # Landed/Waiting
            new['status'] = "waiting"
        elif self.drone.NavData['demo'][0][3]:  # Flying
            new['status'] = "flying"
        elif self.drone.NavData['demo'][0][4]:  # Landing
            new['status'] = "landing"

        new['battery'] = self.drone.NavData['demo'][1]
        new['altitude'] = self.drone.NavData['demo'][3] / 100
        new['speed'] = self.drone.NavData['demo'][4][0] / 1000

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
                return
            i+=1

        # Navdata 200 times per sec
        self.drone.useDemoMode(False)
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

        if not self.drone_calibrated:
            # Calibrate magnetometer
            self.drone.mtrim()
            self.drone_calibrated = True

    def consumeControlQueue(self):
        action = None
        
        # Loop over messages from phone app
        while self.pipe.poll(): 
            cmd, data = self.pipe.recv()
            if cmd == 'connected':
                self.app_connected = data
                print "App Connected" if data else "App Disconnected"
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
        if action == 'takeoff' and self.drone_state.state['status'] == 'waiting':
            self.takeoffDrone()
        if action == 'land' and self.drone_state.state['status'] == 'flying':
            self.drone.land()
        if action == 'return' and self.drone_state.state['status'] == 'flying':
            self.returning = True
        if action == 'abort' and self.drone_state.state['status'] == 'flying':
            self.drone.reset()

