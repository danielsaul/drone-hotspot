import unittest
import mock
from drone_control.utils import *

class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_distanceBetweenPoints(self):
        a = {'latitude': 0.0, 'longitude': 0.0}
        b = {'latitude': 0.0, 'longitude': 0.0}
        should_be = 0.0
        result = distanceBetweenPoints(a, b)
        self.assertAlmostEqual(result, should_be, 1)

        a = {'latitude': 0.0, 'longitude': 0.0}
        b = {'latitude': 51.0, 'longitude': 1.0}
        should_be = 5671726.98
        result = distanceBetweenPoints(a, b)
        self.assertAlmostEqual(result, should_be, 1)

        a = {'latitude': 0.0, 'longitude': 0.0}
        b = {'latitude': -51.0, 'longitude': -1.0}
        should_be = 5671726.98
        result = distanceBetweenPoints(a, b)
        self.assertAlmostEqual(result, should_be, 1)

        a = {'latitude': 52.3, 'longitude': -0.5}
        b = {'latitude': 52.7, 'longitude': 0.1}
        should_be = 60231.17
        result = distanceBetweenPoints(a, b)
        self.assertAlmostEqual(result, should_be, 1)

    def test_bearingBetweenPoints(self):
        a = {'latitude': 0.0, 'longitude': 0.0}
        b = {'latitude': 0.0, 'longitude': 0.0}
        should_be = 0.0
        result = bearingBetweenPoints(a, b)
        self.assertAlmostEqual(result, should_be, 1)

        a = {'latitude': 0.0, 'longitude': 0.0}
        b = {'latitude': 51.0, 'longitude': 1.0}
        should_be = 0.8
        result = bearingBetweenPoints(a, b)
        self.assertAlmostEqual(result, should_be, 1)

        a = {'latitude': 0.0, 'longitude': 0.0}
        b = {'latitude': -51.0, 'longitude': -1.0}
        should_be = 180.8
        result = bearingBetweenPoints(a, b)
        self.assertAlmostEqual(result, should_be, 1)

        a = {'latitude': 52.3, 'longitude': -0.5}
        b = {'latitude': 52.7, 'longitude': 0.1}
        should_be = 42.2
        result = bearingBetweenPoints(a, b)
        self.assertAlmostEqual(result, should_be, 1)
