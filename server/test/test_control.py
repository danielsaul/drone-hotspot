import unittest
import mock
from drone_control.control import Control


class TestControlQueue(unittest.TestCase):
    def setUp(self):
        pipe = mock.Mock()
        self.c = Control(pipe)
        self.c.control_state = mock.Mock()
        self.c.drone = mock.Mock()

    def test_consumeControlQueue_Empty(self):
        self.c.pipe.poll.return_value = False

        self.c.consumeControlQueue()

        self.c.pipe.poll.assert_called_once()

    @mock.patch.object(Control, 'processAction')
    def test_consumeControlQueue_Connection(self, action):
        self.c.pipe.poll.side_effect = [True, False]
        self.c.pipe.recv.side_effect = [('connected', True)]

        self.c.consumeControlQueue()

        self.assertEquals(self.c.app_connected, True)

        self.c.pipe.poll.side_effect = [True, False]
        self.c.pipe.recv.side_effect = [('connected', False)]

        self.c.consumeControlQueue()

        self.assertEquals(self.c.app_connected, False)

    @mock.patch.object(Control, 'processAction')
    def test_consumeControlQueue(self, action):
        msgs = [
            ('action', 'takeoff'),
            ('action', 'abort'),
            ('action', 'land'),
            ('update_all', 1),
            ('update_location', 1),
            ('update_manual', 1),
            ('update_flytopoint', 1),
            ('set_mode', 1),
        ]
        n = len(msgs)

        self.c.pipe.poll.side_effect = [True]*n + [False]*2
        self.c.pipe.recv.side_effect = msgs

        self.c.consumeControlQueue()

        self.assertEquals(self.c.pipe.poll.call_count, n+1)
        self.assertEquals(self.c.pipe.recv.call_count, n)

        action.assert_called_once_with('land')
        self.c.control_state.update_state.assert_called_once_with(1)
        self.c.control_state.update_location.assert_called_once_with(1)
        self.c.control_state.update_manual.assert_called_once_with(1)
        self.c.control_state.update_flytopoint.assert_called_once_with(1)
        self.c.control_state.set_mode.assert_called_once_with(1)




