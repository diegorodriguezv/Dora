"""Handle joystick interaction. Sends raw values via ADP."""
import socket
import logging
import threading
import time
import datetime
import pygame
import interface.joystick_status_pb2

logging.getLogger().setLevel(logging.INFO)
period = .1
HOST, PORT = "localhost", 9999
ready_to_read = False


def read_socket():
    while True:
        try:
            if ready_to_read:
                received = socket.recv(1024)
                now = datetime.datetime.utcnow()
                logging.info("Received: {} bytes".format(len(received)))
                ack = interface.joystick_status_pb2.JoystickAck()
                ack.ParseFromString(received)
                logging.debug(str(ack))
                rtt = now - ack.sent.ToDatetime()
                rttms = rtt.total_seconds() * 1000
                drift = ack.received.ToDatetime() - ack.sent.ToDatetime()
                driftms = drift.total_seconds() * 1000 - rttms / 2
                logging.info("RTT {} ms  Drift {} ms".format(rttms, driftms))
            else:
                time.sleep(.05)
        except Exception as exc:
            logging.error("Problem reading response. {}".format(exc))


try:
    pygame.init()
    js = pygame.joystick.Joystick(0)
    js.init()
    logging.info("Joystick: {}".format(js.get_name()))
except Exception as exc:
    logging.error("Unable to use joystick. {}".format(exc))
    exit(1)
try:
    # SOCK_DGRAM is the socket type to use for UDP sockets
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except Exception as exc:
    logging.error("Unable to open socket. {}".format(exc))
    exit(2)
try:
    read_thread = threading.Thread(target=read_socket)
    read_thread.start()
except Exception as exc:
    logging.error("Unable to start reading thread. {}".format(exc))
    exit(3)
while True:
    try:
        pygame.event.pump()
        time.sleep(period)
        status = interface.joystick_status_pb2.JoystickStatus()
        for a in range(js.get_numaxes()):
            axis = status.axes.add()
            axis.value = js.get_axis(a)
        for b in range(0, js.get_numbuttons()):
            button = status.buttons.add()
            if js.get_button(b) != 0:
                button.pressed = True
        status.sent.GetCurrentTime()
        data = status.SerializeToString()
        socket.sendto(data, (HOST, PORT))
        ready_to_read = True
        logging.info("Sent: {} bytes".format(len(data)))
        logging.debug(str(status))
    except Exception as exc:
        logging.error("Unable to send status. {0}".format(exc))
