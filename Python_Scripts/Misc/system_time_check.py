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

# Set flag to control time thread
show_ntp_time_thread_flag = True


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

        # Grab current time. This will be used as the race start time.
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
        current_datetime_split = current_datetime.split(' ')
        current_date = current_datetime_split[0]

        # Create array to hold rx addresses
        addr_rx = []
        data_rx_raw = []
        data_rx_time = []
        data_rx_time_ticks = []


        diff_hr = []
        diff_min = []
        diff_sec = []
        time_difference = []

        # Capture event details for logging
        # ---------------------------------
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

	# Wait for 2 seconds
	time.sleep(1)

        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')

	# Print waiting message
	print "Waiting for incoming packets..."

	#thread.start_new_thread(show_NTP_time, ())

        while True:

            data, addr = serverSock.recvfrom(1024)

	    show_ntp_time_thread_flag = False

            # Check if the RX address is new or we have seen it before
            addr_len = len(addr_rx)

            if (addr_len == 0):
                #print "first"
                ip = addr[0]
                #print ip
                addr_rx.append(ip)
                data_rx_raw.append(data)

                # Check incoming time data against time refernce (NTP server).
                # Since this is run locally on the time server, check the local time
                #NTP_time_now = time.ctime()
                #NTP_time_split = NTP_time_now.split(' ')
                #NTP_time = NTP_time_split[3]
                #NTP_time = NTP_time.split(':')
                NTP_time_now_ticks = time.time()
                NTP_time_now = time.ctime()

                # Separate received time data
                #rx_time_split = data.split(' ')
                #rx_time = rx_time_split[3]
                #rx_time = rx_time.split(':')

                # Separate received time data
                rx_time_split = data.split(',')
                #print "tp0"
                #print rx_time_split
                #print "tp1"

                rx_time = rx_time_split[0]
                rx_time_ticks = rx_time_split[1]

                data_rx_time.append(rx_time)
                data_rx_time_ticks.append(rx_time_ticks)


                # Compute difference
                #diff_hr.append(int(NTP_time[0])-int(rx_time[0]))
                #diff_min.append(int(NTP_time[1])-int(rx_time[1]))
                #diff_sec.append(int(NTP_time[2])-int(rx_time[2]))
                time_difference.append(float(NTP_time_now_ticks) - float(rx_time_ticks))

                # Log any changes. This is done in case correction is later required to results
                addr_idx = addr_rx.index(ip)
                thread.start_new_thread(write_file, (
                event, current_date, NTP_time_now, NTP_time_now_ticks, Write_type, data_rx_raw[addr_idx],
                addr_rx[addr_idx], data_rx_time[addr_idx], data_rx_time_ticks[addr_idx], time_difference[addr_idx]))


            else:
                # extract IP only
                ip = addr[0]
                #print ip
                #print addr_rx.count(ip)
                if (addr_rx.count(ip) != True):
                    # add the entry
                    addr_rx.append(ip)
                    data_rx_raw.append(data)

                    # Check incoming time data against time refernce (NTP server).
                    # Since this is run locally on the time server, check the local time
                    #NTP_time_now = time.ctime()
                    #NTP_time_split = NTP_time_now.split(' ')
                    #NTP_time = NTP_time_split[3]
                    #NTP_time = NTP_time.split(':')
                    NTP_time_now_ticks = time.time()
                    NTP_time_now = time.ctime()

                    # Separate received time data
                    #rx_time_split = data.split(' ')
                    #rx_time = rx_time_split[3]
                    #rx_time = rx_time.split(':')

                    # Separate received time data
                    rx_time_split = data.split(',')
                    #print "tp2"
                    #print rx_time_split
                    #print "tp3"

                    rx_time = rx_time_split[0]
                    rx_time_ticks = rx_time_split[1]

                    data_rx_time.append(rx_time)
                    data_rx_time_ticks.append(rx_time_ticks)

                    # Compute difference
                    #diff_hr.append(int(NTP_time[0])-int(rx_time[0]))
                    #diff_min.append(int(NTP_time[1])-int(rx_time[1]))
                    #diff_sec.append(int(NTP_time[2])-int(rx_time[2]))
                    time_difference.append(float(NTP_time_now_ticks) - float(rx_time_ticks))

                    # Log any changes. This is done in case correction is later required to results
                    addr_idx = addr_rx.index(ip)
                    thread.start_new_thread(write_file, (
                        event, current_date, NTP_time_now, NTP_time_now_ticks, Write_type, data_rx_raw[addr_idx],
                        addr_rx[addr_idx], data_rx_time[addr_idx], data_rx_time_ticks[addr_idx],
                        time_difference[addr_idx]))

                else:
                    addr_idx = addr_rx.index(ip)
                    # Get index of entry and overwrite
                    data_rx_raw[addr_idx] = data

                    # Check incoming time data against time refernce (NTP server).
                    # Since this is run locally on the time server, check the local time
                    #NTP_time_now = time.ctime()
                    #NTP_time_split = NTP_time_now.split(' ')
                    #NTP_time = NTP_time_split[3]
                    #NTP_time = NTP_time.split(':')
                    NTP_time_now_ticks = time.time()
                    NTP_time_now = time.ctime()

                    # Separate received time data
                    #rx_time_split = data.split(' ')
                    #rx_time = rx_time_split[3]
                    #rx_time = rx_time.split(':')

                    # Separate received time data
                    rx_time_split = data.split(',')
                    #print "tp4"
                    #print rx_time_split
                    #print "tp5"
                    rx_time = rx_time_split[0]
                    rx_time_ticks = rx_time_split[1]

                    data_rx_time[addr_idx] = rx_time
                    data_rx_time_ticks[addr_idx] = rx_time_ticks

                    # Compute difference
                    #diff_hr[addr_idx] = (int(NTP_time[0])-int(rx_time[0]))
                    #diff_min[addr_idx] = (int(NTP_time[1])-int(rx_time[1]))
                    #diff_sec[addr_idx] = (int(NTP_time[2])-int(rx_time[2]))
                    time_difference[addr_idx] = (float(NTP_time_now_ticks) - float(rx_time_ticks))

                    # Log any changes. This is done in case correction is later required to results
                    thread.start_new_thread(write_file, (event, current_date, NTP_time_now, NTP_time_now_ticks, Write_type, data_rx_raw[addr_idx], addr_rx[addr_idx], data_rx_time[addr_idx], data_rx_time_ticks[addr_idx], time_difference[addr_idx]))

            # Now print only the results for know IP addresses
            # ------------------------------------------------

            # Clear the screen
            os.system('cls' if os.name == 'nt' else 'clear')

            # Print local time
            print "NTP Time: %s" % NTP_time_now
            print "NTP Time Ticks: %s" % NTP_time_now_ticks
            print ""

            for i in range(len(addr_rx)):
                print "RX Addr: ", addr_rx[i]
                print "Remote Time: ", data_rx_time[i]
                print "Remote Time Ticks: ", data_rx_time_ticks[i]
                #print "Time Diff is %s:%s:%s" % (diff_hr[i], diff_min[i], diff_sec[i])
                print "Time Difference is %s" % time_difference[i]
                print "\n"


