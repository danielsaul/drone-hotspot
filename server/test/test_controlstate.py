import unittest
from drone_control.controlstate import ControlState

class TestControlState(unittest.TestCase):
    def setUp(self):
        self.func = ControlState()

    def test_initial_state(self):
        state = {
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
        self.assertEqual(self.func.state, state)

    def test_reset_state(self):
        state = {
            'mode': 'manual',
            'location': {
                'latitude': 0.04324,
                'longitude': 53535.00
            },
            'manual': {
                'move': {
                    'x': 353,
                    'y': 535
                },
                'altitude': 355,
                'yaw': 3535
            },
            'flytopoint': {
                'altitude': 3535,
                'location': 35
            },
            'autonomous': None,
        }
        self.func.state = state
        self.assertEqual(self.func.state, state)
        self.func.reset_state()
        self.test_initial_state()

    def test_update_withnothing(self):
        prev = self.func.state.copy()
        self.func.update_state({})
        self.assertEqual(self.func.state, prev)

    def test_no_update_withnewkeys(self):
        prev = self.func.state.copy()
        self.func.update_state({'newkey': 0, 'mode': 'test'})
        self.assertEqual(self.func.state, prev)

    def test_update_withexistingkeys(self):
        prev = self.func.state.copy()
        self.func.update_state({'mode': 'test', 'manual': {}})
        self.assertNotEqual(prev, self.func.state)
        self.assertEqual(self.func.state['mode'], 'test')
        self.assertEqual(self.func.state['manual'], {})
        self.assertEqual(self.func.state['flytopoint'], prev['flytopoint'])

    def test_get_whennotready(self):
        self.assertRaises(ValueError, self.func.get_state)

    def test_get_whenready(self):
        self.func.state['mode'] = 'manual'
        state = self.func.get_state()
        self.assertEqual(self.func.state, state)


if __name__ == '__main__':
    unittest.main()
