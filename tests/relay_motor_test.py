import unittest
import time

import logging

from dora.motor.relaymotor import RelayMotor


class TestRelayMotor(unittest.TestCase):
    on = 0
    off = 0
    onTime = 0
    offTime = 0

    def setUp(self):
        self.lastTime = time.time()
        self.motor = RelayMotor(self.countOn, self.countOff)
        logging.getLogger().setLevel(logging.DEBUG)

    def countOn(self):
        self.on += 1
        self.offTime += time.time() - self.lastTime
        self.lastTime = time.time()

    def countOff(self):
        self.off += 1
        self.onTime += time.time() - self.lastTime
        self.lastTime = time.time()

    def test_init(self):
        self.assertEqual(self.motor.throttle, 0)
        self.assertEqual(self.on, 0)
        self.assertEqual(self.off, 0)

    def test_shape(self):
        precision = 5
        cycles = 3
        throttle = .2
        self.motor = RelayMotor(self.countOn, self.countOff, .05)
        self.assertEqual(self.on, 0)
        self.assertEqual(self.off, 0)
        self.motor.set_throttle(throttle)
        time.sleep(self.motor.period / precision / 2.0)
        for c in range(cycles):
            for i in range(precision):
                self.assertEquals(self.on, c + 1)
                if float(i) / precision < throttle:
                    self.assertEquals(self.off, c)
                else:
                    self.assertEquals(self.off, c + 1)
                time.sleep(self.motor.period / precision)

    def test_distribution(self):
        cycles = 100
        throttle = .30008
        delta = .5
        self.motor = RelayMotor(self.countOn, self.countOff, .01)
        self.assertEqual(self.on, 0)
        self.assertEqual(self.off, 0)
        self.motor.set_throttle(throttle)
        time.sleep(self.motor.period * cycles)
        total_time = self.onTime + self.offTime
        on_percent = self.onTime / total_time
        print "delta: {0}".format((on_percent - throttle))
        self.assertGreaterEqual(on_percent, throttle - delta)
        self.assertLessEqual(on_percent, throttle + delta)
