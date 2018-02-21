import unittest
import mock
from drone_control.socket import *

from multiprocessing import Manager, Pipe

class TestSocket(unittest.TestCase):
    def setUp(self):
        pass

    def test_emitDroneStatus_WrongState(self):
        with self.assertRaises(ValueError):
            emit_drone_status({})
            emit_drone_status({'status': "test", altitude: 5})

    @mock.patch('socketio.Server.emit')
    def test_emitDroneStatus_CorrectState(self, emit):
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

        emit_drone_status(state)
        emit.assert_called_once_with('updateDroneStatus', state)
    
    @mock.patch('eventlet.wsgi.server')
    @mock.patch('socketio.Server.start_background_task')
    def test_start_background_loop(self, bg, server):
        manager = Manager()
        state = manager.dict()
        state['test'] = 'test'

        start(state, None)
        bg.assert_called_once_with(background_loop, state)
        server.assert_called_once()

    @mock.patch('drone_control.socket.pipe')
    def test_connect_sentoverpipe(self, pipe):
        connect(0, 0)
        pipe.send.assert_called_once_with(('connected', True))

    @mock.patch('drone_control.socket.pipe')
    def test_disconnect_sentoverpipe(self, pipe):
        disconnect(0)
        pipe.send.assert_called_once_with(('connected', False))

    @mock.patch('drone_control.socket.pipe')
    def test_action_sentoverpipe(self, pipe):
        action(0, 'takeoff')
        pipe.send.assert_called_once_with(('action', 'takeoff'))

    @mock.patch('drone_control.socket.pipe')
    def test_updateall_sentoverpipe(self, pipe):
        update_all(0, {'test': 'test'})
        pipe.send.assert_called_once_with(('update_all', {'test': 'test'}))

    @mock.patch('drone_control.socket.pipe')
    def test_updatelocation_sentoverpipe(self, pipe):
        update_location(0, {'test': 'test'})
        pipe.send.assert_called_once_with(('update_location', {'test': 'test'}))

    @mock.patch('drone_control.socket.pipe')
    def test_setmode_sentoverpipe(self, pipe):
        set_mode(0, {'test': 'test'})
        pipe.send.assert_called_once_with(('set_mode', {'test': 'test'}))

    @mock.patch('drone_control.socket.pipe')
    def test_updatemanual_sentoverpipe(self, pipe):
        update_manual(0, {'test': 'test'})
        pipe.send.assert_called_once_with(('update_manual', {'test': 'test'}))

    @mock.patch('drone_control.socket.pipe')
    def test_updateflytopoint_sentoverpipe(self, pipe):
        update_flytopoint(0, {'test': 'test'})
        pipe.send.assert_called_once_with(('update_flytopoint', {'test': 'test'}))