# Global Methods
# --------------

def write_file(event, current_date, NTP_time_now, NTP_time_now_ticks, Write_type, data_rx_raw, addr_rx, data_rx_time, data_rx_time_ticks, time_difference):
    print "Writing file"
    # Save incoming data to file

    try:
         if Write_type == 'O':
             # If write_type selected to overwrite, only do this the first time as otherwise all received data for the session will be clobbered.
             # file = open(event + current_date,"w")
             file = open(event + current_date,"a")

             # Force 'Append after the first receive'
             Write_type = 'A'
             print "type O"

         else:
            file = open(event + current_date,"a")

            file.write("Addr: " + str(addr_rx) + "\n")
            file.write("NTP Time: %s" % NTP_time_now + "\n")
            file.write("NTP Time Ticks: %s" % NTP_time_now_ticks + "\n")
            file.write("Remote Time: %s" % str(data_rx_time) + "\n")
            file.write("Remote Time Ticks: %s" % str(data_rx_time_ticks) + "\n")
            file.write("Time Difference: %s" % str(time_difference) + "\n")
            file.write("Raw RX data: %s" % str(data_rx_raw) + "\n")
            file.write("\n\n")
            file.close()

            #data_len = len(addr_rx)

            #for i in range(data_len):
            #    file.write("Addr: " + str(addr_rx[i]) +"\n")
            #    file.write("NTP Time: %s" % NTP_time_now +"\n")
            #    file.write("NTP Time Ticks: %s" % NTP_time_now_ticks + "\n")
            #    file.write("Remote Time: %s" % str(data_rx_time[i]) +"\n")
            #    file.write("Remote Time Ticks: %s" % str(data_rx_time_ticks[i]) + "\n")
            #    file.write("Time Difference: %s" % str(time_difference[i]) + "\n")
            #    file.write("Raw RX data: %s" % str(data_rx_raw[i]) + "\n")
            #    file.write("\n\n")
            #    file.close()

            #    print "Addr: " + str(addr_rx[i]) +"\n"
            #    print "NTP Time: %s" % NTP_time_now +"\n"
            #    print "NTP Time Ticks: %s" % NTP_time_now_ticks + "\n"
            #    print "Remote Time: %s" % str(data_rx_time[i]) +"\n"
            #    print "Remote Time Ticks: %s" % str(data_rx_time_ticks[i]) + "\n"
            #    print "Time Difference: %s" % str(time_difference[i]) + "\n"
            #    print "Raw RX data: %s" % str(data_rx_raw[i]) + "\n"
            #    print "\n\n"

    except Exception:
        print "bailing"
        print Exception.message
        pass

def show_NTP_time():

	while True:
		# Clear the screen
		os.system('cls' if os.name == 'nt' else 'clear')

		# Show time
		print "NTP Time is: %s" % time.ctime()
		print "Waiting for incoming time data..."
		
		if show_ntp_time_thread_flag == False:
			break
			print "Break"
		else:
			print "Sleep"			
			time.sleep(1)


print "Starting Time Monitor"
st = system_time_rx()
