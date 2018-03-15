# Python code to start an event

from IPython import embed
import logging

import time
import datetime
import threading
import os
import Queue

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

class Time_Start:
    def __init__(self, mode = 'cont', port=7148, log_handler = None, log_level = logging.INFO, spead_log_level = logging.DEBUG, **kwargs):
        # if log_handler == None:
        #     log_handler = log_handlers.DebugLogHandler(100)
        # self.log_handler = log_handler
        # self.logger = logging.getLogger('rx')
        # self.logger.addHandler(self.log_handler)
        # self.logger.setLevel(log_level)

        print "Time Start for events. This will save system time in a text file." \
              "Note: This machine needs to have the same system time (NTP) as the nodes!"

    # -------------------------------------------------------------------------------------------------------------

    def Time_check(self):

        print "Grabbing System Time"
        print "--------------------"

        current_datetime = datetime.datetime.now()
        print current_datetime


    def Single_Start(self):

        print "Single Start Time Capture"
        print "-------------------------"

        #Enter Event name
        event = raw_input('Event Name: ')
        print('Event: ', event)
        print " "

        # Press button to capture time
        event_start = raw_input('Press any key to capture...')

        print "*** Time captured ***"

        # Grab current time. This will be used as the race start time.
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
        current_datetime_split = current_datetime.split(' ')
        current_date = current_datetime_split[0]

        print current_datetime

        file = open(event + "_start_time_" + current_date,"w")
        file.write("1 ")
        file.write(current_datetime)
        file.close()


    def Multi_start(self):

        print "Multi Start Time Capture"
        print "-------------------------"

        #Enter Event name
        event = raw_input('Event Name: ')
        print('Event: ', event)
        print " "

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
        current_datetime_split = current_datetime.split(' ')
        current_date = current_datetime_split[0]
        file = open(event + "_start_time_" + current_date,"w")

        time_capture_number = 1
        # Press button to capture time

        while True:
            event_start = raw_input('Press any key to capture. Q to end.')

            if event_start.__str__() == 'q':
                break

            # Grab current time. This will be used as the race start time.
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
            print time_capture_number.__str__() + current_datetime + "\n"

            file.write(time_capture_number.__str__())
            file.write(" ")
            file.write(current_datetime+"\n")

            time_capture_number = time_capture_number + 1

        file.close()

    def Multi_start_named(self):

        print "Multi Start Named Time Capture"
        print "------------------------------"

        #Enter Event name
        event = raw_input('Event Name: ')
        print('Event: ', event)
        print " "

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
        current_datetime_split = current_datetime.split(' ')
        current_date = current_datetime_split[0]
        file = open(event + "_start_time_" + current_date,"w")

        time_capture_number = 1
        # Press button to capture time

        while True:
            event_start = raw_input('Press any key to capture. Q to end.')

            if event_start.__str__() == 'q':
                break

            # Grab current time. This will be used as the race start time.
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
            print time_capture_number.__str__() + ' ' + current_datetime + "\n"

            file.write(time_capture_number.__str__())
            file.write(" ")
            file.write(current_datetime+"\n")

            time_capture_number = time_capture_number + 1

        file.close()