import unittest
import sys
import mock
from drone_control.control import Control


class TestControlQueue(unittest.TestCase):
    def setUp(self):
        pipe = mock.Mock()
        self.c = Control(pipe)
        self.c.control_state = mock.MagicMock()
        self.c.drone_state = mock.MagicMock()
        self.c.drone = mock.MagicMock()

    def test_startDrone_startupfail(self):
        self.c.drone.startup.side_effect = sys.exit
        
        self.c.startDrone()

        self.c.drone.reset.assert_not_called()
        self.assertEquals(self.c.drone_connected, False)

    @mock.patch('time.sleep')
    def test_startDrone_resetfail(self, sleep):
        self.c.drone.getBattery.side_effect = [(-1,0)]*50
       
        self.c.startDrone()

        self.assertEquals(sleep.call_count, 21)
        self.c.drone.useDemoMode.assert_not_called()
        self.assertEquals(self.c.drone_connected, False)

    @mock.patch('time.sleep')
    def test_startDrone_success(self, sleep):
        self.c.drone.getBattery.side_effect = [(-1,0)]*10 + [(1,100)]

        self.c.startDrone()

        self.assertEquals(sleep.call_count, 10)
        self.c.drone.useDemoMode.assert_called_once()
        self.c.drone.getNDpackage.assert_called_once()
        self.assertEquals(self.c.drone_connected, True)

    @mock.patch('time.sleep')
    def test_takeoffDrone_calib(self, sleep):
        self.c.drone.NavData.__getitem__.return_value = [(0,0, False)]
        
        self.c.takeoffDrone()

        self.c.drone.trim.assert_called_once()
        self.c.drone.getSelfRotation.assert_called_once()
        self.c.drone.mtrim.assert_called_once()
        self.assertEquals(self.c.drone_calibrated, True)

    @mock.patch('time.sleep')
    def test_takeoffDrone(self, sleep):
        self.c.drone.NavData.__getitem__.side_effect = [[(0,0, True)]]*5 + [[(0,0, False)]]
        
        self.c.takeoffDrone()

        self.c.drone.takeoff.assert_called_once()

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

    @mock.patch.object(Control, 'takeoffDrone')
    def test_processAction_takeoff(self, takeoff):
        self.c.drone_state.state.__getitem__.return_value = "waiting"
        self.c.processAction('takeoff')
        takeoff.assert_called_once()

    @mock.patch.object(Control, 'takeoffDrone')
    def test_processAction_takeoffflying(self, takeoff):
        self.c.drone_state.state.__getitem__.return_value = "flying"
        self.c.processAction('takeoff')
        takeoff.assert_not_called()

    def test_processAction_land(self):
        self.c.drone_state.state.__getitem__.return_value = "flying"
        self.c.processAction('land')
        self.c.drone.land.assert_called_once()

    def test_processAction_landwaiting(self):
        self.c.drone_state.state.__getitem__.return_value = "waiting"
        self.c.processAction('land')
        self.c.drone.land.assert_not_called()

    def test_processAction_return(self):
        self.c.drone_state.state.__getitem__.return_value = "flying"
        self.c.processAction('return')
        self.assertEquals(self.c.returning, True)

    def test_processAction_returnwaiting(self):
        self.c.drone_state.state.__getitem__.return_value = "waiting"
        self.c.processAction('return')
        self.assertEquals(self.c.returning, False)

    def test_processAction_abort(self):
        self.c.drone_state.state.__getitem__.return_value = "flying"
        self.c.processAction('abort')
        self.c.drone.reset.assert_called_once()

    def test_processAction_abortwaiting(self):
        self.c.drone_state.state.__getitem__.return_value = "waiting"
        self.c.processAction('abort')
        self.c.drone.reset.assert_not_called()
