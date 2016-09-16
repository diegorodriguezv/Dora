import logging
import threading
import time
import traceback


class BidirectionalMotor(object):
    lock = threading.Lock()
    alive = True
    zero_delta = 0.01

    def __init__(self, up_on_func, up_off_func, down_on_func, down_off_func, period=0.1):
        self.up_on_func = up_on_func
        self.up_off_func = up_off_func
        self.down_on_func = down_on_func
        self.down_off_func = down_off_func
        self.period = float(period)
        self.throttle = 0.0
        try:
            self.control_thread = threading.Thread(target=self.control_func)
            self.control_thread.start()
        except Exception as exc:
            logging.error("Error: unable to start thread - {0}".format(exc))

    def control_func(self):
        try:
            while self.alive:
                current_throttle = self.throttle
                active_period = abs(current_throttle) * self.period
                if active_period != 0:
                    self.down_on_func() if current_throttle < 0 else self.up_on_func()
                time.sleep(active_period)
                inactive_period = self.period - active_period
                if active_period != 0:
                    self.down_off_func() if current_throttle < 0 else self.up_off_func()
                time.sleep(inactive_period)
        except Exception as exc:
            logging.error("Error: in control_thread - {0}".format(exc))
            traceback.print_exc()

    def set_throttle(self, throttle):
        with self.lock:
            if throttle < -1 or throttle > 1:
                logging.error("Error: Invalid throttle value")
                return
            if -self.zero_delta < throttle < self.zero_delta:
                self.throttle = 0.0
            else:
                self.throttle = float(throttle)
