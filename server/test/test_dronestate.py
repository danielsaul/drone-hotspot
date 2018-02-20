import unittest
from drone_control.dronestate import DroneState

class TestDroneState(unittest.TestCase):
    def setUp(self):
        self.func = DroneState()

    def test_true(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
