import traceback
import RPi.GPIO as GPIO
import motor.relaymotor


class Dora(object):
    pin = 7

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.signal_off()
        self.motor = motor.relaymotor.RelayMotor(self.signal_on, self.signal_off, 1)

    def signal_on(self):
        # GPIO.output(self.pin, True)
        return

    def signal_off(self):
        # GPIO.output(self.pin, False)
        return

    def tui_thread(self):
        increment = .1
        try:
            while 1:
                print "stop = Z  faster = Q  slower = A  full = W  exit = X"
                inp = raw_input().strip().upper()
                if inp == "Q":
                    self.motor.set_throttle(self.motor.throttle + increment)
                elif inp == "A":
                    self.motor.set_throttle(self.motor.throttle - increment)
                elif inp == "Z":
                    self.motor.set_throttle(0)
                elif inp == "W":
                    self.motor.set_throttle(1)
                elif inp == "X":
                    self.signal_off()
                    break
                print "period: {} throttle: {}".format(self.motor.period, self.motor.throttle)
        except Exception as exc:
            print "Error: in tui_thread - {0}".format(exc)
            traceback.print_exc()


if __name__ == "__main__":
    Dora().tui_thread()
    print "Bye!"
