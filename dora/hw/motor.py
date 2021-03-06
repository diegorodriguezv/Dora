"""Manage the interactions with GPIO hardware"""

import platform

# Don't use the raspberry pi in debug mode
DEBUG_MODE = platform.linux_distribution()[0] != 'debian'
if not DEBUG_MODE:
    import RPi.GPIO as GPIO

    print "hardware on"
else:
    print "no hardware to turn on"

# 0-3: motors
# 4: motor power system
# gpio: 4, 17, 27, 22, 18
PINS = [7, 11, 13, 15, 12]
RIGHT_DOWN = 0
RIGHT_UP = 1
LEFT_UP = 2
LEFT_DOWN = 3
MOTOR_POWER = 4


def setup():
    if not DEBUG_MODE:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        for pin in PINS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)


def turn_off():
    if not DEBUG_MODE:
        for pin in PINS:
            GPIO.output(pin, False)
        GPIO.cleanup()
        print "hardware off"
    else:
        print "no hardware to turn off"


def left_up_signal_on():
    if not DEBUG_MODE:
        GPIO.output(PINS[LEFT_UP], True)


def left_up_signal_off():
    if not DEBUG_MODE:
        GPIO.output(PINS[LEFT_UP], False)


def left_down_signal_on():
    if not DEBUG_MODE:
        GPIO.output(PINS[LEFT_DOWN], True)


def left_down_signal_off():
    if not DEBUG_MODE:
        GPIO.output(PINS[LEFT_DOWN], False)


def right_up_signal_on():
    if not DEBUG_MODE:
        GPIO.output(PINS[RIGHT_UP], True)


def right_up_signal_off():
    if not DEBUG_MODE:
        GPIO.output(PINS[RIGHT_UP], False)


def right_down_signal_on():
    if not DEBUG_MODE:
        GPIO.output(PINS[RIGHT_DOWN], True)


def right_down_signal_off():
    if not DEBUG_MODE:
        GPIO.output(PINS[RIGHT_DOWN], False)


def motors_power_signal_on():
    if not DEBUG_MODE:
        GPIO.output(PINS[MOTOR_POWER], True)


def motors_power_signal_off():
    if not DEBUG_MODE:
        GPIO.output(PINS[MOTOR_POWER], False)
