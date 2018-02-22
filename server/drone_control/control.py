import ps_drone

class Control(object):
    def __init__(self):
        self.pipe = None
        self.control_state = None
        self.app_connected = False
        self.drone = ps_drone.Drone()

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
