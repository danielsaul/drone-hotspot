import unittest
import copy
from drone_control.controlstate import ControlState

class TestControlState(unittest.TestCase):
    def setUp(self):
        self.func = ControlState()

    def test_initial_state(self):
        state = {
            'mode': 'manual',
            'location': {
                'latitude': None,
                'longitude': None
            },
            'manual': {
                'move': {
                    'x': 0.0,
                    'y': 0.0
                },
                'altitude': 0.0,
                'yaw': 0.0
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
        prev = copy.deepcopy(self.func.state)
        self.func.update_state({})
        self.assertEqual(self.func.state, prev)

    def test_no_update_withnewkeys(self):
        prev = copy.deepcopy(self.func.state)
        self.func.update_state({'newkey': 0, 'mode': 'test'})
        self.assertEqual(self.func.state, prev)

    def test_update_withexistingkeys(self):
        prev = copy.deepcopy(self.func.state)
        self.func.update_state({'mode': 'test', 'manual': {}})
        self.assertNotEqual(prev, self.func.state)
        self.assertEqual(self.func.state['mode'], 'test')
        self.assertEqual(self.func.state['manual'], {})
        self.assertEqual(self.func.state['flytopoint'], prev['flytopoint'])

    def test_update_location(self):
        prev = copy.deepcopy(self.func.state)
        self.func.update_location({'latitude': 5, 'longitude': 10})
        self.assertNotEqual(prev, self.func.state)
        self.assertEqual(self.func.state['location']['latitude'], 5)
        self.assertEqual(self.func.state['location']['longitude'], 10)
        self.assertEqual(self.func.state['flytopoint'], prev['flytopoint'])

    def test_update_manual(self):
        prev = copy.deepcopy(self.func.state)
        self.func.update_manual({'move': {'x': 1, 'y': 1}})
        self.assertNotEqual(prev, self.func.state)
        self.assertEqual(self.func.state['manual']['move'], {'x':1, 'y':1})
        self.assertEqual(self.func.state['manual']['altitude'], prev['manual']['altitude'])
        self.assertEqual(self.func.state['manual']['yaw'], prev['manual']['yaw'])
        self.assertEqual(self.func.state['flytopoint'], prev['flytopoint'])

    def test_update_flytopoint(self):
        prev = copy.deepcopy(self.func.state)
        self.func.update_flytopoint({'location': {'latitude': 1, 'longitude': 1}})
        self.assertNotEqual(prev, self.func.state)
        self.assertEqual(self.func.state['flytopoint']['location'], {'latitude':1, 'longitude':1})
        self.assertEqual(self.func.state['flytopoint']['altitude'], prev['flytopoint']['altitude'])
        self.assertEqual(self.func.state['manual'], prev['manual'])

    def test_set_mode(self):
        prev = copy.deepcopy(self.func.state)
        self.func.set_mode({'mode': 'flytopoint'})
        self.assertEqual(self.func.state['mode'], 'flytopoint')
        self.assertEqual(self.func.state['manual'], prev['manual'])

    def test_get_whenready(self):
        self.func.state['mode'] = 'manual'
        state = self.func.get_state()
        self.assertEqual(self.func.state, state)


if __name__ == '__main__':
    unittest.main()
