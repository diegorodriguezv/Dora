import atexit
import logging
import os
import subprocess
import threading
import time
import traceback
import pygame
import readchar

import motor.bidirectionalmotor
import hw.motor


class Dora(object):
    alive = True
    last_input = time.time()

    def __init__(self):
        atexit.register(self.terminate)
        hw.motor.setup()
        self.left_motor = motor.bidirectionalmotor.BidirectionalMotor(hw.motor.left_up_signal_on,
                                                                      hw.motor.left_up_signal_off,
                                                                      hw.motor.left_down_signal_on,
                                                                      hw.motor.left_down_signal_off, 0.05)
        self.right_motor = motor.bidirectionalmotor.BidirectionalMotor(hw.motor.right_up_signal_on,
                                                                       hw.motor.right_up_signal_off,
                                                                       hw.motor.right_down_signal_on,
                                                                       hw.motor.right_down_signal_off, 0.05)
        self.tui_thread = threading.Thread(target=self.tui_func)
        self.tui_thread.start()
        self.js_thread = threading.Thread(target=self.joystick_axis_func)
        self.js_thread.start()
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
        hw.motor.turn_off()
        os._exit(0)

    def tui_func(self):
        increment = .1
        try:
            while 1:
                print "left = Z - V   faster = Q - R   slower = A - F   full = W - E   full back = S - D   exit = X - C"
                inp = readchar.readkey().upper()
                print 'You pressed', inp
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
                elif inp == "R":
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
            logging.error("Error: in tui_thread - {0}".format(exc))
            traceback.print_exc()

    def joystick_button_func(self):
        increment = .1
        DPAD_U = 4
        DPAD_D = 6
        DPAD_L = 7
        PS_BTN = 16
        BTNPAD_U = 12
        BTNPAD_R = 13
        BTNPAD_D = 14
        try:
            pygame.init()
            j = pygame.joystick.Joystick(0)
            j.init()
            print "Using: {}".format(j.get_name())
            button_history = [0 for button in range(j.get_numbuttons())]
            while 1:
                pygame.event.pump()
                for button in range(0, j.get_numbuttons()):
                    if j.get_button(button) != 0:
                        if not button_history[button]:
                            was_recognized = True
                            if button == DPAD_U:
                                self.left_motor.set_throttle(self.left_motor.throttle + increment)
                            elif button == DPAD_D:
                                self.left_motor.set_throttle(self.left_motor.throttle - increment)
                            elif button == DPAD_L:
                                self.left_motor.set_throttle(0)
                            elif button == BTNPAD_U:
                                self.right_motor.set_throttle(self.right_motor.throttle + increment)
                            elif button == BTNPAD_D:
                                self.right_motor.set_throttle(self.right_motor.throttle - increment)
                            elif button == BTNPAD_R:
                                self.right_motor.set_throttle(0)
                            elif button == PS_BTN:
                                print "Bye!"
                                self.terminate()
                            else:
                                was_recognized = False
                            if was_recognized:
                                button_history[button] = True
                                self.last_input = time.time()
                                print "throttle: {} - {}".format(self.left_motor.throttle, self.right_motor.throttle)
                    else:
                        button_history[button] = 0
        except Exception as exc:
            logging.error("Error: in js_thread - {0}".format(exc))
            traceback.print_exc()

    def joystick_axis_func(self):
        PS_BTN = 16
        AXIS_L = 1
        AXIS_R = 3
        AXIS_RES = -1.0
        try:
            pygame.init()
            j = pygame.joystick.Joystick(0)
            j.init()
            print "Joystick: {}".format(j.get_name())
            button_history = [False for button in range(j.get_numbuttons())]
            while 1:
                pygame.event.pump()
                time.sleep(min(self.left_motor.period, self.right_motor.period))
                ax_l = j.get_axis(AXIS_L) / AXIS_RES
                self.left_motor.set_throttle(ax_l)
                ax_r = j.get_axis(AXIS_R) / AXIS_RES
                self.right_motor.set_throttle(ax_r)
                for button in range(0, j.get_numbuttons()):
                    if j.get_button(button) != 0:
                        if not button_history[button]:
                            if button == PS_BTN:
                                print "Bye!"
                                self.terminate()
                            print "throttle: {} - {}".format(self.left_motor.throttle, self.right_motor.throttle)
                    else:
                        button_history[button] = 0
        except Exception as exc:
            logging.error("Error: in js_thread - {0}".format(exc))
            traceback.print_exc()

    def timeout_func(self):
        timeout = 3
        print "Monitoring for input every {} seconds".format(timeout)
        while self.alive:
            if time.time() - self.last_input > timeout:
                self.left_motor.set_throttle(0)
                self.right_motor.set_throttle(0)
            time.sleep(0.5)

    def ping_func(self):
        # hostname = "8.8.8.8"
        hostname = "192.168.1.171"
        print "Monitoring connection to {} every second".format(hostname)
        while self.alive:
            if check_ping_error(hostname):
                self.left_motor.set_throttle(0)
                self.right_motor.set_throttle(0)


def check_ping_error(hostname):
    response = False
    FNULL = open(os.devnull, 'w')
    if os.name == "nt":
        response = subprocess.call(["ping", "-n", "1", hostname], stdout=FNULL)
    if os.name == "posix":
        response = subprocess.call(["ping", "-c", "1", hostname], stdout=FNULL)
    return response


if __name__ == "__main__":
    Dora()
