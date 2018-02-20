
class DroneState(object):
    def __init__(self):
        self.state = {}
        self.reset_state()

    def reset_state(self):
        self.state = {
            'status': None,
            'location': {
                'latitude': None,
                'longitude': None
            },
            'altitude': None,
            'distance': None,
            'speed': None,
            'battery': None,
            'signal': None
        }

    def update_state(self, new):
        noNewKeys = all([key in self.state for key in new.keys()])
        if noNewKeys:
            self.state.update(new)

    def get_state(self):
        pass
