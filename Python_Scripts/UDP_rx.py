from IPython import embed
import logging
import time
import datetime
import threading
import thread
import os
import socket

# Set IP address ans port to listen 
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 11000

#UDP_IP_ADDRESS = "192.168.1.162"
#UDP_PORT_NO = 50000


# Logger 
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

# UDP
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS,UDP_PORT_NO))

# Classes
# -------
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

    def rx(self):

        print "UDP Listen and Capture"
        print "----------------------"

        #Enter Event name
        event = raw_input('Event Name: ')
        print('Event: ', event)
        print " "


        #Enter Event name
        Write_type = raw_input('Overwrite or Append? Options: O or A: ')
        print " "
	if Write_type == 'O':
	    print "Overwrite Selected. If this file exists it will be OVERWRITTEN!\n\n"
	elif Write_type == 'A':
	    print "Append selected\n\n"
	else:
	    print "Default selected\n\n"

	print "Listening for incoming packets\n"

        while True:

            data, addr = serverSock.recvfrom(1024)
	   
            # Grab current time. This will be used as the race start time.
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
            current_datetime_split = current_datetime.split(' ')
            current_date = current_datetime_split[0]

	    thread.start_new_thread(write_file,(event, current_date, current_datetime, Write_type, data, addr))


# Global Methods
# --------------

def write_file(event, current_date, current_datetime, Write_type, data, addr):
  print "Writing file"
  # Save incoming data to file

  try:
	  if Write_type == 'O':
		#If write_type selected to overwrite, only do this the first time as otherwise all received data for the session will be clobbered.  
		#file = open(event + current_date,"w")
		file = open(event + current_date,"a")

		# Force 'Append after the first receive'
		Write_type = 'A'
	  elif Write_type == 'A':
		file = open(event + current_date,"a")
	  else: 
		file = open(event + current_date,"a")

	  file.write("Addr: " + str(addr) +"\n")
	  file.write("Date: " + current_datetime +"\n")
	  file.write(data)
	  file.write("\n\n")
	  file.close()

	  print "Date: ", current_datetime
	  print "Addr: ", addr
	  print "Data: ", data
	  print "\n"    	

  except Exception:
  	pass



