import threading
import time
import traceback
import thread


class RelayMotor(object):
    lock = threading.Lock()

    def __init__(self, on_func, off_func, period=0.1):
        self.on_func = on_func
        self.off_func = off_func
        self.period = float(period)
        self.throttle = 0.0
        try:
            thread.start_new_thread(self.control_thread, ())
        except Exception as exc:
            print "Error: unable to start thread - {0}".format(exc)

    def control_thread(self):
        try:
            while 1:
                if self.throttle == 0:
                    time.sleep(self.period)
                else:
                    self.on_func()
                    with self.lock:
                        active_period = self.throttle * self.period
                    time.sleep(active_period)
                    self.off_func()
                    time.sleep(self.period - active_period)
        except Exception as exc:
            print "Error: in control_thread - {0}".format(exc)
            traceback.print_exc()

    def set_throttle(self, throttle):
        with self.lock:
            if throttle < 0 or throttle > 100:
                print "Error: Invalid throttle value"
                return
            self.throttle = throttle





