import atexit
import logging
import os
import threading
import time
import motor.bidirectionalmotor
import hw.motor
import input.joystick
import input.tui
import net.ping


class Dora(object):
    alive = True
    last_input = time.time()
    last_zero_throttle = time.time()
    saving_power = False
    idle = False

    def __init__(self):
        atexit.register(self.terminate)
        logging.getLogger().setLevel(logging.INFO)
        hw.motor.setup()
        self.left_motor = motor.bidirectionalmotor.BidirectionalMotor(hw.motor.left_up_signal_on,
                                                                      hw.motor.left_up_signal_off,
                                                                      hw.motor.left_down_signal_on,
                                                                      hw.motor.left_down_signal_off,
                                                                      0.05)
        self.right_motor = motor.bidirectionalmotor.BidirectionalMotor(hw.motor.right_up_signal_on,
                                                                       hw.motor.right_up_signal_off,
                                                                       hw.motor.right_down_signal_on,
                                                                       hw.motor.right_down_signal_off,
                                                                       0.05)
        actions = {"get_left_throttle": self.get_left_throttle,
                   "get_right_throttle": self.get_right_throttle,
                   "set_left_throttle": self.set_left_throttle,
                   "set_right_throttle": self.set_right_throttle,
                   "terminate": self.terminate,
                   "input_recorded": self.input_recorded}
        self.tui_thread = threading.Thread(target=input.tui.tui_func, args=[actions])
        self.tui_thread.start()
        self.js_thread = threading.Thread(target=input.joystick.joystick_axis_func,
                                          args=[min(self.left_motor.period, self.right_motor.period), actions])
        self.js_thread.start()
        self.ping_thread = threading.Thread(target=self.ping_func)
        self.ping_thread.start()
        self.input_timeout_thread = threading.Thread(target=self.input_timeout_func)
        self.input_timeout_thread.start()
        self.save_energy_thread = threading.Thread(target=self.save_energy_func)
        self.save_energy_thread.start()

    def terminate(self):
        self.left_motor.alive = False
        self.right_motor.alive = False
        self.alive = False
        self.left_motor.control_thread.join()
        self.right_motor.control_thread.join()
        hw.motor.turn_off()
        os._exit(0)

    def set_left_throttle(self, throttle):
        self.left_motor.set_throttle(throttle)
        if throttle == 0 and self.right_motor.throttle == 0 and not self.idle:
            self.last_zero_throttle = time.time()
            self.idle = True
            logging.info("Idle")
        if throttle != 0:
            if self.saving_power:
                hw.motor.motors_power_signal_on()
                logging.info("Not saving power")
                self.saving_power = False
            self.idle = False

    def set_right_throttle(self, throttle):
        self.right_motor.set_throttle(throttle)
        if throttle == 0 and self.left_motor.throttle == 0 and not self.idle:
            self.last_zero_throttle = time.time()
            self.idle = True
            logging.info("Idle")
        if throttle != 0:
            if self.saving_power:
                hw.motor.motors_power_signal_on()
                logging.info("Not saving power")
                self.saving_power = False
            self.idle = False

    def get_left_throttle(self):
        return self.left_motor.throttle

    def get_right_throttle(self):
        return self.right_motor.throttle

    def input_recorded(self):
        self.last_input = time.time()

    def input_timeout_func(self):
        timeout = 3
        triggered = False
        print "Checking for input timeout: {} seconds".format(timeout)
        while self.alive:
            if time.time() - self.last_input > timeout:
                if not triggered:
                    self.set_left_throttle(0)
                    self.set_right_throttle(0)
                    logging.info("Input timeout: stopping")
                    triggered = True
            else:
                triggered = False
            time.sleep(0.5)
            logging.debug("Checking for input timeout")

    def ping_func(self):
        hostname = "8.8.8.8"
        # hostname = "192.168.1.171"
        triggered = False
        print "Checking connection to {}".format(hostname)
        while self.alive:
            if net.ping.check_ping_error(hostname):
                if not triggered:
                    self.set_left_throttle(0)
                    self.set_right_throttle(0)
                    logging.info("Connection lost: stopping")
                    triggered = True
            else:
                triggered = False
            time.sleep(0.5)
            logging.debug("Checking connection")

    def save_energy_func(self):
        timeout = 10
        triggered = False
        logging.info("Saving power after {} seconds".format(timeout))
        while self.alive:
            if time.time() - self.last_zero_throttle > timeout:
                if not triggered:
                    hw.motor.motors_power_signal_off()
                    logging.info("Saving power: motor off")
                    self.saving_power = True
                    triggered = True
            else:
                triggered = False
            time.sleep(1)


if __name__ == "__main__":
    Dora()
