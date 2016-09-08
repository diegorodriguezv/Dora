import unittest
import time
import logging

from dora.motor.bidirectionalmotor import BidirectionalMotor


class TestBidirectionalMotor(unittest.TestCase):
    up_on = 0
    up_off = 0
    down_on = 0
    down_off = 0
    up_on_time = 0
    up_off_time = 0
    down_on_time = 0
    down_off_time = 0

    def setUp(self):
        self.motor = BidirectionalMotor(self.up_on_func, self.up_off_func, self.down_on_func, self.down_off_func, .03)
        self.is_first = True
        logging.getLogger().setLevel(logging.DEBUG)

    def tearDown(self):
        self.motor.alive = False
        self.motor.control_thread.join()

    def up_on_func(self):
        now = time.time()
        if self.is_first:
            self.start_time = self.last_time = now
            self.is_first = False
        self.up_off_time += now - self.last_time
        self.last_time = now
        elapsed = now - self.start_time
        self.up_on += 1
        print "{:f} up_off: {:f} ".format(elapsed, self.up_off_time)

    def up_off_func(self):
        now = time.time()
        self.up_on_time += now - self.last_time
        self.last_time = now
        elapsed = now - self.start_time
        self.up_off += 1
        print "{:f} up_on: {:f} ".format(elapsed, self.up_on_time)

    def down_on_func(self):
        now = time.time()
        if self.is_first:
            self.start_time = self.last_time = now
            self.is_first = False
        self.down_off_time += now - self.last_time
        self.last_time = now
        elapsed = now - self.start_time
        self.down_on += 1
        print "{:f} down_off: {:f} ".format(elapsed, self.down_off_time)

    def down_off_func(self):
        now = time.time()
        self.down_on_time += now - self.last_time
        self.last_time = now
        elapsed = now - self.start_time
        self.down_off += 1
        print "{:f} down_on: {:f} ".format(elapsed, self.down_on_time)

    def test_init(self):
        self.assertEqual(self.motor.throttle, 0)
        self.assertEqual(self.up_on, 0)
        self.assertEqual(self.up_off, 0)
        self.assertEqual(self.down_on, 0)
        self.assertEqual(self.down_off, 0)

    def test_distribution(self, throttle=.0):
        now = time.time()
        self.start_time = self.last_time = now
        elapsed = now - self.start_time
        print "{:f} start throttle: {:f} ".format(elapsed, throttle)
        cycles = 5
        delta = 5 / 100.0
        self.assertEqual(self.up_on, 0)
        self.assertEqual(self.up_off, 0)
        self.assertEqual(self.down_on, 0)
        self.assertEqual(self.down_off, 0)
        self.motor.set_throttle(throttle)
        time.sleep((cycles + 1) * self.motor.period)
        if throttle == 0:
            now = time.time()
            elapsed = now - self.start_time
            print "{:f} finish throttle: {:f} on: {} of: {} ont: {:f} oft: {:f} tt: {:f} real: {:f} " \
                .format(elapsed, throttle, self.up_on, self.up_off, self.up_on_time, self.up_off_time,
                        self.up_on_time + self.up_off_time,
                        0)
            self.assertEqual(self.up_on, 0)
            self.assertEqual(self.up_off, 0)
            self.assertEqual(self.down_on, 0)
            self.assertEqual(self.down_off, 0)
        elif throttle > 0:
            now = time.time()
            if self.up_off == self.up_on:
                self.up_off_time += now - self.last_time
            else:
                self.up_on_time += now - self.last_time
            total_time = self.up_on_time + self.up_off_time
            self.assertTrue(total_time != 0)
            on_rate = self.up_on_time / total_time
            elapsed = now - self.start_time
            print "{:f} finish throttle: {:f} on: {} of: {} ont: {:f} oft: {:f} tt: {} real: {} " \
                .format(elapsed, throttle, self.up_on, self.up_off, self.up_on_time, self.up_off_time,
                        self.up_on_time + self.up_off_time,
                        on_rate)
            self.assertGreaterEqual(on_rate, throttle - delta)
            self.assertLessEqual(on_rate, throttle + delta)
            self.assertEqual(self.down_on, 0)
            self.assertEqual(self.down_off, 0)
        else:
            now = time.time()
            if self.down_off == self.down_on:
                self.down_off_time += now - self.last_time
            else:
                self.down_on_time += now - self.last_time
            total_time = self.down_on_time + self.down_off_time
            self.assertTrue(total_time != 0)
            on_rate = self.down_on_time / total_time
            elapsed = now - self.start_time
            print "{:f} finish throttle: {:f} on: {} of: {} ont: {:f} oft: {:f} tt: {} real: {} " \
                .format(elapsed, throttle, self.down_on, self.down_off, self.down_on_time, self.down_off_time,
                        self.down_on_time + self.down_off_time,
                        on_rate)
            self.assertGreaterEqual(on_rate, -throttle - delta)
            self.assertLessEqual(on_rate, -throttle + delta)
            self.assertEqual(self.up_on, 0)
            self.assertEqual(self.up_off, 0)

    def test_distribution_005(self):
        throttle = 5 / 100.0
        self.test_distribution(throttle)

    def test_distribution_010(self):
        throttle = 10 / 100.0
        self.test_distribution(throttle)

    def test_distribution_020(self):
        throttle = 20 / 100.0
        self.test_distribution(throttle)

    def test_distribution_025(self):
        throttle = 25 / 100.0
        self.test_distribution(throttle)

    def test_distribution_0333(self):
        throttle = 33.3333333 / 100.0
        self.test_distribution(throttle)

    def test_distribution_050(self):
        throttle = 50 / 100.0
        self.test_distribution(throttle)

    def test_distribution_080(self):
        throttle = 80 / 100.0
        self.test_distribution(throttle)

    def test_distribution_090(self):
        throttle = 90 / 100.0
        self.test_distribution(throttle)

    def test_distribution_095(self):
        throttle = 95 / 100.0
        self.test_distribution(throttle)

    def test_distribution_100(self):
        throttle = 100 / 100.0
        self.test_distribution(throttle)

    def test_distribution__005(self):
        throttle = -5 / 100.0
        self.test_distribution(throttle)

    def test_distribution__010(self):
        throttle = -10 / 100.0
        self.test_distribution(throttle)

    def test_distribution__020(self):
        throttle = -20 / 100.0
        self.test_distribution(throttle)

    def test_distribution__025(self):
        throttle = -25 / 100.0
        self.test_distribution(throttle)

    def test_distribution__0333(self):
        throttle = -33.3333333 / 100.0
        self.test_distribution(throttle)

    def test_distribution__050(self):
        throttle = -50 / 100.0
        self.test_distribution(throttle)

    def test_distribution__080(self):
        throttle = -80 / 100.0
        self.test_distribution(throttle)

    def test_distribution__090(self):
        throttle = -90 / 100.0
        self.test_distribution(throttle)

    def test_distribution__095(self):
        throttle = -95 / 100.0
        self.test_distribution(throttle)

    def test_distribution__100(self):
        throttle = -100 / 100.0
        self.test_distribution(throttle)
