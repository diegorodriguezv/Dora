"""Creates a UDP server to handle remote joystick interaction."""
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

status = {}


def remote_joystick_func(period, actions):
    logging.info("Using remote joystick")
    while True:
        try:
            time.sleep(period)
            # todo: decode status
        except Exception as exc:
            logging.error("Error in remote joystick. {0}".format(exc))


def init_server():
    HOST, PORT = "localhost", 9999
    logging.info("Remote joystick server started {} port {}".format(HOST, PORT))
    server = SocketServer.UDPServer((HOST, PORT), RemoteJoystickUDPHandler)
    server.serve_forever()


class RemoteJoystickUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        logging.info("received {} bytes from {}".format(len(data), self.client_address[0]))
        jss = interface.joystick_status_pb2.JoystickStatus()
        jss.ParseFromString(data)
        status["sent"] = jss.sent.ToDatetime()
        status["buttons"] = []
        for b in jss.buttons:
            status["buttons"].append(b.pressed)
        status["axes"] = []
        for a in jss.axes:
            status["axes"].append(a.value)
        ack = interface.joystick_status_pb2.JoystickAck()
        ack.sent.CopyFrom(jss.sent)
        ack.received.GetCurrentTime()
        response = ack.SerializeToString()
        socket.sendto(response, self.client_address)
