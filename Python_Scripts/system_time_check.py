from IPython import embed
import logging
import time
import datetime
import threading
import thread
import os
import socket


# Set IP address and port to listen 
#UDP_IP_ADDRESS = "127.0.0.0"
UDP_IP_ADDRESS = "192.168.1.162"

UDP_PORT_NO = 50000


# Logger 
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

# UDP
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS,UDP_PORT_NO))

# Classes
# -------
class system_time_rx:
    def __init__(self, mode = 'cont', port=7148, log_handler = None, log_level = logging.INFO, spead_log_level = logging.DEBUG, **kwargs):
        # if log_handler == None:
        #     log_handler = log_handlers.DebugLogHandler(100)
        # self.log_handler = log_handler
        # self.logger = logging.getLogger('rx')
        # self.logger.addHandler(self.log_handler)
        # self.logger.setLevel(log_level)

        print "Listen for time broadcast from each node"
        self.time_rx()

    def time_rx(self):
	print "Listening for incoming time packets\n"
	
	# Create array to hold rx addresses	
	addr_rx = []
	
        while True:

            	data, addr = serverSock.recvfrom(1024)

		# Check if the RX address is new or we have seen it before
		addr_len = len(addr_rx)
		
		if (addr_len == 0):
			print "first"
			ip = addr[0]
			print ip
			addr_rx.append(ip) 
		else:
			# extract IP only
			ip = addr[0]
			print ip
			print addr_rx.count(ip)
			if (addr_rx.count(ip) == True):
				print "already there"
			else:
				# add the entry
				print "second"
				addr_rx.append(ip) 
				print addr
		

		
		# Check incoming time data against time refernce (NTP server). Since this is run 			locally on the time server, check the local time
		NTP_time_now = time.ctime()
		NTP_time_split = NTP_time_now.split(' ')
		NTP_time = NTP_time_split[4] 	
		NTP_time = NTP_time.split(':')

		# Separate received time data
		rx_time_split = data.split(' ')
		rx_time = rx_time_split[4] 	
		rx_time = rx_time.split(':')
		
		# Compute difference 
		diff_hr  = int(NTP_time[0])-int(rx_time[0])
		diff_min = int(NTP_time[1])-int(rx_time[1])
		diff_sec = int(NTP_time[2])-int(rx_time[2])
		
		# Log any changes. This is done in case correction is later required to results
		# TBD

		# now print only the reults for know IP addresses
		
		# Clear the screen
		#os.system('cls' if os.name == 'nt' else 'clear')

	  	print "RX Addr: ", addr
	  	print "Time: ", data
		print "Time Diff is %s:%s:%s" % (diff_hr, diff_min, diff_sec)
		#print "Time difference is %s" % 
	  	print "\n"  	   



