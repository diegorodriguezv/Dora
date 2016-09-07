import atexit
import os
import threading
import traceback
import subprocess

import RPi.GPIO as GPIO
import time

import motor.relaymotor


class Dora(object):
    pin = 7
    pingAlive = True
    last_input = time.time()

    def __init__(self):
        self.setup()
        self.motor = motor.relaymotor.RelayMotor(self.signal_on, self.signal_off, .1)
        self.tui_thread = threading.Thread(target=self.tui_func)
        self.tui_thread.start()
        self.ping_thread = threading.Thread(target=self.ping_func)
        self.ping_thread.start()
        self.timeout_thread = threading.Thread(target=self.timeout_func)
        self.timeout_thread.start()

    def terminate(self):
        self.motor.alive = False
        self.pingAlive = False
        self.motor.control_thread.join()
        self.signal_off()
        print "Bye!"
        exit(0)

    def setup(self):
        atexit.register(self.terminate)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.signal_off()

    def signal_on(self):
        GPIO.output(self.pin, True)
        return

    def signal_off(self):
        GPIO.output(self.pin, False)
        return

    def tui_func(self):
        increment = .1
        try:
            while 1:
                print "stop = Z  faster = Q  slower = A  full = W  exit = X"
                inp = raw_input().strip().upper()
                self.last_input = time.time()
                if inp == "Q":
                    self.motor.set_throttle(self.motor.throttle + increment)
                elif inp == "A":
                    self.motor.set_throttle(self.motor.throttle - increment)
                elif inp == "Z":
                    self.motor.set_throttle(0)
                elif inp == "W":
                    self.motor.set_throttle(1)
                elif inp == "X":
                    self.terminate()
                print "period: {} throttle: {}".format(self.motor.period, self.motor.throttle)
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
        while self.pingAlive:
            if self.check_ping_error():
                self.motor.set_throttle(0)
            else:
                pass

    def timeout_func(self):
        timeout = 3
        while self.pingAlive:
            if time.time() - self.last_input < timeout:
                self.motor.set_throttle(0)
            else:
                pass


if __name__ == "__main__":
    Dora()
