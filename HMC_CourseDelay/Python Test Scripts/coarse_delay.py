__author__ = 'avanderbyl'

import sys
import os
import time
import struct
import pylab as plt

from IPython import embed
import casperfpga
import logging
import numpy as np

class coarse_delay:
    def __init__(self):
        #logging.basicConfig()
        #casperfpga.skarab_fpga.logging.getLogger().setLevel(casperfpga.skarab_fpga.logging.DEBUG)
        print "Test course delay on SKARAB"

    def skarab(self):

        print 'Grabbing System info'
        self.f = casperfpga.SkarabFpga('10.99.55.170')
        self.f.get_system_information('/tmp/s_cd_ramp_2017-4-3_1226.fpg')

        # Enable the dvalid
        self.f.registers.dvalid.write(reg=1)


    def setup_FPGA(self):

        # Specify skarab to use
        skarab_ip = '10.99.55.170'

        # Programming file
        #prog_file = "/tmp/s_cd_hmc_reord_build_ramp.fpg"
        prog_file = "/tmp/s_cd_ramp_2017-4-3_1226.fpg"

        # Create FPGA Object
        self.f = casperfpga.SkarabFpga(skarab_ip)

        print 'FPGA Object Created'

        try:
            self.f.upload_to_ram_and_program(prog_file)
            print "Programming FPGA done"

        except:
            print "Programming Failed"

    # Grab read tags as they exit the HMC
    # -----------------------------------
    def rd_tag(self, arm_mode, trig_mode, valid_mode, length):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        while True:

            # Iterate through the bins
            if plot_count == length:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'
            self.f.registers.ss_rd_tag_in_ss_ctrl.write(reg=1)
            self.f.registers.ss_rd_tag_out_ss_ctrl.write(reg=1)
            self.f.registers.ss_reord_bram_addb_ss_ctrl.write(reg=1)

            print "Grabbing CD in SS"
            rd_data_in = self.f.snapshots.ss_rd_tag_in_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            rd_data_out = self.f.snapshots.ss_rd_tag_in_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            reord_bram = self.f.snapshots.ss_reord_bram_addb_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']

            rd_tag_in = rd_data_in['rd_tag']
            dvalid_in = rd_data_in['dvalid']

            rd_tag_out = rd_data_out['rd_tag']
            dvalid_out = rd_data_out['dvalid']

            reord_bram_addr = reord_bram['addr_b']
            dvalid_reord = reord_bram['dvalid']

            print 'Disarming Snapblocks'
            self.f.registers.ss_rd_tag_in_ss_ctrl.write(reg=0)
            self.f.registers.ss_rd_tag_out_ss_ctrl.write(reg=0)
            self.f.registers.ss_reord_bram_addb_ss_ctrl.write(reg=0)

            print "Rd Tag In"
            print rd_tag_in

            print "Rd Tag Out"
            print rd_tag_out

            print "Reord Addr B"
            print reord_bram_addr

    # Input of Coarse Delay
    # ---------------------
    def input_data(self,arm_mode,trig_mode,valid_mode,plot_count_max):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'
            self.f.registers.ss_cd_in_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            print "Grabbing CD in SS"
            rd_data = self.f.snapshots.ss_cd_in_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            d0 = rd_data['d0']
            d1 = rd_data['d1']
            d2 = rd_data['d2']
            d3 = rd_data['d3']
            d4 = rd_data['d4']
            d5 = rd_data['d5']
            d6 = rd_data['d6']
            d7 = rd_data['d7']

            print "SS CD in grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.ss_cd_in_ss_ctrl.write(reg=0)

            cd_in = []

            for x in range(0, len(d0)):
                cd_in.extend([d0[x], d1[x], d2[x], d3[x],
                               d4[x], d5[x], d6[x], d7[x]])

            # Plot channel Time-series
            plt.figure(1)
            plt.ion()
            plt.clf()
            plt.subplot(211)
            plt.plot(d0)
            plt.title('CD In d0')

            plt.subplot(212)
            plt.plot(cd_in)
            plt.title('cd_in')

            plt.pause(0.01)

    # Input of Coarse Delay
    # ---------------------
    def hmc_input(self, arm_mode, trig_mode, valid_mode, plot_count_max):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_ss_ctrl.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            print "Grabbing HMC in SS"
            hmc_in0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)[
                'data']
            d00 = hmc_in0['d0']
            d01 = hmc_in0['d1']
            d02 = hmc_in0['d2']
            d03 = hmc_in0['d3']
            d04 = hmc_in0['d4']
            d05 = hmc_in0['d5']
            d06 = hmc_in0['d6']
            d07 = hmc_in0['d7']
            print "D00-d07"
            print d00[1:10]
            #print d01
            #print d02
            #print d03
            #print d04
            #print d05
            #print d06
            #print d07

            hmc_in1 = \
            self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                   man_valid=valid_mode)[
                'data']
            d10 = hmc_in1['d0']
            d11 = hmc_in1['d1']
            d12 = hmc_in1['d2']
            d13 = hmc_in1['d3']
            d14 = hmc_in1['d4']
            d15 = hmc_in1['d5']
            d16 = hmc_in1['d6']
            d17 = hmc_in1['d7']

            print "D10-d17"
            print d10[1:10]
            #print d11
            #print d12
            #print d13
            #print d14
            #print d15
            #print d16
            #print d17

            print "SS HMC in grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_ss_ctrl.write(reg=0)

            hmc_in = []

            for x in range(0, len(d00)):
                hmc_in.extend([d10[x], d11[x], d12[x], d13[x],
                              d14[x], d15[x], d16[x], d17[x],
                              d00[x], d01[x], d02[x], d03[x],
                              d04[x], d05[x], d06[x], d07[x]])

            print "hmc in"
            print hmc_in[1:10]

            # Plot channel Time-series
            plt.figure(2)
            plt.ion()
            plt.clf()
            plt.subplot(211)
            plt.plot(d00)
            plt.title('Input to HMC d00')

            plt.subplot(212)
            plt.plot(hmc_in)
            plt.title('Input to HMC')

            plt.pause(0.01)

    def hmc_output(self, arm_mode, trig_mode, valid_mode, plot_count_max):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_dout0_ss_ctrl.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_dout1_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            print "Grabbing HMC out SS"
            hmc_out0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout0_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)[
                'data']
            d00 = hmc_out0['d0']
            d01 = hmc_out0['d1']
            d02 = hmc_out0['d2']
            d03 = hmc_out0['d3']
            d04 = hmc_out0['d4']
            d05 = hmc_out0['d5']
            d06 = hmc_out0['d6']
            d07 = hmc_out0['d7']
            print "D00-d07"
            print d00[1:10]
            #print d01
            #print d02
            #print d03
            #print d04
            #print d05
            #print d06
            #print d07

            hmc_out1 = \
            self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout1_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                   man_valid=valid_mode)[
                'data']
            d10 = hmc_out1['d0']
            d11 = hmc_out1['d1']
            d12 = hmc_out1['d2']
            d13 = hmc_out1['d3']
            d14 = hmc_out1['d4']
            d15 = hmc_out1['d5']
            d16 = hmc_out1['d6']
            d17 = hmc_out1['d7']

            print "D10-d17"
            print d10[1:10]
            #print d11
            #print d12
            #print d13
            #print d14
            #print d15
            #print d16
            #print d17

            print "SS HMC out grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_ss_ctrl.write(reg=0)

            hmc_out = []

            for x in range(0, len(d00)):
                hmc_out.extend([d10[x], d11[x], d12[x], d13[x],
                              d14[x], d15[x], d16[x], d17[x],
                              d00[x], d01[x], d02[x], d03[x],
                              d04[x], d05[x], d06[x], d07[x]])

            print "hmc in"
            print hmc_out[1:10]

            # Plot channel Time-series
            plt.figure(3)
            plt.ion()
            plt.clf()
            plt.subplot(211)
            plt.plot(d00)
            plt.title('Output of HMC d00')

            plt.subplot(212)
            plt.plot(hmc_out)
            plt.title('Output of HMC')

            plt.pause(0.01)

    def hmc_reord(self, arm_mode, trig_mode, valid_mode, plot_count_max):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        debug_length = 30

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # -----------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_reord0_ss_ctrl.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_reord1_ss_ctrl.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_reord_addb_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            print "Grabbing HMC out SS"
            hmc_reord0 = \
            self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord0_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                 man_valid=valid_mode)[
                'data']
            d00 = hmc_reord0['d0']
            d01 = hmc_reord0['d1']
            d02 = hmc_reord0['d2']
            d03 = hmc_reord0['d3']
            d04 = hmc_reord0['d4']
            d05 = hmc_reord0['d5']
            d06 = hmc_reord0['d6']
            d07 = hmc_reord0['d7']
            print "reord D00-d07"
            print d00[0:debug_length]
            # print d01
            # print d02
            # print d03
            # print d04
            # print d05
            # print d06
            # print d07

            hmc_reord1 = \
                self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord1_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                     man_valid=valid_mode)[
                    'data']
            d10 = hmc_reord1['d0']
            d11 = hmc_reord1['d1']
            d12 = hmc_reord1['d2']
            d13 = hmc_reord1['d3']
            d14 = hmc_reord1['d4']
            d15 = hmc_reord1['d5']
            d16 = hmc_reord1['d6']
            d17 = hmc_reord1['d7']

            print "reord D10-d17"
            print d10[0:debug_length]
            # print d11
            # print d12
            # print d13
            # print d14
            # print d15
            # print d16
            # print d17

            print "SS HMC out grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_reord0_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_reord1_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_reord_addb_ss_ctrl.write(reg=0)

            hmc_reord = []

            for x in range(0, len(d00)):
                hmc_reord.extend([d10[x], d11[x], d12[x], d13[x],
                                d14[x], d15[x], d16[x], d17[x],
                                d00[x], d01[x], d02[x], d03[x],
                                d04[x], d05[x], d06[x], d07[x]])

            print "reord data"
            print hmc_reord[0:debug_length]

            hmc_reord_addb = \
                self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reord_addb_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                     man_valid=valid_mode)['data']
            reord_addb = hmc_reord_addb['addr_b']
            reord_addb_dvalid = hmc_reord_addb['dvalid']

            print "reord addb"
            print reord_addb[0:debug_length]
            print reord_addb_dvalid[0:debug_length]

            # Plot channel Time-series
            plt.figure(4)
            plt.ion()
            plt.clf()
            plt.subplot(211)
            plt.plot(d00)
            plt.title('Output of HMC d00')

            plt.subplot(212)
            plt.plot(hmc_reord)
            plt.title('Output of HMC')

            plt.pause(0.01)


    def read_tag_order(self,arm_mode,trig_mode,valid_mode,plot_count_max):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # -----------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_rd_tag_in_ss_ctrl.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_rd_tag_out_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            print "Grabbing HMC out SS"
            hmc_rd_tag_in = \
            self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_rd_tag_in_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                 man_valid=valid_mode)['data']
            rd_tag_in = hmc_rd_tag_in['rd_tag']
            rd_tag_in_dv = hmc_rd_tag_in['dvalid']

            print "rd_tag_in"
            print rd_tag_in[0:20]
            print rd_tag_in_dv[0:20]

            hmc_rd_tag_out = \
                self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_rd_tag_out_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                     man_valid=valid_mode)['data']
            rd_tag_out = hmc_rd_tag_out['rd_tag']
            rd_tag_out_dv = hmc_rd_tag_out['dvalid']


            print "rd_tag_out"
            print rd_tag_out[0:20]
            print rd_tag_out_dv[0:20]

            print "SS HMC rd_tag grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_rd_tag_in_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_rd_tag_out_ss_ctrl.write(reg=0)



    # Output of Coarse Delay
    # ----------------------
    def output_data(self,arm_mode,trig_mode,valid_mode,plot_count_max):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'
            self.f.registers.ss_cd_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            print "Grabbing CD out SS"
            rd_data = self.f.snapshots.ss_cd_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            d0 = rd_data['d0']
            d1 = rd_data['d1']
            d2 = rd_data['d2']
            d3 = rd_data['d3']
            d4 = rd_data['d4']
            d5 = rd_data['d5']
            d6 = rd_data['d6']
            d7 = rd_data['d7']

            print "SS CD out grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.ss_cd_ss_ctrl.write(reg=0)

            cd_out = []

            for x in range(0, len(d0)):
                cd_out.extend([d0[x], d1[x], d2[x], d3[x],
                               d4[x], d5[x], d6[x], d7[x]])

            # Plot channel Time-series
            plt.figure(1)
            plt.ion()
            plt.clf()
            plt.subplot(211)
            plt.plot(d0)
            plt.title('CD Out d0')

            plt.subplot(212)
            plt.plot(cd_out)
            plt.title('cd_out')

            plt.pause(0.01)

    # Output of HMC FIFO
    def cd_interal_data(self,arm_mode,trig_mode,valid_mode,plot_count_max):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_ss_qout_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            print "Grabbing HMC FIFO SS"
            rd_data = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_ss_qout_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            d0 = rd_data['d0']
            d1 = rd_data['d1']
            d2 = rd_data['d2']
            d3 = rd_data['d3']
            d4 = rd_data['d4']
            d5 = rd_data['d5']
            d6 = rd_data['d6']
            d7 = rd_data['d7']

            print "SS HMC FIFO grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_ss_qout_ss_ctrl.write(reg=0)

            hmc_fifo = []

            for x in range(0, len(d0)):
                hmc_fifo.extend([d0[x], d1[x], d2[x], d3[x],
                               d4[x], d5[x], d6[x], d7[x]])

            # Plot channel Time-series
            plt.figure(1)
            plt.ion()
            plt.clf()
            plt.subplot(211)
            plt.plot(d0)
            plt.title('CD HMC FIFO d0')

            plt.subplot(212)
            plt.plot(hmc_fifo)
            plt.title('hmc_fifo')

            plt.pause(0.01)