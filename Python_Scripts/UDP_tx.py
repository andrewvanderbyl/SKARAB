from IPython import embed
import logging

import time
import threading
import os

import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 11000
Message = "Hello Server"

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

class UDP_tx:
    def __init__(self, mode = 'cont', port=7148, log_handler = None, log_level = logging.INFO, spead_log_level = logging.DEBUG, **kwargs):
        # if log_handler == None:
        #     log_handler = log_handlers.DebugLogHandler(100)
        # self.log_handler = log_handler
        # self.logger = logging.getLogger('rx')
        # self.logger.addHandler(self.log_handler)
        # self.logger.setLevel(log_level)

        print "UDP TX test"
        self.tx()

    # ---------

    def tx(self):
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print "Sending Message: ", Message
        clientSock.sendto(Message, (UDP_IP_ADDRESS, UDP_PORT_NO))
