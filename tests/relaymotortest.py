import unittest
import time
import logging

from dora.motor.relaymotor import RelayMotor


class TestRelayMotor(unittest.TestCase):
    on = 0
    off = 0
    on_time = 0.0
    off_time = 0.0

    def setUp(self):
        self.motor = RelayMotor(self.count_on, self.count_off, .03)
        self.is_first = True
        logging.getLogger().setLevel(logging.DEBUG)

    def tearDown(self):
        self.motor.alive = False
        self.motor.control_thread.join()

    def count_on(self):
        now = time.time()
        if self.is_first:
            self.start_time = self.last_time = now
            self.is_first = False
        self.off_time += now - self.last_time
        self.last_time = now
        elapsed = now - self.start_time
        self.on += 1
        # print "{:f} off: {:f} ".format(elapsed, self.off_time)

    def count_off(self):
        now = time.time()
        self.on_time += now - self.last_time
        self.last_time = now
        elapsed = now - self.start_time
        self.off += 1
        # print "{:f} on: {:f} ".format(elapsed, self.on_time)

    def test_init(self):
        self.assertEqual(self.motor.throttle, 0)
        self.assertEqual(self.on, 0)
        self.assertEqual(self.off, 0)

    # def test_shape(self):
    #     precision = 10
    #     cycles = 3
    #     throttle = .2
    #     ones_ok = 0
    #     zeros_ok = 0
    #     delta = .2
    #     self.motor = RelayMotor(self.countOn, self.countOff, 1)
    #     self.assertEqual(self.on, 0)
    #     self.assertEqual(self.off, 0)
    #     self.motor.set_throttle(throttle)
    #     time.sleep(self.motor.period / precision / 2.0)
    #     for c in range(cycles):
    #         for i in range(precision):
    #             if self.on == c + 1:
    #                 ones_ok += 1
    #             if float(i) / precision < throttle:
    #                 if self.off == c:
    #                     zeros_ok += 1
    #             else:
    #                 if self.off == c + 1:
    #                     zeros_ok += 1
    #             time.sleep(self.motor.period / precision)
    #     ones_rate = float(ones_ok) / float(cycles * precision)
    #     ones_error = abs(ones_rate - 1)
    #     zeros_rate = float(zeros_ok) / float(cycles * precision)
    #     zeros_error = abs(zeros_rate - 1)
    #     # print "ones_error: {}   zeros_error: {}".format(ones_error, zeros_error)
    #     self.assertLess(ones_error, delta)
    #     # self.assertGreater(zeros_error, -delta)

    def test_distribution(self, throttle=.0):
        now = time.time()
        self.start_time = self.last_time = now
        elapsed = now - self.start_time
        # print "{} start throttle: {} ".format(elapsed, throttle)
        cycles = 5
        delta = 5 / 100.0
        self.assertEqual(self.on, 0)
        self.assertEqual(self.off, 0)
        self.motor.set_throttle(throttle)
        time.sleep((cycles + 1) * self.motor.period)
        if throttle == 0:
            now = time.time()
            elapsed = now - self.start_time
            logging.info("{:f} finish throttle: {} on: {} of: {} ont: {:f} oft: {:f} tt: {:f} \
real: {:f} ".format(elapsed, throttle, self.on, self.off, self.on_time, self.off_time, self.on_time + self.off_time, 0))
            self.assertTrue(self.on_time == 0)
            self.assertTrue(self.off_time == 0)
        else:
            now = time.time()
            if self.off == self.on:
                self.off_time += now - self.last_time
            else:
                self.on_time += now - self.last_time
            total_time = self.on_time + self.off_time
            self.assertTrue(total_time != 0)
            on_rate = self.on_time / total_time
            elapsed = now - self.start_time
            logging.info("{:f} finish throttle: {} on: {} of: {} ont: {:f} oft: {:f} tt: {} \
real: {} ".format(elapsed, throttle, self.on, self.off, self.on_time, self.off_time, self.on_time + self.off_time,
                  on_rate))
            self.assertGreaterEqual(on_rate, throttle - delta)
            self.assertLessEqual(on_rate, throttle + delta)

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
