
class RelayMotor(object):
    def __init__(self, on_func, off_func):
        self.onFunc = on_func
        self.offFunc = off_func
        self.period = 0.1
        self.throttle = 0
        self.active = 0

    def set_throttle(self, throttle):
        self.throttle = throttle
        self.active = self.period * self.throttle



