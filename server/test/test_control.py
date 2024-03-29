import unittest
import sys
import mock
from datetime import datetime
from drone_control.control import Control


class TestControlQueue(unittest.TestCase):
    def setUp(self):
        pipe = mock.Mock()
        dronestatedict = {}
        self.c = Control(dronestatedict, pipe)
        self.c.control_state = mock.MagicMock()
        self.c.drone_state = mock.MagicMock()
        self.c.drone = mock.MagicMock()
        self.c.modem = mock.MagicMock()

    @mock.patch.object(Control, 'startDrone')
    @mock.patch.object(Control, 'loop')
    @mock.patch.object(Control, 'consumeControlQueue')
    @mock.patch('time.sleep')
    def test_start(self, sleep, cq, loop, start):
        self.c.drone_connected = False
        def setTrue(): self.c.drone_connected = True
        start.side_effect = setTrue
        self.c.modem.start.return_value = True

        self.c.start()

        self.assertEquals(start.call_count, 1)
        loop.assert_called_once()
        self.c.modem.start.assert_called_once()
        self.c.modem.turnOnGPS.assert_called_once()
        self.assertEquals(self.c.modem_connected, True)

    def test_flyToPoint_nosetlocation(self):
        self.c.control_state.state = {
            'flytopoint': {
                'altitude': None,
                'location': None
            }
        }

        self.c.flyToPoint()

        self.c.drone.stop.assert_called_once()
        self.c.drone.move.assert_not_called()
        self.c.drone.turnAngle.assert_not_called()

    def test_flyToPoint_nogpslocation(self):
        self.c.control_state.state = {
            'flytopoint': {
                'altitude': 5,
                'location': {
                    'latitude': 51.0,
                    'longitude': -0.1
                }
            }
        }
        self.c.drone_state.state = {
            'location': {
                'latitude': None,
                'longitude': None
            }
        }

        self.c.flyToPoint()

        self.c.drone.stop.assert_called_once()
        self.c.drone.move.assert_not_called()
        self.c.drone.turnAngle.assert_not_called()

    def test_flyToPoint_arrived(self):
        self.c.control_state.state = {
            'flytopoint': {
                'altitude': 5,
                'location': {
                    'latitude': 51.0,
                    'longitude': -0.1
                }
            }
        }
        self.c.drone_state.state = {
            'altitude': 4.8,
            'location': {
                'latitude': 51.00001,
                'longitude': -0.100001,
            }
        }

        self.c.flyToPoint()

        self.c.drone.stop.assert_called_once()
        self.c.drone.move.assert_not_called()
        self.c.drone.turnAngle.assert_not_called()

    def test_flyToPoint_turntobearingandmove(self):
        self.c.control_state.state = {
            'flytopoint': {
                'altitude': 5,
                'location': {
                    'latitude': 51.0,
                    'longitude': -0.1
                }
            }
        }
        self.c.drone_state.state = {
            'altitude': 1,
            'location': {
                'latitude': 51.01,
                'longitude': 0.1,
            }
        }
        self.c.drone.NavData = {
            "demo": [0, 0, [0, 0, 130]] # Current bearing = 130degs
        }
        
        expected_turn = 135.53

        self.c.flyToPoint()

        args, kwargs = self.c.drone.turnAngle.call_args
        self.assertAlmostEqual(args[0], expected_turn, 1)
        
        args, kwargs = self.c.drone.move.call_args
        self.assertEqual(args[0], 0.0)
        self.assertEqual(args[1], 1.0)
        self.assertEqual(args[2], 0.4)
        self.assertEqual(args[3], 0.0)

    def test_flyToPoint_turntobearingandmoveminus(self):
        self.c.control_state.state = {
            'flytopoint': {
                'altitude': 5,
                'location': {
                    'latitude': 52.564,
                    'longitude': -1.351
                }
            }
        }
        self.c.drone_state.state = {
            'altitude': 1,
            'location': {
                'latitude': 52.1,
                'longitude': -0.01,
            }
        }
        self.c.drone.NavData = {
            "demo": [0, 0, [0, 0, 340]] # Current bearing = 340degs
        }
        
        expected_turn = -40.0

        self.c.flyToPoint()

        args, kwargs = self.c.drone.turnAngle.call_args
        self.assertAlmostEqual(args[0], expected_turn, 0)
        
        args, kwargs = self.c.drone.move.call_args
        self.assertEqual(args[0], 0.0)
        self.assertEqual(args[1], 1.0)
        self.assertEqual(args[2], 0.4)
        self.assertEqual(args[3], 0.0)    
        
    def test_flyManual_allzero(self):
        self.c.control_state.state = {
            'manual': {
                'move': {
                    'x': 0.0,
                    'y': 0.0
                },
                'altitude': 0.0,
                'yaw': 0.0
            }
        }

        self.c.flyManual()

        self.c.drone.stop.assert_called_once()
        self.c.drone.move.assert_not_called()

    def test_flyManual_move(self):
        self.c.control_state.state = {
            'manual': {
                'move': {
                    'x': 0.4,
                    'y': 0.3
                },
                'altitude': 0.2,
                'yaw': 0.1
            }
        }

        self.c.flyManual()

        self.c.drone.stop.assert_not_called()
        self.c.drone.move.assert_called_once_with(0.4, 0.3, 0.2, 0.1)

    @mock.patch('drone_control.control.utils.distanceBetweenPoints')
    def test_getDistance_noapplocation(self, d):
        self.c.control_state.state.__getitem__.return_value = {
            'latitude': None,
            'longitude': None
        }
        self.c.drone_state.state.__getitem__.return_value = {
            'latitude': 50.0,
            'longitude': -0.1
        }

        self.c.getDistance()

        d.assert_not_called()
        self.c.drone_state.update_state.assert_not_called()

    @mock.patch('drone_control.control.utils.distanceBetweenPoints')
    def test_getDistance_nodronelocation(self, d):
        self.c.control_state.state.__getitem__.return_value = {
            'latitude': 50.0,
            'longitude': -0.1
        }
        self.c.drone_state.state.__getitem__.return_value = {
            'latitude': None,
            'longitude': None
        }

        self.c.getDistance()

        d.assert_not_called()
        self.c.drone_state.update_state.assert_not_called()

    @mock.patch('drone_control.control.utils.distanceBetweenPoints')
    def test_getDistance_success(self, d):
        self.c.control_state.state.__getitem__.return_value = {
            'latitude': 50.0,
            'longitude': -0.1
        }
        self.c.drone_state.state.__getitem__.return_value = {
            'latitude': 25.0,
            'longitude': 5.0
        }
        d.return_value = 50.0

        self.c.getDistance()

        d.assert_called_once()
        self.c.drone_state.update_state.assert_called_once_with({'distance': 50.0})

    def test_getSignal_modemnotconnected(self):
        self.c.modem_connected = False

        self.c.getSignal()

        self.c.modem.getSignalStrength.assert_not_called()
        self.c.drone_state.update_state.assert_not_called()

    def test_getSignal_none(self):
        self.c.modem_connected = True
        self.c.modem.getSignalStrength.return_value = None

        self.c.getSignal()

        self.c.modem.getSignalStrength.assert_called_once()
        self.c.drone_state.update_state.assert_not_called()

    def test_getSignal_success(self):
        self.c.modem_connected = True
        self.c.modem.getSignalStrength.return_value = -113.0
        newstate = {
            'signal': -113.0
        }

        self.c.getSignal()

        self.c.modem.getSignalStrength.assert_called_once()
        self.c.drone_state.update_state.assert_called_once_with(newstate)

    def test_getGPS_modemnotconnected(self):
        self.c.modem_connected = False

        self.c.getGPS()

        self.c.modem.getGPSCoordinates.assert_not_called()
        self.c.drone_state.update_state.assert_not_called()

    def test_getGPS_none(self):
        self.c.modem_connected = True
        self.c.modem.getGPSCoordinates.return_value = None

        self.c.getGPS()

        self.c.modem.getGPSCoordinates.assert_called_once()
        self.c.drone_state.update_state.assert_not_called()

    def test_getGPS_success(self):
        self.c.modem_connected = True
        self.c.modem.getGPSCoordinates.return_value = (50.0,-1.0)
        newstate = {
            'location': {
                'latitude': 50.0,
                'longitude': -1.0
            }
        }

        self.c.getGPS()

        self.c.modem.getGPSCoordinates.assert_called_once()
        self.c.drone_state.update_state.assert_called_once_with(newstate)

    def test_getDroneData_old(self):
        self.c.prev_data_count = 10
        self.c.drone.NavDataCount = 10

        self.c.getDroneData()

        self.c.drone_state.update_state.assert_not_called()

    def test_getDroneData_new(self):
        self.c.prev_data_count = 10
        self.c.drone.NavDataCount = 11

        self.c.getDroneData()

        self.assertEquals(self.c.prev_data_count, self.c.drone.NavDataCount)
        self.c.drone_state.update_state.assert_called_once()

    def test_connectionCheck_true(self):
        self.c.app_connected = True
        result = self.c.connectionCheck()
        self.assertEquals(result, True)
        self.assertIs(self.c.app_disconnected_timer, None)
        self.c.drone.stop.assert_not_called()

    def test_connectionCheck_false(self):
        self.c.app_connected = False
        self.c.drone_state.state.__getitem__.return_value = "flying"
        result = self.c.connectionCheck()
        self.assertEquals(result, False)
        self.assertIsNot(self.c.app_disconnected_timer, None)
        self.c.drone.stop.assert_called_once()
        self.c.drone.land.assert_not_called()

    @mock.patch('drone_control.control.datetime.datetime')
    def test_connectionCheck_falsetimer(self, dt):
        dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
        self.c.app_connected = False
        self.c.drone_state.state.__getitem__.return_value = "flying"
        self.c.app_disconnected_timer = datetime(2018, 2, 1, 12, 30, 00)
        dt.now.return_value = datetime(2018, 2, 1, 12, 31, 30) #1.5 mins

        result = self.c.connectionCheck()

        self.assertEquals(result, False)
        self.c.drone.stop.assert_called_once()
        self.c.drone.land.assert_not_called()

    @mock.patch('drone_control.control.datetime.datetime')
    def test_connectionCheck_falsetimerland(self, dt):
        dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
        self.c.app_connected = False
        self.c.drone_state.state.__getitem__.return_value = "flying"
        self.c.app_disconnected_timer = datetime(2018, 2, 1, 12, 30, 00)
        dt.now.return_value = datetime(2018, 2, 1, 12, 32, 30) #2.5 mins

        result = self.c.connectionCheck()

        self.assertEquals(result, False)
        self.c.drone.stop.assert_called_once()
        self.c.drone.land.assert_called_once()

    def test_connectionCheck_truetimerreset(self):
        self.c.app_connected = True
        self.c.drone_state.state.__getitem__.return_value = "flying"
        self.c.app_disconnected_timer = datetime(2018, 2, 1, 12, 30, 00)

        result = self.c.connectionCheck()

        self.assertEquals(result, True)
        self.assertIs(self.c.app_disconnected_timer, None)
        self.c.drone.stop.assert_not_called()
        self.c.drone.land.assert_not_called()

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
        self.c.drone.setConfig.assert_called_once()
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
        self.c.drone_connected = True
        self.c.drone_state.state.__getitem__.return_value = "waiting"
        self.c.processAction('takeoff')
        takeoff.assert_called_once()

    @mock.patch.object(Control, 'takeoffDrone')
    def test_processAction_takeoffflying(self, takeoff):
        self.c.drone_connected = True
        self.c.drone_state.state.__getitem__.return_value = "flying"
        self.c.processAction('takeoff')
        takeoff.assert_not_called()

    def test_processAction_land(self):
        self.c.drone_connected = True
        self.c.drone_state.state.__getitem__.return_value = "flying"
        self.c.processAction('land')
        self.c.drone.land.assert_called_once()

    def test_processAction_landwaiting(self):
        self.c.drone_connected = True
        self.c.drone_state.state.__getitem__.return_value = "waiting"
        self.c.processAction('land')
        self.c.drone.land.assert_not_called()

    def test_processAction_return(self):
        self.c.drone_connected = True
        self.c.drone_state.state.__getitem__.return_value = "flying"
        self.c.processAction('return')
        self.assertEquals(self.c.returning, True)

    def test_processAction_returnwaiting(self):
        self.c.drone_connected = True
        self.c.drone_state.state.__getitem__.return_value = "waiting"
        self.c.processAction('return')
        self.assertEquals(self.c.returning, False)

    def test_processAction_abort(self):
        self.c.drone_connected = True
        self.c.drone_state.state.__getitem__.return_value = "flying"
        self.c.processAction('abort')
        self.c.drone.reset.assert_called_once()

    def test_processAction_abortwaiting(self):
        self.c.drone_connected = True
        self.c.drone_state.state.__getitem__.return_value = "waiting"
        self.c.processAction('abort')
        self.c.drone.reset.assert_not_called()
