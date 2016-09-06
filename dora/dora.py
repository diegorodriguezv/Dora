import traceback
import RPi.GPIO as GPIO
import motor.relaymotor


class Dora(object):
    pin = 7

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)
        self.motor = motor.relaymotor.RelayMotor(self.motor_on, self.motor_off)


    def motor_on(self):
        # GPIO.output(self.pin, True)
        pass

    def motor_off(self):
        # GPIO.output(self.pin, False)
        pass

    def tui_thread(self):
        increment = 20
        try:
            while 1:
                inp = raw_input().strip().upper()
                if inp == "Q":
                    self.motor.set_throttle(self.motor.throttle + increment)
                elif inp == "A":
                    self.motor.set_throttle(self.motor.throttle - increment)
                elif inp == "Z":
                    self.motor.set_throttle(0)
                print "per: {} thr: {}".format(self.motor.period, self.motor.throttle)
        except Exception as exc:
            print "Error: in tui_thread - {0}".format(exc)
            traceback.print_exc()


if __name__ == "__main__":
    Dora().tui_thread()
