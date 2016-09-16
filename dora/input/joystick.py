""""Yeah"""
import logging
import pygame
import time

import traceback


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
                            self.set_left_throttle(self.get_left_throttle() + increment)
                        elif button == DPAD_D:
                            self.set_left_throttle(self.get_left_throttle() - increment)
                        elif button == DPAD_L:
                            self.set_left_throttle(0)
                        elif button == BTNPAD_U:
                            self.set_right_throttle(self.get_right_throttle() + increment)
                        elif button == BTNPAD_D:
                            self.set_right_throttle(self.get_right_throttle() - increment)
                        elif button == BTNPAD_R:
                            self.set_right_throttle(0)
                        elif button == PS_BTN:
                            print "Bye!"
                            self.terminate()
                        else:
                            was_recognized = False
                        if was_recognized:
                            button_history[button] = True
                        self.last_input = pygame.time.time()
                        print "throttle: {} - {}".format(self.get_left_throttle(), self.get_right_throttle())
                else:
                    button_history[button] = 0
    except Exception as exc:
        logging.error("Error: in js_thread - {0}".format(exc))
        traceback.print_exc()


def joystick_axis_func(period, actions):
    PS_BTN = 16
    AXIS_L = 1
    AXIS_R = 3
    AXIS_RES = -1.0
    zero_delta = 0.01
    try:
        pygame.init()
        j = pygame.joystick.Joystick(0)
        j.init()
        print "Joystick: {}".format(j.get_name())
        button_history = [False for button in range(j.get_numbuttons())]
        axis_history = [0, 0]
        while 1:
            pygame.event.pump()
            time.sleep(period)
            ax_l_value = j.get_axis(AXIS_L) / AXIS_RES
            if -zero_delta < ax_l_value < zero_delta:
                ax_l_value = 0
            if ax_l_value != 0:
                actions["input_recorded"]()
            if ax_l_value != axis_history[0]:
                actions["set_left_throttle"](ax_l_value)
                axis_history[0] = ax_l_value
                print "throttle: {} - {}".format(actions["get_left_throttle"](), actions["get_right_throttle"]())
            ax_r_value = j.get_axis(AXIS_R) / AXIS_RES
            if -zero_delta < ax_r_value < zero_delta:
                ax_r_value = 0
            if ax_r_value != 0:
                actions["input_recorded"]()
            if ax_r_value != axis_history[1]:
                actions["set_right_throttle"](ax_r_value)
                axis_history[1] = ax_r_value
                print "throttle: {} - {}".format(actions["get_left_throttle"](), actions["get_right_throttle"]())
            for button in range(0, j.get_numbuttons()):
                if j.get_button(button) != 0:
                    if not button_history[button]:
                        if button == PS_BTN:
                            print "Bye!"
                            actions["terminate"]()
                        button_history[button] = True
                        actions["input_recorded"]()
                        print "throttle: {} - {}".format(actions["get_left_throttle"](),
                                                         actions["get_right_throttle"]())
                else:
                    button_history[button] = False
    except Exception as exc:
        logging.error("Error: in js_thread - {0}".format(exc))
        traceback.print_exc()