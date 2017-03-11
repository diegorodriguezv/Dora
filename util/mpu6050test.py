import time
from context import dora
from dora.input.gyroscope import Gyroscope

gyro = Gyroscope()

while True:
    try:
        quat = Gyroscope.quat
        print quat
        time.sleep(0.5)
    except KeyboardInterrupt:
        print "Bye!"
        exit(0)
