import RPi.GPIO as GPIO
import time

def turn_on_motor(pin, go):
    GPIO.output(pin, go)
    return

# gpio: 4
pins = [7]
GPIO.setmode(GPIO.BOARD)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
for x in range (0, 5000):    
    print x
    for pin in pins:        
        raw_input('Enter to start ')
        turn_on_motor(pin, True)
        raw_input('Enter to stop ')
        turn_on_motor(pin, False)
        
GPIO.cleanup()

