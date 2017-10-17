# Setup FEng
import pylab as plt

from IPython import embed
import casperfpga
import logging
import numpy as np
import time

class dsim:
    def __init__(self):
        #logging.basicConfig()
        #casperfpga.skarab_fpga.logging.getLogger().setLevel(casperfpga.skarab_fpga.logging.DEBUG)
        print "Test course delay on SKARAB"

    def setup_FPGA(self):
        # Specify skarab to use
        # Spare SKARAB: skarab020304-01
        skarab_ip = '10.100.205.202'

        # Programming file
        prog_file = "/tmp/s_deng_rev1_13_wide_2017-10-16_1304.fpg"

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
        skarab_ip = '10.100.205.202'

        print "Communicating to SKARAB: %s" % skarab_ip

        self.f = casperfpga.CasperFpga(skarab_ip)

        self.f.get_system_information('/tmp/s_deng_rev1_13_wide_2017-10-16_1304.fpg')


        print 'Grabbing System info: Done'
        print "--------------------"
        print ''


    def run_dsim(self, arm_mode, trig_mode, valid_mode):
        print "Starting DSim"
        print "-------------"

        self.skarab_info()

        # Set the DSim CWG0

        # Set the CWG scale
        self.f.registers.scale_cwg0.write(scale=0.0)
        self.f.registers.scale_out0.write(scale=0.5)

        self.f.registers.scale_cwg1.write(scale=0.0)
        self.f.registers.scale_out1.write(scale=0.5)

        # Set the frequency
        self.f.registers.freq_cwg0.write(frequency=10000000)
        self.f.registers.freq_cwg1.write(frequency=1000000)

        # Noise Control
        self.f.registers.scale_wng0.write(scale=0.0)
        self.f.registers.scale_wng1.write(scale=0.0)
        self.f.registers.scale_wng_corr.write(scale=0.25)

        # TVG Select
        self.f.registers.orig_control.write(tvg_select0=1)
        self.f.registers.orig_control.write(tvg_select1=1)

        # Traffic Control
        self.f.registers.pol_traffic_trigger.write(pol0_tx_trigger=1)
        self.f.registers.pol_tx_always_on.write(pol0_tx_always_on=1)

        # Source Control
        self.f.registers.src_sel_cntrl.write(src_sel_0=0)
        self.f.registers.src_sel_cntrl.write(src_sel_1=0)

        # Sync Control
        self.f.registers.orig_control.write(msync=1)
        self.f.registers.orig_control.write(msync=0)

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
        ss_localtime = self.f.snapshots.ss_localtime_ss.read(arm=False)['data']
        localtime = ss_localtime['time']

        print "Grabbing fifo_in"
        ss_fifo_in = self.f.snapshots.ss_fifo_in_ss.read(arm=False)['data']

        fifo_in_d0 = ss_fifo_in['d0']
        fifo_in_d1 = ss_fifo_in['d1']
        fifo_in_d2 = ss_fifo_in['d2']
        fifo_in_d3 = ss_fifo_in['d3']
        fifo_in_d4 = ss_fifo_in['d4']
        fifo_in_d5 = ss_fifo_in['d5']
        fifo_in_d6 = ss_fifo_in['d6']
        fifo_in_d7 = ss_fifo_in['d7']

        fifo_in = []

        for x in range(0, len(fifo_in_d0)):
            fifo_in.extend(
                [fifo_in_d0[x], fifo_in_d1[x], fifo_in_d2[x], fifo_in_d3[x], fifo_in_d4[x],
                 fifo_in_d5[x], fifo_in_d6[x], fifo_in_d7[x]])


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

        plt.figure(3)
        plt.ion()
        plt.clf()
        plt.plot(fifo_in)

        plt.figure(4)
        plt.ion()
        plt.clf()
        plt.plot(hist0[0])
        plt.plot(hist1[0])

        plt.show()

        print "Done"
        print "----"