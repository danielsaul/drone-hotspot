import unittest
import mock
from drone_control.control import Control

class TestControl(unittest.TestCase):
    def setUp(self):
        self.c = Control()

    @mock.patch.object(Control, 'pipe')
    def test_consumeControlQueue_Empty(self, pipe):
        pipe.poll.return_value = False

        self.c.consumeControlQueue()
        pipe.poll.assert_called_once()




