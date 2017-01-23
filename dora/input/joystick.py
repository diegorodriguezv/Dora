"""Handle joystick interaction. Uses a playstation 3 controller."""
import logging
import pygame
import time

increment = .1
DPAD_U = 4
DPAD_D = 6
DPAD_L = 7
PS_BTN = 16
BTNPAD_U = 12
BTNPAD_R = 13
BTNPAD_D = 14
START = 3
AXIS_THROTTLE = 1
AXIS_STEERING = 2
AXIS_RES = -1.0
zero_delta = 0.01


def joystick_axis_func(period, actions):
    try:
        pygame.init()
        j = pygame.joystick.Joystick(0)
        j.init()
        logging.info("Joystick: {}".format(j.get_name()))
        button_history = [False] * j.get_numbuttons()
        axis_history = [0, 0]
        while 1:
            pygame.event.pump()
            time.sleep(period)
            ax_t_value = j.get_axis(AXIS_THROTTLE) / AXIS_RES
            if -zero_delta < ax_t_value < zero_delta:
                ax_t_value = 0
            ax_s_value = j.get_axis(AXIS_STEERING) / AXIS_RES
            if -zero_delta < ax_s_value < zero_delta:
                ax_s_value = 0
            if ax_t_value != 0 or ax_s_value != 0:
                actions["input_recorded"]()
            if ax_t_value != axis_history[0] or ax_s_value != axis_history[1]:
                actions["set_throttle_steering"](ax_t_value, ax_s_value)
                axis_history[0] = ax_t_value
                axis_history[1] = ax_s_value
                logging.debug(
                    "Joystick axis:Throttle: {} - {}".format(actions["get_left_throttle"](),
                                                             actions["get_right_throttle"]()))
            for button in range(0, j.get_numbuttons()):
                if j.get_button(button) != 0:
                    if not button_history[button]:
                        if button == DPAD_U:
                            actions["set_left_throttle"](actions["get_left_throttle"]() + increment)
                        elif button == DPAD_D:
                            actions["set_left_throttle"](actions["get_left_throttle"]() - increment)
                        elif button == DPAD_L:
                            actions["set_left_throttle"](0)
                        elif button == BTNPAD_U:
                            actions["set_right_throttle"](actions["get_right_throttle"]() + increment)
                        elif button == BTNPAD_D:
                            actions["set_right_throttle"](actions["get_right_throttle"]() - increment)
                        elif button == BTNPAD_R:
                            actions["set_right_throttle"](0)
                        if button == START:
                            logging.info("Your pressed joystick start button. Bye!")
                            actions["terminate"]()
                        button_history[button] = True
                        actions["input_recorded"]()
                        logging.debug(
                            "Joystick button: Throttle buttons: {} - {}".format(actions["get_left_throttle"](),
                                                                                actions["get_right_throttle"]()))
                else:
                    button_history[button] = False
    except Exception as exc:
        logging.error("Error: in js_thread - {0}".format(exc))