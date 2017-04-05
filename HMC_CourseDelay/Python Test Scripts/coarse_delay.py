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
        self.f.get_system_information('/tmp/s_cd_ramp_2017-4-5_1411.fpg')


        # Enable the dvalid
        self.f.registers.dvalid.write(reg=1)

    def setup_FPGA(self):

        # Specify skarab to use
        skarab_ip = '10.99.55.170'
        #skarab_ip = '10.99.37.5'

        # Programming file
        prog_file = "/tmp/s_cd_ramp_2017-4-5_1411.fpg"

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
        disp_length = 20

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

            print 'Input Samples'
            print '-------------'

            print 'D0'
            print '-------------'
            print d0[0:disp_length]

            print 'D1'
            print '-------------'
            print d1[0:disp_length]

            print 'D2'
            print '-------------'
            print d2[0:disp_length]

            print 'D3'
            print '-------------'
            print d3[0:disp_length]

            print 'D4'
            print '-------------'
            print d4[0:disp_length]

            print 'D5'
            print '-------------'
            print d5[0:disp_length]

            print 'D6'
            print '-------------'
            print d6[0:disp_length]

            print 'D7'
            print '-------------'
            print d7[0:disp_length]


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

    # Input of HMC
    # ------------
    def hmc_input(self, arm_mode, trig_mode, valid_mode, plot_count_max):

        self.skarab()

        # Reset the plot counter
        plot_count = 0
        disp_length = 20

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_din_m_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            print "Grabbing HMC in SS"
            hmc_in0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din_m_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            d00 = hmc_in0['d00']
            d01 = hmc_in0['d01']
            d02 = hmc_in0['d02']
            d03 = hmc_in0['d03']
            d04 = hmc_in0['d04']
            d05 = hmc_in0['d05']
            d06 = hmc_in0['d06']
            d07 = hmc_in0['d07']
            d10 = hmc_in0['d10']
            d11 = hmc_in0['d11']
            d12 = hmc_in0['d12']
            d13 = hmc_in0['d13']
            d14 = hmc_in0['d14']
            d15 = hmc_in0['d15']
            d16 = hmc_in0['d16']
            d17 = hmc_in0['d17']

            print "SS HMC in grab complete"


            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_din_m_ss_ctrl.write(reg=0)

            hmc_in = []

            '''for x in range(0, len(d00)):
                hmc_in.extend([d10[x], d11[x], d12[x], d13[x],
                              d14[x], d15[x], d16[x], d17[x],
                              d00[x], d01[x], d02[x], d03[x],
                              d04[x], d05[x], d06[x], d07[x]])
            '''

            for x in range(0, len(d00)):
                hmc_in.extend([d10[x], d11[x], d12[x], d13[x],
                              d14[x], d15[x], d16[x], d17[x],
                              d00[x], d01[x], d02[x], d03[x],
                              d04[x], d05[x], d06[x], d07[x]])


            print "HMC in"
            print '-------------'
            print hmc_in[0:disp_length]
            print '                  '


            print 'Input Samples: D00 - D07'
            print '------------------------'
            print 'D00'
            print '-------------'
            print d00[0:disp_length]

            print 'D01'
            print '-------------'
            print d01[0:disp_length]

            print 'D02'
            print '-------------'
            print d02[0:disp_length]

            print 'D03'
            print '-------------'
            print d03[0:disp_length]

            print 'D04'
            print '-------------'
            print d04[0:disp_length]

            print 'D05'
            print '-------------'
            print d05[0:disp_length]

            print 'D06'
            print '-------------'
            print d06[0:disp_length]

            print 'D07'
            print '-------------'
            print d07[0:disp_length]
            print '                  '

            print 'Input Samples: D10 - D17'
            print '------------------------'

            print 'D10'
            print '-------------'
            print d10[0:disp_length]

            print 'D11'
            print '-------------'
            print d11[0:disp_length]

            print 'D12'
            print '-------------'
            print d12[0:disp_length]

            print 'D13'
            print '-------------'
            print d13[0:disp_length]

            print 'D14'
            print '-------------'
            print d14[0:disp_length]

            print 'D15'
            print '-------------'
            print d15[0:disp_length]

            print 'D16'
            print '-------------'
            print d16[0:disp_length]

            print 'D17'
            print '-------------'
            print d17[0:disp_length]


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

    # Output of HMC
    # -------------
    def hmc_output(self, arm_mode, trig_mode, valid_mode, plot_count_max):

        self.skarab()

        # Reset the plot counter
        plot_count = 0
        disp_length = 20

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_dout_m_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            print "Grabbing HMC out SS"
            hmc_out = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout_m_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)[
                'data']
            d00 = hmc_out['d00']
            d01 = hmc_out['d01']
            d02 = hmc_out['d02']
            d03 = hmc_out['d03']
            d04 = hmc_out['d04']
            d05 = hmc_out['d05']
            d06 = hmc_out['d06']
            d07 = hmc_out['d07']
            d10 = hmc_out['d10']
            d11 = hmc_out['d11']
            d12 = hmc_out['d12']
            d13 = hmc_out['d13']
            d14 = hmc_out['d14']
            d15 = hmc_out['d15']
            d16 = hmc_out['d16']
            d17 = hmc_out['d17']

            print "SS HMC out grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_dout_m_ss_ctrl.write(reg=0)

            hmc_out = []

            for x in range(0, len(d00)):
                hmc_out.extend([d10[x], d11[x], d12[x], d13[x],
                              d14[x], d15[x], d16[x], d17[x],
                              d00[x], d01[x], d02[x], d03[x],
                              d04[x], d05[x], d06[x], d07[x]])


            print "hmc_out"
            print '-------------'
            print hmc_out[0:disp_length]
            print '                  '


            print 'Reord Samples: D00 - D07'
            print '------------------------'
            print 'D00'
            print '-------------'
            print d00[0:disp_length]

            print 'D01'
            print '-------------'
            print d01[0:disp_length]

            print 'D02'
            print '-------------'
            print d02[0:disp_length]

            print 'D03'
            print '-------------'
            print d03[0:disp_length]

            print 'D04'
            print '-------------'
            print d04[0:disp_length]

            print 'D05'
            print '-------------'
            print d05[0:disp_length]

            print 'D06'
            print '-------------'
            print d06[0:disp_length]

            print 'D07'
            print '-------------'
            print d07[0:disp_length]
            print '                  '

            print 'Input Samples: D10 - D17'
            print '------------------------'

            print 'D10'
            print '-------------'
            print d10[0:disp_length]

            print 'D11'
            print '-------------'
            print d11[0:disp_length]

            print 'D12'
            print '-------------'
            print d12[0:disp_length]

            print 'D13'
            print '-------------'
            print d13[0:disp_length]

            print 'D14'
            print '-------------'
            print d14[0:disp_length]

            print 'D15'
            print '-------------'
            print d15[0:disp_length]

            print 'D16'
            print '-------------'
            print d16[0:disp_length]

            print 'D17'
            print '-------------'
            print d17[0:disp_length]

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

    # HMC Re-order
    # ------------
    def hmc_reord(self, arm_mode, trig_mode, valid_mode, plot_count_max):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        disp_length = 100

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # -----------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_reord_m_ss_ctrl.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_reord_addb_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            print "Grabbing HMC reord SS"
            hmc_reord = \
            self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord_m_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            d00 = hmc_reord['d00']
            d01 = hmc_reord['d01']
            d02 = hmc_reord['d02']
            d03 = hmc_reord['d03']
            d04 = hmc_reord['d04']
            d05 = hmc_reord['d05']
            d06 = hmc_reord['d06']
            d07 = hmc_reord['d07']
            d10 = hmc_reord['d10']
            d11 = hmc_reord['d11']
            d12 = hmc_reord['d12']
            d13 = hmc_reord['d13']
            d14 = hmc_reord['d14']
            d15 = hmc_reord['d15']
            d16 = hmc_reord['d16']
            d17 = hmc_reord['d17']

            print "SS HMC reord grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_reord_m_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_reord_addb_ss_ctrl.write(reg=0)

            hmc_reord = []

            for x in range(0, len(d00)):
                hmc_reord.extend([d10[x], d11[x], d12[x], d13[x],
                                d14[x], d15[x], d16[x], d17[x],
                                d00[x], d01[x], d02[x], d03[x],
                                d04[x], d05[x], d06[x], d07[x]])


            hmc_reord_addb = \
                self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reord_addb_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                     man_valid=valid_mode)['data']
            reord_addb = hmc_reord_addb['addr_b']
            reord_addb_dvalid = hmc_reord_addb['dvalid']

            print "reord addb"
            print reord_addb[0:disp_length]
            print reord_addb_dvalid[0:disp_length]
            print '                  '

            print "hmc_reord"
            print '-------------'
            print hmc_reord[0:disp_length]
            print '                  '


            print 'Reord Samples: D00 - D07'
            print '------------------------'
            print 'D00'
            print '-------------'
            print d00[0:disp_length]

            print 'D01'
            print '-------------'
            print d01[0:disp_length]

            print 'D02'
            print '-------------'
            print d02[0:disp_length]

            print 'D03'
            print '-------------'
            print d03[0:disp_length]

            print 'D04'
            print '-------------'
            print d04[0:disp_length]

            print 'D05'
            print '-------------'
            print d05[0:disp_length]

            print 'D06'
            print '-------------'
            print d06[0:disp_length]

            print 'D07'
            print '-------------'
            print d07[0:disp_length]
            print '                  '

            print 'Input Samples: D10 - D17'
            print '------------------------'

            print 'D10'
            print '-------------'
            print d10[0:disp_length]

            print 'D11'
            print '-------------'
            print d11[0:disp_length]

            print 'D12'
            print '-------------'
            print d12[0:disp_length]

            print 'D13'
            print '-------------'
            print d13[0:disp_length]

            print 'D14'
            print '-------------'
            print d14[0:disp_length]

            print 'D15'
            print '-------------'
            print d15[0:disp_length]

            print 'D16'
            print '-------------'
            print d16[0:disp_length]

            print 'D17'
            print '-------------'
            print d17[0:disp_length]

            # Plot channel Time-series
            plt.figure(4)
            plt.ion()
            plt.clf()
            plt.subplot(211)
            plt.plot(d00)
            plt.title('Output of hmc_reord d00')

            plt.subplot(212)
            plt.plot(hmc_reord)
            plt.title('Output of hmc_reord')

            plt.pause(0.01)

    # Read Tag Order
    # --------------
    def read_tag_order(self,arm_mode,trig_mode,valid_mode,plot_count_max, disp_length):

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
            print rd_tag_in[0:disp_length]
            print rd_tag_in_dv[0:disp_length]

            hmc_rd_tag_out = \
                self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_rd_tag_out_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                     man_valid=valid_mode)['data']
            rd_tag_out = hmc_rd_tag_out['rd_tag']
            rd_tag_out_dv = hmc_rd_tag_out['dvalid']


            print "rd_tag_out"
            print rd_tag_out[0:disp_length]
            print rd_tag_out_dv[0:disp_length]

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
    # ------------------
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