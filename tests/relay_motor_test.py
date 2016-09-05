import unittest
import time

from dora.motor.relaymotor import RelayMotor


class TestRelayMotor(unittest.TestCase):
    on = 0
    off = 0

    def setUp(self):
        self.motor = RelayMotor(self.countOn, self.countOff)
        pass

    def countOn(self):
        self.on += 1

    def countOff(self):
        self.off += 1

    def test_init(self):
        # self.assertEqual(self.motor.throttle,  0)
        time.sleep(2)
        self.assertEqual(self.on,  0)
        self.assertEqual(self.off,  0)
