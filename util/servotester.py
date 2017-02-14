""" Servotester lets you test a set of servos."""

from context import dora
from dora.motor.servo import Servo
import dora.hw.servos

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

pins = dora.hw.servos.pins
servos = []
i = 0
for g in pins:
    servos.append(Servo(i, dora.hw.servos.signal_on, dora.hw.servos.signal_off))
    i += 1
while True:
    for servo_num in range(0, len(pins)):
        while True:
            try:
                inp = raw_input("position for servo: {} pin: {}? ".format(servo_num, pins[servo_num]))
                print "You entered {}".format(inp)
                pos = float(inp)
                if pos < -90 or pos > 90:
                    print "Invalid input"
                else:
                    break
            except KeyboardInterrupt:
                print "bye!"
                for servo in servos:
                    servo.alive = False
                    dora.hw.servos.turn_off()
                exit(0)
            except Exception:
                print "Invalid input"
        servos[servo_num].position = pos
