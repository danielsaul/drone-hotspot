
class ControlState(object):
    def __init__(self):
        self.state = {}
        self.reset_state()

    def reset_state(self):
        self.state = {
            'mode': None,
            'location': {
                'latitude': None,
                'longitude': None
            },
            'manual': {
                'move': {
                    'x': None,
                    'y': None
                },
                'altitude': None,
                'yaw': None
            },
            'flytopoint': {
                'altitude': None,
                'location': None
            },
            'autonomous': None,
        }

    def update_state(self, new):
        noNewKeys = all([key in self.state for key in new.keys()])
        if noNewKeys:
            self.state.update(new)

    def update_location(self, new):
        self.state['location'].update(new)

    def update_manual(self, new):
        self.state['manual'].update(new)

    def update_flytopoint(self, new):
        self.state['flytopoint'].update(new)

    def set_mode(self, new):
        self.state['mode'] = new['mode']

    def get_state(self):
        if self.state['mode'] is None:
            raise ValueError('State has not been updated.')
            return
        return self.state


