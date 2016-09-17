import logging
import threading
import time
import traceback


class RelayMotor(object):
    lock = threading.Lock()
    alive = True

    def __init__(self, on_func, off_func, period=0.1):
        self.on_func = on_func
        self.off_func = off_func
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
                if self.throttle == 0:
                    time.sleep(self.period)
                else:
                    self.on_func()
                    active_period = self.throttle * self.period
                    time.sleep(active_period)
                    self.off_func()
                    time.sleep(self.period - active_period)
        except Exception as exc:
            logging.error("Error: in control_thread - {0}".format(exc))
            traceback.print_exc()

    def set_throttle(self, throttle):
        with self.lock:
            if throttle < 0 or throttle > 1:
                logging.warning("Error: Invalid throttle value")
                return
            self.throttle = float(throttle)
