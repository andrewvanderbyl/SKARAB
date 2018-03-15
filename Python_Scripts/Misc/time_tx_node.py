#!/usr/bin/env python
#from IPython import embed
import logging
import time
import datetime
import threading
import os
import socket

#UDP_IP_ADDRESS = "127.0.0.1"
UDP_IP_ADDRESS = "192.168.1.162"
UDP_PORT_NO = 50000
Message = "Hello Server"

sleep_time = 1

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class time_tx_class:
    def __init__(self, mode = 'cont', port=7148, log_handler = None, log_level = logging.INFO, spead_log_level = logging.DEBUG, **kwargs):
        # if log_handler == None:
        #     log_handler = log_handlers.DebugLogHandler(100)
        # self.log_handler = log_handler
        # self.logger = logging.getLogger('rx')
        # self.logger.addHandler(self.log_handler)
        # self.logger.setLevel(log_level)

        print "UDP TX test"
        #self.tx()
        self.tx_time()


    # ---------

    def tx(self):
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print "Sending Message: ", Message
        clientSock.sendto(Message, (UDP_IP_ADDRESS, UDP_PORT_NO))

    def tx_time(self):

	# Align start to second boundary
	while True:	
		time_now = datetime.datetime.now()
		
		if (time_now.microsecond < 100000):
			#print time_now.microsecond
			start = True
			break

	if (start == True):
		while True:
			# Create Socket connection
			clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
			# Get time and send time	
			# clientSock.sendto(time.ctime(), (UDP_IP_ADDRESS, UDP_PORT_NO))
			time_data_str = str(time.ctime()) + "," + str(time.time())

			clientSock.sendto(time_data_str, (UDP_IP_ADDRESS, UDP_PORT_NO))
			print time_data_str


			# Sleep for 'n' seconds
			time.sleep(sleep_time)	


print "Starting Time transmit"
tx = time_tx_class()




