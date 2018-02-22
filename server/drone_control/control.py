import ps_drone
from controlstate import ControlState

class Control(object):
    def __init__(self, pipe):
        self.pipe = pipe
        self.drone = ps_drone.Drone()

        self.control_state = ControlState()
        self.app_connected = False

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
