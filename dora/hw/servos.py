"""Manage the interactions with GPIO hardware for servos"""

import platform

# Don't use the raspberry pi in debug mode
DEBUG_MODE = platform.linux_distribution()[0] != 'debian'
if not DEBUG_MODE:
    import RPi.GPIO as GPIO
    print "hardware on"
else:
    print "no hardware to turn on"

# gpio 26
pins = [37]


def setup():
    if not DEBUG_MODE:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        for g in pins:
            GPIO.setup(g, GPIO.OUT)
            GPIO.output(g, False)


def turn_off():
    if not DEBUG_MODE:
        for pin in pins:
            GPIO.output(pin, False)
        GPIO.cleanup()
        print "hardware off"
    else:
        print "no hardware to turn off"


def signal_on(servo_idx):
    if not DEBUG_MODE:
        GPIO.output(pins[servo_idx], True)


def signal_off(servo_idx):
    if not DEBUG_MODE:
        GPIO.output(pins[servo_idx], False)
