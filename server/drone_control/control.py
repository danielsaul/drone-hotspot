import time
import ps_drone
from controlstate import ControlState

class Control(object):
    def __init__(self, pipe):
        self.pipe = pipe
        self.drone = ps_drone.Drone()

        self.control_state = ControlState()
        self.app_connected = False
        self.drone_connected = False
        self.drone_calibrated = False

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

        self.drone_connected = True

    def takeoffDrone(self):
        if not self.drone_calibrated:
            # Calibrate level and gyro
            self.drone.trim()
            self.drone.getSelfRotation(5)

        self.drone.takeoff()

        while self.drone.NavData["demo"][0][2]:
            time.sleep(0.1)

        if not self.drone_calibrated:
            # Calibrate magnetometer
            self.drone.mtrim()
            self.drone_calibrated = True

    def consumeControlQueue(self):
        action = None

        while self.pipe.poll(): 
            cmd, data = self.pipe.recv()
            if cmd == 'connected':
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

        if action:
            self.processAction(action)

    def processAction(self):
        pass
