from IPython import embed
import logging

import time
import threading
import os

import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 11000


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverSock.bind((UDP_IP_ADDRESS,UDP_PORT_NO))

class UDP_rx:
    def __init__(self, mode = 'cont', port=7148, log_handler = None, log_level = logging.INFO, spead_log_level = logging.DEBUG, **kwargs):
        # if log_handler == None:
        #     log_handler = log_handlers.DebugLogHandler(100)
        # self.log_handler = log_handler
        # self.logger = logging.getLogger('rx')
        # self.logger.addHandler(self.log_handler)
        # self.logger.setLevel(log_level)

        print "UDP RX test"
        self.rx()

    # ---------

    def rx(self):

        while True:
            data, addr = serverSock.recvfrom(1024)
            print "Message: ", data

