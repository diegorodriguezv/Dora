""" Servotester lets you test a set of servos."""

import platform
import readchar

# Don't use the raspberry pi in debug mode
DEBUG_MODE = platform.linux_distribution()[0] != 'debian'
if not DEBUG_MODE:
    import pigpio
    pi = pigpio.pi()
    if not pi.connected:
        print "pigpiod not running"
        # exit(1)
    print "hardware on"
else:
    print "no hardware to turn on"

# ask which servos to test ?
# ask which mode
#   manual
#       loop in servos
#           ask for position
#           set
#   auto
#       ask for minimum and maximum ?
#       ask for speed (`/s)
#       loop
#           set

servos = [26]
pulse_range = [1.0, 2.0]
period = 20
while True:
    for servo_num in range(0, len(servos)):
        while True:
            try:
                inp = raw_input("position for servo: {} gpio: {}? ".format(servo_num, servos[servo_num]))
                print "You entered {}".format(inp)
                pos = float(inp)
                if pos < -90 or pos > 90:
                    print "Invalid input"
                else:
                    break
            except KeyboardInterrupt:
                print "bye!"
                if not DEBUG_MODE:
                    for s in range(0, len(servos)):
                        pi.set_servo_pulsewidth(servos[s], 0)
                    pi.stop()
                exit(0)
            except Exception:
                print "Invalid input"

        total_period = pulse_range[1] - pulse_range[0]
        period_center = total_period / 2 + pulse_range[0]
        duty_cycle = (pos + 90) / 180 * total_period + pulse_range[0]
        print "duty cycle: {}".format(duty_cycle)
        if not DEBUG_MODE:
            if not pi.connected:
                print "pigpiod not running"
            else:
                pi.set_servo_pulsewidth(servos[servo_num], duty_cycle * 1000)

