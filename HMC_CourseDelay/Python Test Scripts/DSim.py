# Setup FEng
#import pylab as plt

import matplotlib.pyplot as plt
from IPython import embed
import casperfpga
import logging
import numpy as np
import spead64_48 as spead


import spead2
import spead2.recv as s2rx
import time
import threading
import os
import logging
import Queue
import matplotlib.pyplot as pyplot

from corr2 import utils
from corr2.corr_rx import CorrRx
from corr2.dsimhost_fpga import FpgaDsimHost

# Note: USED SKARABS
#skarab020306-01
#skarab020302-01
#skarab020308-01
#skarab020309-01
#skarab02030C-01
#skarab02030A-01
#skarab02030B-01
#skarab02030E-01

# Spare:
#skarab020307-01
#skarab020304-01
#skarab02030F-01

HOST = 'skarab020304-01'

# Programming file
prog_file = "/tmp/s_deng_rev1_13_wide_2017-11-08_1611.fpg"

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

class dsim:
    def __init__(self, mode = 'cont', port=7148, log_handler = None, log_level = logging.INFO, spead_log_level = logging.DEBUG, **kwargs):
        # if log_handler == None:
        #     log_handler = log_handlers.DebugLogHandler(100)
        # self.log_handler = log_handler
        # self.logger = logging.getLogger('rx')
        # self.logger.addHandler(self.log_handler)
        # self.logger.setLevel(log_level)

        print "Test DSim on SKARAB"

    def setup_FPGA(self):

        # Create FPGA Object
        self.f = casperfpga.CasperFpga(HOST)

        print 'FPGA Object Created'

        try:
            self.f.upload_to_ram_and_program(prog_file)
            print "Programming FPGA done"

        except:
            print "Programming Failed"


    def skarab_info(self):
        print 'Grabbing System info'
        print "--------------------"

        print "Communicating to SKARAB: %s" % HOST

        self.f = casperfpga.CasperFpga(HOST)

        self.f.get_system_information(prog_file)


        print 'Grabbing System info: Done'
        print "--------------------"
        print ''

    def roach2_info(self):

        roach_HOST = 'roach020A11'

        print 'Grabbing System info'
        print "--------------------"

        print "Communicating to SKARAB: %s" % roach_HOST

        self.f = casperfpga.CasperFpga(roach_HOST)

        self.f.get_system_information()


        print 'Grabbing System info: Done'
        print "--------------------"
        print ''


    def run_dsim(self, arm_mode, trig_mode, valid_mode):

        self.skarab_info()


        print "Set IP Addr"
        print "-----------"
        print "Gbe0 is: 239.2.0.64"
        self.f.registers.gbe_iptx0.write(reg=4009885760+4)
        print "Gbe0 is: 239.2.0.65"
        self.f.registers.gbe_iptx1.write(reg=4009885761+4)
        print "Gbe0 is: 239.2.0.66"
        self.f.registers.gbe_iptx2.write(reg=4009885762+4)
        print "Gbe0 is: 239.2.0.67"
        self.f.registers.gbe_iptx3.write(reg=4009885763+4)

        print "iptx0: %s" % self.f.registers.gbe_iptx0.read()
        print "iptx1: %s" % self.f.registers.gbe_iptx1.read()
        print "iptx2: %s" % self.f.registers.gbe_iptx2.read()
        print "iptx3: %s" % self.f.registers.gbe_iptx3.read()

        print "Setting Port 7148"
        self.f.registers.gbe_porttx.write(reg=7148)
        print "Port: %s" % self.f.registers.gbe_porttx.read()


        print "Starting DSim"
        print "-------------"



        # Set the DSim CWG0

        # Set the CWG scale
        self.f.registers.scale_cwg0.write(scale=0.5)
        self.f.registers.scale_out0.write(scale=0.5)

        self.f.registers.scale_cwg1.write(scale=0.5)
        self.f.registers.scale_out1.write(scale=0.5)

        # Set the frequency
        self.f.registers.freq_cwg0.write(frequency=10000000)
        self.f.registers.freq_cwg1.write(frequency=1000000)

        # Noise Control
        self.f.registers.scale_wng0.write(scale=0.0)
        self.f.registers.scale_wng1.write(scale=0.0)
        self.f.registers.scale_wng_corr.write(scale=0.0)

        # TVG Select
        self.f.registers.orig_control.write(tvg_select0=1)
        self.f.registers.orig_control.write(tvg_select1=1)

        self.f.registers.test_control.write(sel_ramp80=1)
        self.f.registers.test_control.write(rst_ramp80=0)

        # Traffic Control
        self.f.registers.pol_traffic_trigger.write(pol0_tx_trigger=1)
        self.f.registers.pol_traffic_trigger.write(pol1_tx_trigger=1)

        self.f.registers.pol_tx_always_on.write(pol0_tx_always_on=1)
        self.f.registers.pol_tx_always_on.write(pol1_tx_always_on=1)

        # Source Control
        self.f.registers.src_sel_cntrl.write(src_sel_0=0)
        self.f.registers.src_sel_cntrl.write(src_sel_1=0)

        # Sync Control
        self.f.registers.orig_control.write(msync=1)
        self.f.registers.orig_control.write(msync=0)

        self.f.registers.gbecontrol.write(gbe0=1, gbe1=1, gbe2=1, gbe3=1)

        # Arm the Snapshot Blocks
        # -----------------------
        print 'Arming Snapblocks'
        print "-----------------"

        self.f.snapshots.ss_fifo_in_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_localtime_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_cwg0_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_cwg1_ss.arm(man_trig=trig_mode, man_valid=valid_mode)

        print 'Grabbing Snapshot Data'
        print "----------------------"

        print "Grabbing localtime"
        #ss_localtime = self.f.snapshots.ss_localtime_ss.read(arm=False)['data']
        #localtime = ss_localtime['time']

        print "Grabbing fifo_in"
        #ss_fifo_in = self.f.snapshots.ss_fifo_in_ss.read(arm=False)['data']

        #fifo_in_d0 = ss_fifo_in['d0']
        #fifo_in_d1 = ss_fifo_in['d1']
        #fifo_in_d2 = ss_fifo_in['d2']
        #fifo_in_d3 = ss_fifo_in['d3']
        #fifo_in_d4 = ss_fifo_in['d4']
        #fifo_in_d5 = ss_fifo_in['d5']
        #fifo_in_d6 = ss_fifo_in['d6']
        #fifo_in_d7 = ss_fifo_in['d7']

        #fifo_in = []

        #for x in range(0, len(fifo_in_d0)):
        #    fifo_in.extend(
        #        [fifo_in_d0[x], fifo_in_d1[x], fifo_in_d2[x], fifo_in_d3[x], fifo_in_d4[x],
        #         fifo_in_d5[x], fifo_in_d6[x], fifo_in_d7[x]])


        print "Grabbing cwg0 and cwg1"
        ss_cwg0 = self.f.snapshots.ss_cwg0_ss.read(arm=False)['data']

        cwg0_d0 = ss_cwg0['d0']
        cwg0_d1 = ss_cwg0['d1']
        cwg0_d2 = ss_cwg0['d2']
        cwg0_d3 = ss_cwg0['d3']
        cwg0_d4 = ss_cwg0['d4']
        cwg0_d5 = ss_cwg0['d5']
        cwg0_d6 = ss_cwg0['d6']
        cwg0_d7 = ss_cwg0['d7']

        cwg0 = []

        for x in range(0, len(cwg0_d0)):
            cwg0.extend(
                [cwg0_d0[x], cwg0_d1[x], cwg0_d2[x], cwg0_d3[x], cwg0_d4[x],
                 cwg0_d5[x], cwg0_d6[x], cwg0_d7[x]])



        ss_cwg1 = self.f.snapshots.ss_cwg1_ss.read(arm=False)['data']

        cwg1_d0 = ss_cwg1['d0']
        cwg1_d1 = ss_cwg1['d1']
        cwg1_d2 = ss_cwg1['d2']
        cwg1_d3 = ss_cwg1['d3']
        cwg1_d4 = ss_cwg1['d4']
        cwg1_d5 = ss_cwg1['d5']
        cwg1_d6 = ss_cwg1['d6']
        cwg1_d7 = ss_cwg1['d7']

        cwg1 = []

        for x in range(0, len(cwg1_d0)):
            cwg1.extend(
                [cwg1_d0[x], cwg1_d1[x], cwg1_d2[x], cwg1_d3[x], cwg1_d4[x],
                 cwg1_d5[x], cwg1_d6[x], cwg1_d7[x]])


        #print "localtime is %s" % localtime

        # Noise Histogram
        hist0 = np.histogram(cwg0)
        hist1 = np.histogram(cwg1)


        plt.figure(1)
        plt.ion()
        plt.clf()
        plt.plot(cwg0)

        plt.figure(2)
        plt.ion()
        plt.clf()
        plt.plot(cwg1)

        #plt.figure(3)
        #plt.ion()
        #plt.clf()
        #plt.plot(fifo_in)

        plt.figure(4)
        plt.ion()
        plt.clf()
        plt.plot(hist0[0])
        plt.plot(hist1[0])

        plt.show()

        print "Done"
        print "----"


    def rx_data(self,data_port=7148, sd_ip='127.0.0.1', sd_port=7149, **kwargs):

        print "RX DSim data"
        print "------------"
        rx_port = 7148

        receiver = CorrRx(port=rx_port, queue_size=5)

        #logger.info('Waiting for receiver to report running')
        receiver.daemon = True
        receiver.start(timeout=10)
        if receiver.running_event.wait(timeout=10):
            print 'Receiver ready'
            #logger.info('Receiver ready')
        else:
            print 'Receiver not ready'
            msg = 'Receiver not ready'
            #logger.info(msg)
            raise RuntimeError(msg)

        try:
            raw_input('Press Enter get clean dump')
            dump = receiver.get_clean_dump()
        except KeyboardInterrupt:
            print 'KB interrupt'
            #logger.info('Keyboard interrupt')
        except Exception:
            raise
        else:
            print 'Dump received'
            #logger.info('Dump received')
    # Test methods

    def test_var_args(self,farg,*args):

        print "Test Method"
        print "-----------"

        print "formal arg", farg

        for arg in args:
            print "Another Arg:", arg

    def test_var_kwargs(self,farg,**kwargs):
        print "Formal arg:", farg
        for key in kwargs:
            print "Another keyword arg: %s: %s" %(key,kwargs[key])
            print "Key:", key

        print "myarg: %s", kwargs
        print "myarg: %s", kwargs['myarg']


