import atexit
import os
import platform
import threading
import traceback
import subprocess
import time

import motor.bidirectionalmotor

# gpio: 4, 17, 27, 22
pins = [7, 11, 13, 15]
LEFT_UP = 0
LEFT_DOWN = 1
RIGHT_UP = 2
RIGHT_DOWN = 3

# Don't use the raspberry pi in debug mode
DEBUG_MODE = platform.linux_distribution()[0] == 'debian'
if not DEBUG_MODE:
    import RPi.GPIO as GPIO
    print "hardware on"


class Dora(object):
    alive = True
    last_input = time.time()

    def __init__(self):
        atexit.register(self.terminate)
        self.setup()
        self.left_motor = motor.bidirectionalmotor.BidirectionalMotor(self.left_up_signal_on, self.left_up_signal_off,
                                                                      self.left_down_signal_on,
                                                                      self.left_down_signal_off)
        self.right_motor = motor.bidirectionalmotor.BidirectionalMotor(self.right_up_signal_on,
                                                                       self.right_up_signal_off,
                                                                       self.right_down_signal_on,
                                                                       self.right_down_signal_off)
        self.tui_thread = threading.Thread(target=self.tui_func)
        self.tui_thread.start()
        self.ping_thread = threading.Thread(target=self.ping_func)
        self.ping_thread.start()
        self.timeout_thread = threading.Thread(target=self.timeout_func)
        self.timeout_thread.start()

    def terminate(self):
        self.left_motor.alive = False
        self.right_motor.alive = False
        self.alive = False
        self.left_motor.control_thread.join()
        self.right_motor.control_thread.join()
        self.turn_off()
        # print "terminate"
        os._exit(0)

    def setup(self):
        if not DEBUG_MODE:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            for pin in pins:
                GPIO.setup(pins[pin], GPIO.OUT)
                GPIO.output(pins[pin], False)

    def turn_off(self):
        if not DEBUG_MODE:
            for pin in pins:
                GPIO.output(pins[pin], False)

    def left_up_signal_on(self):
        if not DEBUG_MODE:
            GPIO.output(pins[LEFT_UP], True)

    def left_up_signal_off(self):
        if not DEBUG_MODE:
            GPIO.output(pins[LEFT_UP], False)

    def left_down_signal_on(self):
        if not DEBUG_MODE:
            GPIO.output(pins[LEFT_DOWN], True)

    def left_down_signal_off(self):
        if not DEBUG_MODE:
            GPIO.output(pins[LEFT_DOWN], False)

    def right_up_signal_on(self):
        if not DEBUG_MODE:
            GPIO.output(pins[RIGHT_UP], True)

    def right_up_signal_off(self):
        if not DEBUG_MODE:
            GPIO.output(pins[RIGHT_UP], False)

    def right_down_signal_on(self):
        if not DEBUG_MODE:
            GPIO.output(pins[RIGHT_DOWN], True)

    def right_down_signal_off(self):
        if not DEBUG_MODE:
            GPIO.output(pins[RIGHT_DOWN], False)

    def tui_func(self):
        increment = .1
        try:
            while 1:
                print "left = Z - V   faster = Q - R   slower = A - F   full = W - E   full back = S - D   exit = X - C"
                inp = raw_input().strip().upper()
                self.last_input = time.time()
                if inp == "Q":
                    self.left_motor.set_throttle(self.left_motor.throttle + increment)
                elif inp == "A":
                    self.left_motor.set_throttle(self.left_motor.throttle - increment)
                elif inp == "Z":
                    self.left_motor.set_throttle(0)
                elif inp == "W":
                    self.left_motor.set_throttle(1)
                elif inp == "S":
                    self.left_motor.set_throttle(-1)
                elif inp == "X":
                    print "Bye!"
                    self.terminate()
                if inp == "R":
                    self.right_motor.set_throttle(self.right_motor.throttle + increment)
                elif inp == "F":
                    self.right_motor.set_throttle(self.right_motor.throttle - increment)
                elif inp == "V":
                    self.right_motor.set_throttle(0)
                elif inp == "E":
                    self.right_motor.set_throttle(1)
                elif inp == "D":
                    self.right_motor.set_throttle(-1)
                elif inp == "C":
                    print "Bye!"
                    self.terminate()
                print "throttle: {} - {}".format(self.left_motor.throttle, self.right_motor.throttle)
        except Exception as exc:
            print "Error: in tui_thread - {0}".format(exc)
            traceback.print_exc()

    def check_ping_error(self):
        # hostname = "8.8.8.8"
        hostname = "192.168.1.171"
        response = False
        FNULL = open(os.devnull, 'w')
        if os.name == "nt":
            response = subprocess.call(["ping", "-n", "1", hostname], stdout=FNULL)
        if os.name == "posix":
            response = subprocess.call(["ping", "-c", "1", hostname], stdout=FNULL)
        return response

    def ping_func(self):
        while self.alive:
            if self.check_ping_error():
                self.left_motor.set_throttle(0)
                self.right_motor.set_throttle(0)

    def timeout_func(self):
        timeout = 3
        while self.alive:
            if time.time() - self.last_input > timeout:
                self.left_motor.set_throttle(0)
                self.right_motor.set_throttle(0)
            time.sleep(0.5)


if __name__ == "__main__":
    Dora()
