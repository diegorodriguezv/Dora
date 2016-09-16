import logging
import traceback

import readchar


def tui_func(actions):
    increment = .1
    try:
        while 1:
            print "left = Z - V   faster = Q - R   slower = A - F   full = W - E   full back = S - D   exit = X - C"
            inp = readchar.readkey().upper()
            print 'You pressed', inp
            actions["input_recorded"]()
            if inp == "Q":
                actions["set_left_throttle"](actions["get_left_throttle"]() + increment)
            elif inp == "A":
                actions["set_left_throttle"](actions["get_left_throttle"]() - increment)
            elif inp == "Z":
                actions["set_left_throttle"](0)
            elif inp == "W":
                actions["set_left_throttle"](1)
            elif inp == "S":
                actions["set_left_throttle"](-1)
            elif inp == "X":
                print "Bye!"
                actions["terminate"]()
            elif inp == "R":
                actions["set_right_throttle"](actions["get_right_throttle"]() + increment)
            elif inp == "F":
                actions["set_right_throttle"](actions["get_right_throttle"]() - increment)
            elif inp == "V":
                actions["set_right_throttle"](0)
            elif inp == "E":
                actions["set_right_throttle"](1)
            elif inp == "D":
                actions["set_right_throttle"](-1)
            elif inp == "C":
                print "Bye!"
                actions["terminate"]()
            print "throttle: {} - {}".format(actions["get_left_throttle"](), actions["get_right_throttle"]())
    except Exception as exc:
        logging.error("Error: in tui_thread - {0}".format(exc))
        traceback.print_exc()
