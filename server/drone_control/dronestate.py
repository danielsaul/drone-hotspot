
class DroneState(object):
    def __init__(self):
        self.state = {}
        self.reset_state()

    def reset_state(self):
        self.state = {
            'status': "waiting",
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
