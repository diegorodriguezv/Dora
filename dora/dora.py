#! /usr/bin/env python
import atexit
import logging
import os
import threading
import time
import motor.bidirectionalmotor
import hw.motor
import input.remote_joystick
import input.tui
import net.ping


class Dora(object):
    alive = True
    last_input = time.time()
    last_zero_throttle = time.time()
    saving_power = True
    idle = True
    main_throttle = 0
    steering = 0

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
                   "input_recorded": self.input_recorded,
                   "set_throttle_steering": self.set_throttle_steering}
        self.tui_thread = threading.Thread(target=input.tui.tui_func, args=[actions])
        self.tui_thread.start()
        self.js_server_thread = threading.Thread(target=input.remote_joystick.init_server)
        self.js_server_thread.start()
        self.js_thread = threading.Thread(target=input.remote_joystick.remote_joystick_func,
                                          args=[min(self.left_motor.period, self.right_motor.period), actions])
        self.js_thread.start()
        # self.ping_thread = threading.Thread(target=self.ping_func)
        # self.ping_thread.start()
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

    def set_throttle_steering(self, main_throttle, steering):
        left, right = convert_steering_to_2motors(main_throttle, steering)
        self.set_left_throttle(left)
        self.set_right_throttle(right)

    def set_left_throttle(self, throttle):
        self.left_motor.throttle = throttle
        self.power_saver()

    def set_right_throttle(self, throttle):
        self.right_motor.throttle = throttle
        self.power_saver()

    def power_saver(self):
        if self.left_motor.throttle == 0 and self.right_motor.throttle == 0:
            if not self.idle:
                self.last_zero_throttle = time.time()
                self.idle = True
                logging.debug("Idle")
        else:
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
        logging.info("Checking for input timeout: {} seconds".format(timeout))
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
        logging.info("Checking connection to {}".format(hostname))
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
        timeout = 1
        triggered = False
        logging.info("Saving power after {} seconds".format(timeout))
        while self.alive:
            if time.time() - self.last_zero_throttle > timeout:
                if not triggered:
                    if self.idle:
                        hw.motor.motors_power_signal_off()
                        logging.info("Saving power: motor off")
                        self.saving_power = True
                    triggered = True
            else:
                triggered = False
            time.sleep(0.5)


def convert_steering_to_2motors(throttle, steering):
    factor = .3
    if throttle < 0:
        difference = -factor * steering
    else:
        difference = factor * steering
    left, right = throttle - difference, throttle + difference
    # Detect when steering surpasses max throttle, compensate reducing the opposing motor (same with min)
    if left > 1:
        right += 1 - left
    elif left < -1:
        right += -1 - left
    if right > 1:
        left += 1 - right
    elif right < -1:
        left += -1 - right
    return left, right


if __name__ == "__main__":
    Dora()
