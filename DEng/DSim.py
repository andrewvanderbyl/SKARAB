# Setup FEng
import pylab as plt

from IPython import embed
import casperfpga
import logging
import numpy as np
import spead64_48 as spead
import time


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

class dsim:
    def __init__(self):
        #logging.basicConfig()
        #casperfpga.skarab_fpga.logging.getLogger().setLevel(casperfpga.skarab_fpga.logging.DEBUG)
        print "Test course delay on SKARAB"

    def setup_FPGA(self):
        # Specify skarab to use
        # Spare SKARAB: skarab020304-01
        #skarab_ip = '10.100.205.202'

        # Spare SKARAB: skarab020304-01
        skarab_ip = '10.100.213.168'


        # Programming file
        prog_file = "/tmp/s_deng_rev1_13_wide_2017-10-25_1004.fpg"

        # Create FPGA Object
        self.f = casperfpga.CasperFpga(skarab_ip)

        print 'FPGA Object Created'

        try:
            self.f.upload_to_ram_and_program(prog_file)
            print "Programming FPGA done"

        except:
            print "Programming Failed"


    def skarab_info(self):
        print 'Grabbing System info'
        print "--------------------"

        # Specify skarab to use
        # Spare SKARAB: skarab020304-01
        #skarab_ip = '10.100.205.202'

        # Spare SKARAB: skarab020304-01
        skarab_ip = '10.100.213.168'

        print "Communicating to SKARAB: %s" % skarab_ip

        self.f = casperfpga.CasperFpga(skarab_ip)

        self.f.get_system_information('/tmp/s_deng_rev1_13_wide_2017-10-25_1004.fpg')


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

        '''
                Process SPEAD data from X engines and forward it to the SD.
        '''

        logger = self.logger
        logger.info("Data reception on port %i." % data_port)

        rx = spead.TransportUDPrx(data_port, pkt_count=1024, buffer_size=51200000)
        #logger.info("Sending Signal Display data to %s:%i." % (sd_ip, sd_port))
        #tx_sd = spead.Transmitter(spead.TransportUDPtx(sd_ip, sd_port))
        #ig = spead.ItemGroup()
        #ig_sd = spead.ItemGroup()

        print "Stopping RX data"
        print "----------------"
        rx.stop()




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


