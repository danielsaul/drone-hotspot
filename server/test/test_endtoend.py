import unittest
import mock

from multiprocessing import Process, Pipe, Manager
from socketIO_client import SocketIO

from drone_control import socket
from drone_control.control import Control


class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.manager = Manager()
        self.drone_state = self.manager.dict()
        self.socket_pipe, self.control_pipe = Pipe()

        self.socketproc = Process(target=socket.start, args=(self.drone_state, self.socket_pipe))
        self.socketproc.start()

        self.c = Control(self.drone_state, self.control_pipe)
        self.c.running = False

        self.sio = SocketIO('localhost', 8000)

        self.c.drone = mock.Mock()
        self.c.drone.getBattery.return_value = (100, 0)
        self.c.drone.NavData = {
            "demo": [
                [0, 0, 1, 0, 0], # default, init, landed, flying, landing
                100, # Battery
                [0.0]*3, 
                1.0, # Altitude
                [0.0]*3 # Speeds
            ]
        }
        def takeoff():
            self.c.drone.NavData["demo"][0] = [0, 0, 0, 1, 0]
        self.c.drone.takeoff.side_effect = takeoff
        def land():
            self.c.drone.NavData["demo"][0] = [0, 0, 0, 0, 1]
        self.c.drone.land.side_effect = land

        def navdatacountinc():
            return navdatacount.call_count+1
        navdatacount = mock.PropertyMock()
        type(self.c.drone).NavDataCount = navdatacount
        navdatacount.side_effect = navdatacountinc

        self.c.modem = mock.Mock()
        self.c.modem.start.return_value = True
        self.c.modem.getGPSCoordinates.return_value = (51.0, -0.1)
        self.c.modem.getSignalStrength.return_value = -10

    def test_startup_droneconnected(self):
        self.assertEqual(self.c.drone_connected, False)
        self.c.start()
        self.assertEqual(self.c.drone_connected, True)

    def test_startup_appconnected(self):
        self.assertEqual(self.c.app_connected, False)
        self.c.start()
        self.assertEqual(self.c.app_connected, True)

    def test_appdisconnects(self):
        self.c.start()
        self.c.iteration()
        self.sio.disconnect()
        self.c.iteration()
        self.assertEqual(self.c.app_connected, False)
    
    def test_takesoff(self):
        self.c.start()
        self.c.iteration()
        self.sio.emit('action', 'takeoff')
        self.sio.wait(seconds=1)
        self.c.iteration()
        self.assertEqual(self.c.drone_calibrated, True)
        self.assertEqual(self.c.drone_state.state['status'], 'flying')

    def test_appdisconnects_whileflying(self):
        self.c.start()
        self.c.iteration()
        self.sio.emit('action', 'takeoff')
        self.sio.wait(seconds=1)
        self.c.iteration()
        self.sio.disconnect()
        self.c.iteration()
        self.assertEqual(self.c.app_connected, False)
        self.c.drone.stop.assert_called()

    def test_receivedronedata(self):
        received_data = {}
        def on_updateDroneStatus(data):
            received_data.update(data)
        self.sio.on('updateDroneStatus', on_updateDroneStatus)
        self.c.start()
        self.c.iteration()
        self.sio.wait(seconds=1)
        self.assertNotEqual(received_data, {})

    def test_lands(self):
        self.c.start()
        self.c.iteration()
        self.sio.emit('action', 'takeoff')
        self.sio.wait(seconds=1)
        self.c.iteration()
        self.sio.emit('action', 'land')
        self.sio.wait(seconds=1)
        self.c.iteration()
        self.assertEqual(self.c.drone_state.state['status'], 'landing')

    def test_moves(self):
        self.c.start()
        self.c.iteration()
        self.sio.emit('action', 'takeoff')
        self.sio.wait(seconds=1)
        self.c.iteration()
        self.sio.emit('update_manual', {'move': {'x': 0.5, 'y': 0.2}})
        self.sio.wait(seconds=1)
        self.c.iteration()
        self.c.drone.move.assert_called_with(0.5, 0.2, 0.0, 0.0)

    def test_fliestopoint(self):
        self.c.start()
        self.c.iteration()
        self.sio.emit('set_mode', {'mode': 'flytopoint'})
        self.sio.emit('action', 'takeoff')
        self.sio.wait(seconds=1)
        self.c.iteration()
        self.sio.emit('update_flytopoint', {
            'altitude': 10,
            'location': { 'latitude': 52.0, 'longitude': 1.0}
            })
        self.sio.wait(seconds=1)
        self.c.iteration()
        self.c.drone.turnAngle.assert_called_once()
        self.c.drone.move.assert_called_once()
        self.c.modem.getGPSCoordinates.return_value = (52.0, 1.0)
        self.c.drone.NavData['demo'][3] = 10
        self.c.iteration()
        self.c.drone.stop.assert_called()

    def tearDown(self):
        self.socketproc.terminate()
        self.socketproc.join()
