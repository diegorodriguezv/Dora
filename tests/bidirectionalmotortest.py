import unittest
import time
import logging

from dora.motor.bidirectionalmotor import BidirectionalMotor


class TestBidirectionalMotor(unittest.TestCase):

    def setUp(self):
        self.up_on = 0
        self.up_off = 0
        self.down_on = 0
        self.down_off = 0
        self.up_on_time = 0
        self.up_off_time = 0
        self.down_on_time = 0
        self.down_off_time = 0
        self.is_first_sample = True
        self.motor = BidirectionalMotor(self.up_on_func, self.up_off_func, self.down_on_func, self.down_off_func, .01)
        logging.getLogger().setLevel(logging.DEBUG)

    def tearDown(self):
        self.motor.alive = False
        self.motor.control_thread.join()

    def up_on_func(self):
        now = time.time()
        if self.is_first_sample:
            self.first_sample_time = self.last_sample_time = now
            self.is_first_sample = False
        self.up_off_time += now - self.last_sample_time
        self.last_sample_time = now
        elapsed = now - self.first_sample_time
        self.up_on += 1
        logging.debug("{:f} up_on: ont:{:f} oft:{:f}".format(elapsed, self.up_on_time, self.up_off_time))
        self.up_cycle_finished = False

    def up_off_func(self):
        now = time.time()
        self.up_on_time += now - self.last_sample_time
        self.last_sample_time = now
        elapsed = now - self.first_sample_time
        self.up_off += 1
        logging.debug("{:f} up_off: ont:{:f} oft:{:f}".format(elapsed, self.up_on_time, self.up_off_time))
        self.up_cycle_finished = True

    def down_on_func(self):
        now = time.time()
        if self.is_first_sample:
            self.first_sample_time = self.last_sample_time = now
            self.is_first_sample = False
        self.down_off_time += now - self.last_sample_time
        self.last_sample_time = now
        elapsed = now - self.first_sample_time
        self.down_on += 1
        logging.debug("{:f} down_on: ont:{:f} oft:{:f}".format(elapsed, self.down_on_time, self.down_off_time))
        self.down_cycle_finished = False

    def down_off_func(self):
        now = time.time()
        self.down_on_time += now - self.last_sample_time
        self.last_sample_time = now
        elapsed = now - self.first_sample_time
        self.down_off += 1
        logging.debug("{:f} down_off: ont:{:f} oft:{:f}".format(elapsed, self.down_on_time, self.down_off_time))
        self.down_cycle_finished = True

    def test_init(self):
        self.assertEqual(self.motor.throttle, 0)
        self.assertEqual(self.up_on_time, 0)
        self.assertEqual(self.up_off_time, 0)
        self.assertEqual(self.down_on_time, 0)
        self.assertEqual(self.down_off_time, 0)

    def test_distribution(self, throttle=.0, cycles=5, delta=.12):
        logging.debug("{:f} start throttle:{:f}".format(0, throttle))
        self.start_time = time.time()
        self.motor.throttle = throttle
        time.sleep(cycles * self.motor.period)
        now = time.time()
        elapsed = now - self.start_time
        logging.debug(
            "{:f} end throttle:{:f} up_on:{} up_of:{} up_ont:{:f} up_oft:{:f} down_on:{} down_of:{} down_ont:{:f} down_oft:{:f}"
                .format(elapsed, throttle, self.up_on, self.up_off, self.up_on_time, self.up_off_time, self.down_on,
                        self.down_off, self.down_on_time, self.down_off_time))
        if throttle == 0:
            self.assertEqual(self.up_on_time, 0)
            self.assertEqual(self.up_off_time, 0)
            self.assertEqual(self.down_on_time, 0)
            self.assertEqual(self.down_off_time, 0)
            self.assertEqual(self.up_on, 0)
            self.assertEqual(self.up_off, 0)
            self.assertEqual(self.down_on, 0)
            self.assertEqual(self.down_off, 0)
        elif throttle > 0:
            lost = now - self.last_sample_time
            total_time = self.up_on_time + self.up_off_time + lost
            self.assertTrue(total_time != 0)
            if self.up_cycle_finished:
                on_rate = self.up_on_time / total_time
            else:
                on_rate = (self.up_on_time + lost) / total_time
            logging.debug("{:f} end throttle:{:f} lost: {:f} tt: {:f} real:{:f} finished:{}"
                          .format(elapsed, throttle, lost, total_time, on_rate, self.up_cycle_finished))
            self.assertGreaterEqual(on_rate, throttle - delta)
            self.assertLessEqual(on_rate, throttle + delta)
            self.assertEqual(self.down_on_time, 0)
            self.assertEqual(self.down_off_time, 0)
            self.assertEqual(self.down_on, 0)
            self.assertEqual(self.down_off, 0)
        else:
            lost = now - self.last_sample_time
            total_time = self.down_on_time + self.down_off_time + lost
            self.assertTrue(total_time != 0)
            if self.down_cycle_finished:
                on_rate = self.down_on_time / total_time
            else:
                on_rate = (self.down_on_time + lost) / total_time
            logging.debug("{:f} end throttle:{:f} lost: {:f} tt: {:f} real:{:f} finished:{}"
                          .format(elapsed, throttle, lost, total_time, on_rate, self.down_cycle_finished))
            self.assertGreaterEqual(on_rate, -throttle - delta)
            self.assertLessEqual(on_rate, -throttle + delta)
            self.assertEqual(self.up_on_time, 0)
            self.assertEqual(self.up_off_time, 0)
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

    def test_multi_up_tri(self):
        cycles = 20
        delta = 0.50
        throttle = 0 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 5 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 10 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 20 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 25 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 33.3333333 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 50 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 80 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 90 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 95 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 100 / 100.0
        self.test_distribution(throttle, cycles, delta)

    def test_multi_up_tri_inv(self):
        cycles = 20
        delta = 0.50
        throttle = 100 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 95 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 90 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 80 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 50 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 33.3333333 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 25 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 20 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 10 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 5 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 0 / 100.0
        self.test_distribution(throttle, cycles, delta)

    def test_multi_down_tri(self):
        cycles = 20
        delta = 0.50
        throttle = 0 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -5 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -10 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -20 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -25 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -33.3333333 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -50 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -80 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -90 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -95 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -100 / 100.0
        self.test_distribution(throttle, cycles, delta)

    def test_multi_down_tri_inv(self):
        cycles = 20
        delta = 0.50
        throttle = -100 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -95 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -90 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -80 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -50 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -33.3333333 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -25 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -20 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -10 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -5 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 0 / 100.0
        self.test_distribution(throttle, cycles, delta)

    def test_multi_double_tri(self):
        self.test_multi_up_tri()
        self.test_multi_down_tri()

    def test_multi_double_tri_inv(self):
        self.test_multi_down_tri()
        self.test_multi_up_tri()

    def test_multi_double_tri_2(self):
        self.test_multi_up_tri()
        self.test_multi_up_tri_inv()

    def test_multi_double_tri_inv_2(self):
        self.test_multi_down_tri()
        self.test_multi_down_tri_inv()

    def test_multi_up_saw(self):
        self.test_multi_up_tri()
        self.test_multi_up_tri()
        self.test_multi_up_tri()
        self.test_multi_up_tri()
        self.test_multi_up_tri()

    def test_multi_down_saw(self):
        self.test_multi_down_tri()
        self.test_multi_down_tri()
        self.test_multi_down_tri()
        self.test_multi_down_tri()
        self.test_multi_down_tri()

    def test_multi_double_saw(self):
        self.test_multi_double_tri()
        self.test_multi_double_tri()
        self.test_multi_double_tri()
        self.test_multi_double_tri()
        self.test_multi_double_tri()

    def test_multi_up_saw_inv(self):
        self.test_multi_up_tri_inv()
        self.test_multi_up_tri_inv()
        self.test_multi_up_tri_inv()
        self.test_multi_up_tri_inv()
        self.test_multi_up_tri_inv()

    def test_multi_down_saw_inv(self):
        self.test_multi_down_tri_inv()
        self.test_multi_down_tri_inv()
        self.test_multi_down_tri_inv()
        self.test_multi_down_tri_inv()
        self.test_multi_down_tri_inv()

    def test_multi_double_saw_inv(self):
        self.test_multi_double_tri_inv()
        self.test_multi_double_tri_inv()
        self.test_multi_double_tri_inv()
        self.test_multi_double_tri_inv()
        self.test_multi_double_tri_inv()

    def test_multiple_throttle(self):
        cycles = 20
        delta = 0.50
        throttle = 0 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -100 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 100 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -100 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 0 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 100 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -100 / 100.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -50 / 50.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 0 / 50.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -50 / 50.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 50 / 50.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -50 / 50.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 0 / 50.0
        self.test_distribution(throttle, cycles, delta)
        throttle = 50 / 50.0
        self.test_distribution(throttle, cycles, delta)
        throttle = -50 / 50.0
        self.test_distribution(throttle, cycles, delta)
