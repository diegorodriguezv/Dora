import logging
import threading
import time
import traceback


class Servo(object):
    lock = threading.Lock()
    alive = True

    def __init__(self, servo_idx, on_func, off_func, period=0.02):
        self.servo_idx = servo_idx
        self.on_func = on_func
        self.off_func = off_func
        self.period = float(period)
        self._pos = 0.0
        self.pulse_range = [0.001, 0.002]  # s
        self.pos_range = [-90, 90]  # degrees
        try:
            self.control_thread = threading.Thread(target=self.control_func)
            self.control_thread.start()
        except Exception as exc:
            logging.error("Error: unable to start thread - {0}".format(exc))

    def control_func(self):
        try:
            while self.alive:
                current_pos = self._pos
                pulse_width = (current_pos - self.pos_range[0]) / (self.pos_range[1] - self.pos_range[0]) * \
                              (self.pulse_range[1] - self.pulse_range[0]) + self.pulse_range[0]
                if pulse_width != 0:
                    self.on_func(self.servo_idx)
                self.accurate_sleep(pulse_width)
                inactive_period = self.period - pulse_width
                if pulse_width != 0:
                    self.off_func(self.servo_idx)
                self.accurate_sleep(inactive_period)
        except Exception as exc:
            logging.error("Error: in control_thread - {0}".format(exc))
            traceback.print_exc()

    def accurate_sleep(self, secs, granularity=0.0001):
        """Provide an accurate sleep mechanism. Do normal sleep for some time and then do
        busy-wait. The amount of time spent busy waiting is called granularity. It must be found
        experimentally, since it will vary with architecture. Granularity should be as low as
        possible to waste the least CPU but if it is too low it won't increase the accuracy."""
        current_time = time.time()
        time.sleep(secs - granularity)
        while time.time() < current_time + secs:
            pass

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, p):
        with self.lock:
            if p < -90:
                self._pos = -90
                logging.info("Invalid position")
            elif p > 90:
                self._pos = 90
                logging.info("Invalid position")
            else:
                self._pos = float(p)
