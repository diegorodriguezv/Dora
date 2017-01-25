"""Creates a UDP server to handle remote joystick interaction."""
import traceback
import logging
import time
import SocketServer
import interface.joystick_status_pb2

increment = .1
DPAD_U = 4
DPAD_D = 6
DPAD_L = 7
PS_BTN = 16
BTNPAD_U = 12
BTNPAD_R = 13
BTNPAD_D = 14
START = 3
AXIS_THROTTLE = 1
AXIS_STEERING = 2
AXIS_RES = -1.0
zero_delta = 0.01

latest_status = None


def remote_joystick_func(period, actions):
    logging.info("Using remote joystick")
    axis_history = [0, 0]
    button_history = {}
    while True:
        try:
            time.sleep(period)
            if latest_status:
                ax_t_value = latest_status.axes[AXIS_THROTTLE].value / AXIS_RES
                if -zero_delta < ax_t_value < zero_delta:
                    ax_t_value = 0
                ax_s_value = latest_status.axes[AXIS_STEERING].value / AXIS_RES
                if -zero_delta < ax_s_value < zero_delta:
                    ax_s_value = 0
                if ax_t_value != 0 or ax_s_value != 0:
                    actions["input_recorded"]()
                if ax_t_value != axis_history[0] or ax_s_value != axis_history[1]:
                    actions["set_throttle_steering"](ax_t_value, ax_s_value)
                    axis_history[0] = ax_t_value
                    axis_history[1] = ax_s_value
                    logging.debug(
                        "Joystick axis:Throttle: {} - {}".format(actions["get_left_throttle"](),
                                                                 actions["get_right_throttle"]()))
                for button in range(0, len(latest_status.buttons)):
                    if latest_status.buttons[button].pressed:
                        if button not in button_history:
                            if button == DPAD_U:
                                actions["set_left_throttle"](actions["get_left_throttle"]() + increment)
                            elif button == DPAD_D:
                                actions["set_left_throttle"](actions["get_left_throttle"]() - increment)
                            elif button == DPAD_L:
                                actions["set_left_throttle"](0)
                            elif button == BTNPAD_U:
                                actions["set_right_throttle"](actions["get_right_throttle"]() + increment)
                            elif button == BTNPAD_D:
                                actions["set_right_throttle"](actions["get_right_throttle"]() - increment)
                            elif button == BTNPAD_R:
                                actions["set_right_throttle"](0)
                            if button == START:
                                logging.info("Your pressed joystick start button. Bye!")
                                actions["terminate"]()
                            button_history[button] = True
                            actions["input_recorded"]()
                            logging.debug(
                                "Joystick button: Throttle buttons: {} - {}".format(actions["get_left_throttle"](),
                                                                                    actions["get_right_throttle"]()))
                    else:
                        button_history[button] = False
        except Exception as exc:
            logging.error("Error in remote joystick. {0}".format(traceback.format_exc()))


def init_server():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    # todo: improve ip finding method, currently it fails when no internet connection is available
    HOST, PORT = str(s.getsockname()[0]), 9999
    s.close()
    # HOST, PORT = "192.168.1.239", 9999
    logging.info("Remote joystick server started {} port {}".format(HOST, PORT))
    server = SocketServer.UDPServer((HOST, PORT), RemoteJoystickUDPHandler)
    server.serve_forever()


class RemoteJoystickUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        """Process a request to the remote joystick server. The request contains a joystick status. Discards statuses
        sent before the latest known status. This can happen because UDP doesn't guarantee ordered delivery. Stores the
        staus recived in the global variable latest_status."""
        global latest_status
        data = self.request[0]
        socket = self.request[1]
        logging.info("Received {} bytes from {}".format(len(data), self.client_address[0]))
        jss = interface.joystick_status_pb2.JoystickStatus()
        jss.ParseFromString(data)
        sent = jss.sent.ToDatetime()
        if not latest_status:
            latest_status = jss
        else:
            if latest_status.sent.ToDatetime() < sent:
                latest_status = jss
            else:
                logging.warning("Discarded stray package.")
        ack = interface.joystick_status_pb2.JoystickAck()
        ack.sent.CopyFrom(jss.sent)
        ack.received.GetCurrentTime()
        response = ack.SerializeToString()
        socket.sendto(response, self.client_address)
