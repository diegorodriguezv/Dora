import atexit
import logging
import os
import threading
import traceback
import subprocess
import time
import readchar
import pygame

import motor.bidirectionalmotor
import hw


class Dora(object):
    alive = True
    last_input = time.time()

    def __init__(self):
        atexit.register(self.terminate)
        hw.setup()
        self.left_motor = motor.bidirectionalmotor.BidirectionalMotor(hw.left_up_signal_on, hw.left_up_signal_off,
                                                                      hw.left_down_signal_on,
                                                                      hw.left_down_signal_off, 0.05)
        self.right_motor = motor.bidirectionalmotor.BidirectionalMotor(hw.right_up_signal_on,
                                                                       hw.right_up_signal_off,
                                                                       hw.right_down_signal_on,
                                                                       hw.right_down_signal_off, 0.05)
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
        hw.turn_off()
        os._exit(0)

    def tui_func(self):
        increment = .1
        try:
            while 1:
                print "left = Z - V   faster = Q - R   slower = A - F   full = W - E   full back = S - D   exit = X - C   >",
                inp = readchar.readchar().upper()
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
            logging.error("Error: in tui_thread - {0}".format(exc))
            traceback.print_exc()

    def joystick_button_func(self):
        increment = .1
        DPAD_U = 4
        DPAD_R = 5
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
                            # print 'Button %i reads %i' % (button, j.get_button(button))
                            button_history[button] = 1
                            self.last_input = time.time()
                            if button == DPAD_U:
                                self.left_motor.set_throttle(self.left_motor.throttle + increment)
                            elif button == DPAD_D:
                                self.left_motor.set_throttle(self.left_motor.throttle - increment)
                            elif button == DPAD_L:
                                self.left_motor.set_throttle(0)
                            # elif button == "W":
                            #     self.left_motor.set_throttle(1)
                            # elif button == "S":
                            #     self.left_motor.set_throttle(-1)
                            # elif button == "X":
                            #     print "Bye!"
                            #     self.terminate()
                            if button == BTNPAD_U:
                                self.right_motor.set_throttle(self.right_motor.throttle + increment)
                            elif button == BTNPAD_D:
                                self.right_motor.set_throttle(self.right_motor.throttle - increment)
                            elif button == BTNPAD_R:
                                self.right_motor.set_throttle(0)
                            # elif button == "E":
                            #     self.right_motor.set_throttle(1)
                            # elif button == "D":
                            #     self.right_motor.set_throttle(-1)
                            elif button == PS_BTN:
                                print "Bye!"
                                self.terminate()
                            print "throttle: {} - {}".format(self.left_motor.throttle, self.right_motor.throttle)
                    else:
                        button_history[button] = 0
        except Exception as exc:
            logging.error("Error: in js_thread - {0}".format(exc))
            traceback.print_exc()

    def joystick_axis_func(self):
        increment = .1
        PS_BTN = 16
        AXIS_L = 1
        AXIS_R = 3
        AXIS_RES = -1.0
        try:
            pygame.init()
            j = pygame.joystick.Joystick(0)
            j.init()
            print "Using: {}".format(j.get_name())
            button_history = [0 for button in range(j.get_numbuttons())]
            while 1:
                pygame.event.pump()
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
                            # print "axes: {} - {}".format(ax_l, ax_r)
                    else:
                        button_history[button] = 0
        except Exception as exc:
            logging.error("Error: in js_thread - {0}".format(exc))
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
