import unittest
from drone_control.dronestate import DroneState

class TestDroneState(unittest.TestCase):
    def setUp(self):
        self.func = DroneState()

    def test_initial_state(self):
        state = {
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
        self.assertEqual(self.func.state, state)

    def test_reset_state(self):
        state = {
            'status': "flying",
            'location': {
                'latitude': 0.003394,
                'longitude': 45345345.0,
            },
            'altitude': 323,
            'distance': 54,
            'speed': 234,
            'battery': 8,
            'signal': 4
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
        self.func.update_state({'newkey': 0, 'status': 'test'})
        self.assertEqual(self.func.state, prev)

    def test_update_withexistingkeys(self):
        prev = self.func.state.copy()
        self.func.update_state({'status': 'test', 'battery': 50})
        self.assertNotEqual(prev, self.func.state)
        self.assertEqual(self.func.state['status'], 'test')
        self.assertEqual(self.func.state['battery'], 50)
        self.assertEqual(self.func.state['altitude'], prev['altitude'])


if __name__ == '__main__':
    unittest.main()
