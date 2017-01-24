"""Handle joystick interaction. Sends raw values via ADP."""
import atexit
import traceback
import socket
import errno
import logging
import threading
import time
import datetime
import pygame
import interface.joystick_status_pb2

logging.getLogger().setLevel(logging.INFO)
period = .1
HOST, PORT = "dora", 9999
ready_to_read = False
reading_thread_alive = True
sending_thread_alive = True


def read_socket():
    while reading_thread_alive:
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
                diff = ack.received.ToDatetime() - ack.sent.ToDatetime()
                diffms = diff.total_seconds() * 1000 - rttms / 2
                logging.info("RTT {} ms  Time Difference {} ms".format(rttms, diffms))
            else:
                time.sleep(.05)
        except IOError as error:
            if error.errno == errno.WSAECONNRESET:
                logging.debug("Reconnecting")
            else:
                raise
        except Exception as exc:
            logging.error("Problem reading response. {}".format(traceback.format_exc()))


def terminate():
    global sending_thread_alive, reading_thread_alive
    logging.info("Terminating...")
    # sending_thread_alive = False
    # reading_thread_alive = False
    logging.info("Bye!")

atexit.register(terminate)
try:
    pygame.init()
    js = pygame.joystick.Joystick(0)
    js.init()
    logging.info("Joystick: {}".format(js.get_name()))
except Exception as exc:
    logging.error("Unable to use joystick. {}".format(traceback.format_exc()))
    exit(1)
try:
    # SOCK_DGRAM is the socket type to use for UDP sockets
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except Exception as exc:
    logging.error("Unable to open socket. {}".format(traceback.format_exc()))
    exit(2)
try:
    read_thread = threading.Thread(target=read_socket)
    read_thread.start()
except Exception as exc:
    logging.error("Unable to start reading thread. {}".format(traceback.format_exc()))
    exit(3)
while sending_thread_alive:
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
        logging.error("Unable to send status. {0}".format(traceback.format_exc()))
