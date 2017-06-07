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
import time

class coarse_delay:
    def __init__(self):
        #logging.basicConfig()
        #casperfpga.skarab_fpga.logging.getLogger().setLevel(casperfpga.skarab_fpga.logging.DEBUG)
        print "Test course delay on SKARAB"

    def skarab(self):

        print 'Grabbing System info'

        self.f = casperfpga.SkarabFpga('10.99.55.170')
        #self.f = casperfpga.SkarabFpga('10.99.39.170')

        self.f.get_system_information('/tmp/s_cd_hmc_v2_2017-6-7_1255.fpg')
        #self.f.get_system_information('/tmp/s_cd_hmc_v2_dvalid_sync_2017-6-1_0733.fpg')
                
    def setup_FPGA(self):

        # Specify skarab to use
        skarab_ip = '10.99.55.170'
        #skarab_ip = '10.99.39.170'
        
        # Programming file
        prog_file = "/tmp/s_cd_hmc_v2_2017-6-7_1255.fpg"
        #prog_file = "/tmp/s_cd_hmc_v2_dvalid_sync_2017-6-1_0733.fpg"
        
        
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
    def input_data(self,arm_mode,trig_mode,valid_mode,plot_count_max,disp_length):

        self.skarab()

        # Reset the plot counter
        plot_count = 0


        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg  = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']


        print "Post is %s" % post
        print "Init is %s" % init

        # Set delay for test
        self.f.registers.delay0.write(initial=0)

        self.f.registers.sync_en_cd_in.write(reg=0)
        self.f.registers.man_dvalid.write(reg=0)

        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=0)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_en.write(reg=1)

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_in_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            print "Grabbing CD in SS"
            rd_data = self.f.snapshots.cd_in_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            d00 = rd_data['d00']
            d01 = rd_data['d01']
            d02 = rd_data['d02']
            d03 = rd_data['d03']
            d04 = rd_data['d04']
            d05 = rd_data['d05']
            d06 = rd_data['d06']
            d07 = rd_data['d07']

            print "SS CD in grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_in_ss_ctrl.write(reg=0)

            cd_in = []

            for x in range(0, len(d00)):
                cd_in.extend([d00[x], d01[x], d02[x], d03[x],
                               d04[x], d05[x], d06[x], d07[x]])

            print 'Input Samples'
            print '-------------'

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


            # Plot channel Time-series
            plt.figure(1)
            plt.ion()
            plt.clf()
            plt.subplot(211)
            plt.plot(d00)
            plt.title('CD In d0')

            plt.subplot(212)
            plt.plot(cd_in)
            plt.title('cd_in')

            plt.pause(0.01)

    # Input of HMC
    # ------------
    def hmc_input(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length):

        self.skarab()

        # Reset the plot counter
        plot_count = 0


        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg  = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']


        print "Post is %s" % post
        print "Init is %s" % init

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_din_all0_ss_ctrl.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_din_all1_ss_ctrl.write(reg=1)

            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_en_in.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_en.write(reg=1)


            print 'Arming Snapblocks done'

            print "Grabbing HMC in SS"
            hmc_in0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din_all0_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            hmc_in1 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din_all1_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']

            # Separate data
            d00 = hmc_in0['d00']
            d01 = hmc_in0['d01']
            d02 = hmc_in0['d02']
            d03 = hmc_in0['d03']
            d04 = hmc_in0['d04']
            d05 = hmc_in0['d05']
            d06 = hmc_in0['d06']
            d07 = hmc_in0['d07']
            d10 = hmc_in1['d00']
            d11 = hmc_in1['d01']
            d12 = hmc_in1['d02']
            d13 = hmc_in1['d03']
            d14 = hmc_in1['d04']
            d15 = hmc_in1['d05']
            d16 = hmc_in1['d06']
            d17 = hmc_in1['d07']

            win0 = hmc_in0['win']
            rin0 = hmc_in0['rin']
            waddr0 = hmc_in0['waddr']
            raddr0 = hmc_in0['raddr']
            tag0 = hmc_in0['tag']

            win1 = hmc_in1['win']
            rin1 = hmc_in1['rin']
            waddr1 = hmc_in1['waddr']
            raddr1 = hmc_in1['raddr']
            tag1 = hmc_in1['tag']



            print "SS HMC in grab complete"


            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_din_all0_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_din_all1_ss_ctrl.write(reg=0)

            hmc_in = []

            for x in range(0, len(d00)):
                '''hmc_in.extend([d10[x], d11[x], d12[x], d13[x],
                              d14[x], d15[x], d16[x], d17[x],
                              d00[x], d01[x], d02[x], d03[x],
                              d04[x], d05[x], d06[x], d07[x]])
                '''
                hmc_in.extend([d00[x], d01[x], d02[x], d03[x],
                              d04[x], d05[x], d06[x], d07[x],
                              d10[x], d11[x], d12[x], d13[x],
                              d14[x], d15[x], d16[x], d17[x]])

            print "HMC in"
            print '-------------'
            print hmc_in[0:disp_length]
            print '                  '

            print "waddr0"
            print '-------------'
            print waddr0[0:disp_length]
            print '                  '
            print "waddr1"
            print '-------------'
            print waddr1[0:disp_length]
            print '             '

            print "win0"
            print '-------------'
            print win0[0:disp_length]
            print '                  '
            print "win1"
            print '-------------'
            print win1[0:disp_length]
            print '             '

            print "raddr0"
            print '-------------'
            print raddr0[0:disp_length]
            print '                  '
            print "raddr1"
            print '-------------'
            print raddr1[0:disp_length]
            print '             '

            print "rin0"
            print '-------------'
            print rin0[0:disp_length]
            print '                  '
            print "rin1"
            print '-------------'
            print rin1[0:disp_length]
            print '             '

            print "tag"
            print '-------------'
            print tag0[0:disp_length]
            print '             '





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
            print 'D05'
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
            plt.plot(hmc_in)
            plt.title('Input to HMC')

            plt.pause(0.01)

    # Output of HMC
    # -------------
    def hmc_output(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg  = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']


        print "Post is %s" % post
        print "Init is %s" % init

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break           
            
            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_dout_all0_ss_ctrl.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_dout_all1_ss_ctrl.write(reg=1)

            print 'Arming Snapblocks done'


            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_en_out.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_en.write(reg=1)

            print "Grabbing HMC out SS"
            hmc_out0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout_all0_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            hmc_out1 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout_all1_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']

            # Separate data
            d00 = hmc_out0['d00']
            d01 = hmc_out0['d01']
            d02 = hmc_out0['d02']
            d03 = hmc_out0['d03']
            d04 = hmc_out0['d04']
            d05 = hmc_out0['d05']
            d06 = hmc_out0['d06']
            d07 = hmc_out0['d07']
            d10 = hmc_out1['d00']
            d11 = hmc_out1['d01']
            d12 = hmc_out1['d02']
            d13 = hmc_out1['d03']
            d14 = hmc_out1['d04']
            d15 = hmc_out1['d05']
            d16 = hmc_out1['d06']
            d17 = hmc_out1['d07']


            dvalid0 = hmc_out0['dvalid']
            wr_rdy0 = hmc_out0['wr_rdy']
            rd_rdy0 = hmc_out0['rd_rdy']
            init0 = hmc_out0['init']
            post0 = hmc_out0['post']
            tag0 = hmc_out0['tag']

            dvalid1 = hmc_out1['dvalid']
            wr_rdy1 = hmc_out1['wr_rdy']
            rd_rdy1 = hmc_out1['rd_rdy']
            init1 = hmc_out1['init']
            post1 = hmc_out1['post']
            tag1 = hmc_out1['tag']

            print "SS HMC out grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_dout_all0_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_dout_all1_ss_ctrl.write(reg=0)

            hmc_out = []

            for x in range(0, len(d00)):
                '''hmc_out.extend([d10[x], d11[x], d12[x], d13[x],
                              d14[x], d15[x], d16[x], d17[x],
                              d00[x], d01[x], d02[x], d03[x],
                              d04[x], d05[x], d06[x], d07[x]])
                '''
                hmc_out.extend([d00[x], d01[x], d02[x], d03[x],
                              d04[x], d05[x], d06[x], d07[x],
                              d10[x], d11[x], d12[x], d13[x],
                              d14[x], d15[x], d16[x], d17[x]])

            print "hmc_out"
            print '-------------'
            print hmc_out[0:disp_length]
            print '                  '


            print "dvalid0"
            print '-------------'
            print dvalid0[0:disp_length]
            print '                  '
            print "dvalid1"
            print '-------------'
            print dvalid1[0:disp_length]
            print '             '

            print "wr_rdy0"
            print '-------------'
            print wr_rdy0[0:disp_length]
            print '                  '
            print "wr_rdy1"
            print '-------------'
            print wr_rdy1[0:disp_length]
            print '             '

            print "rd_rdy0"
            print '-------------'
            print rd_rdy0[0:disp_length]
            print '                  '
            print "rd_rdy1"
            print '-------------'
            print rd_rdy1[0:disp_length]
            print '             '

            print "init0"
            print '-------------'
            print init0[0:disp_length]
            print '                  '
            print "init1"
            print '-------------'
            print init1[0:disp_length]
            print '             '

            print "post0"
            print '-------------'
            print post0[0:disp_length]
            print '                  '
            print "post1"
            print '-------------'
            print post1[0:disp_length]
            print '             '

            print "tag out"
            print '-------------'
            print tag0[0:disp_length]
            print '             '




            print 'Output Samples: D00 - D07'
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

            print 'Output Samples: D10 - D17'
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
            plt.plot(hmc_out)
            plt.title('Output of HMC')

            plt.pause(0.01)

    # HMC Re-order
    # ------------
    def hmc_reord(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length):

        self.skarab()

        # Reset the plot counter
        plot_count = 0


        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg  = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']


        print "Post is %s" % post
        print "Init is %s" % init

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
            print 'Arming Snapblocks done'

            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_en_reord.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_en.write(reg=1)

            print "Grabbing HMC reord SS"
            hmc_reord0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord0_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']

            hmc_reord1 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord1_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']

            d00 = hmc_reord0['d00']
            d01 = hmc_reord0['d01']
            d02 = hmc_reord0['d02']
            d03 = hmc_reord0['d03']
            d04 = hmc_reord0['d04']
            d05 = hmc_reord0['d05']
            d06 = hmc_reord0['d06']
            d07 = hmc_reord0['d07']
            d10 = hmc_reord1['d00']
            d11 = hmc_reord1['d01']
            d12 = hmc_reord1['d02']
            d13 = hmc_reord1['d03']
            d14 = hmc_reord1['d04']
            d15 = hmc_reord1['d05']
            d16 = hmc_reord1['d06']
            d17 = hmc_reord1['d07']

            print "SS HMC reord grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_reord0_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_reord1_ss_ctrl.write(reg=0)

            hmc_reord = []

            for x in range(0, len(d00)):
                '''hmc_reord.extend([d10[x], d11[x], d12[x], d13[x],
                                d14[x], d15[x], d16[x], d17[x],
                                d00[x], d01[x], d02[x], d03[x],
                                d04[x], d05[x], d06[x], d07[x]])
                '''
                hmc_reord.extend([d00[x], d01[x], d02[x], d03[x],
                              d04[x], d05[x], d06[x], d07[x],
                              d10[x], d11[x], d12[x], d13[x],
                              d14[x], d15[x], d16[x], d17[x]])
            print "hmc_reord"
            print '-------------'
            print hmc_reord[(len(hmc_reord)-disp_length):len(hmc_reord)]
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

            print 'Reord Samples: D10 - D17'
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
            plt.plot(hmc_reord)
            plt.title('Output of hmc_reord')

            plt.pause(0.01)

    # HMC Re-order: BRAM Input
    # ------------------------
    def hmc_reord_bram(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length):

        self.skarab()

        # Reset the plot counter
        plot_count = 0


        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg  = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']


        print "Post is %s" % post
        print "Init is %s" % init

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # -----------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_reord_bram0_ss_ctrl.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_reord_bram1_ss_ctrl.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_reord_bram_addr_a_ss_ctrl.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_reord_bram_addr_b_ss_ctrl.write(reg=1)

            print 'Arming Snapblocks done'

            #self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_en_reord.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_en_bram.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_en.write(reg=1)

            print "Grabbing HMC reord SS"
            hmc_reord_bram0 = \
                self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reord_bram0_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            hmc_reord_bram1 = \
                self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reord_bram1_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                  man_valid=valid_mode)['data']
            hmc_reord_bram_addr_a = \
                self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reord_bram_addr_a_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                  man_valid=valid_mode)['data']
            hmc_reord_bram_addr_b = \
                self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reord_bram_addr_b_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                  man_valid=valid_mode)['data']
            d00 = hmc_reord_bram0['d00']
            d01 = hmc_reord_bram0['d01']
            d02 = hmc_reord_bram0['d02']
            d03 = hmc_reord_bram0['d03']
            d04 = hmc_reord_bram0['d04']
            d05 = hmc_reord_bram0['d05']
            d06 = hmc_reord_bram0['d06']
            d07 = hmc_reord_bram0['d07']
            d10 = hmc_reord_bram1['d00']
            d11 = hmc_reord_bram1['d01']
            d12 = hmc_reord_bram1['d02']
            d13 = hmc_reord_bram1['d03']
            d14 = hmc_reord_bram1['d04']
            d15 = hmc_reord_bram1['d05']
            d16 = hmc_reord_bram1['d06']
            d17 = hmc_reord_bram1['d07']

            addr_a = hmc_reord_bram_addr_a['addr_a']
            addr_b = hmc_reord_bram_addr_b['addr_b']
            wea = hmc_reord_bram_addr_a['wea']
            enb = hmc_reord_bram_addr_b['enb']

            print "SS HMC reord grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_reord_bram0_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_reord_bram1_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_reord_bram_addr_a_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_reord_bram_addr_b_ss_ctrl.write(reg=0)

            hmc_bram_in = []

            for x in range(0, len(d00)):
                hmc_bram_in.extend([d10[x], d11[x], d12[x], d13[x],
                                  d14[x], d15[x], d16[x], d17[x],
                                  d00[x], d01[x], d02[x], d03[x],
                                  d04[x], d05[x], d06[x], d07[x]])



            print "hmc_reord in"
            print '-------------'
            print hmc_bram_in[(len(hmc_bram_in) - disp_length):len(hmc_bram_in)]
            print '                  '

            print "hmc_reord addr a"
            print '-------------'
            print addr_a[(len(addr_a) - disp_length):len(addr_a)]
            print '                  '

            print "hmc_reord addr b"
            print '-------------'
            print addr_b[(len(addr_b) - disp_length):len(addr_b)]
            print '                  '

            print "hmc_reord bram wea"
            print '-------------'
            print wea[(len(wea) - disp_length):len(wea)]
            print '                  '

            print "hmc_reord bram enb"
            print '-------------'
            print enb[(len(enb) - disp_length):len(enb)]
            print '                  '


            # Plot channel Time-series
            plt.figure(5)
            plt.ion()
            plt.clf()
            plt.subplot(211)
            plt.plot(addr_a)
            plt.title('Reord addr_a')

            plt.subplot(212)
            plt.plot(addr_b)
            plt.title('Reord addr_b')

            plt.figure(6)
            plt.ion()
            plt.clf()
            plt.subplot(211)
            plt.plot(addr_a)
            plt.title('Reord addr_a')

            plt.subplot(212)
            plt.plot(hmc_bram_in)
            plt.title('hmc_bram_in')


            plt.pause(0.01)

    # HMC Re-order: BRAM Input
    # ------------------------
    def fifo(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']

        print "Post is %s" % post
        print "Init is %s" % init

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # -----------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_fifo0_ss_ctrl.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_fifo1_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_en_fifo.write(reg=1)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_en.write(reg=1)

            print "Grabbing HMC reord SS"
            fifo0 = \
            self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_fifo0_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                  man_valid=valid_mode)['data']

            fifo1 = \
            self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_fifo1_ss.read(arm=arm_mode, man_trig=trig_mode,
                                                                                  man_valid=valid_mode)['data']

            d00 = fifo0['d00']
            d01 = fifo0['d01']
            d02 = fifo0['d02']
            d03 = fifo0['d03']
            d04 = fifo0['d04']
            d05 = fifo0['d05']
            d06 = fifo0['d06']
            d07 = fifo0['d07']
            d10 = fifo1['d00']
            d11 = fifo1['d01']
            d12 = fifo1['d02']
            d13 = fifo1['d03']
            d14 = fifo1['d04']
            d15 = fifo1['d05']
            d16 = fifo1['d06']
            d17 = fifo1['d07']

            fifo0_empty = fifo0['empty']
            fifo0_per_full = fifo0['per_full']
            fifo0_full = fifo0['full']
            fifo0_mux_sel = fifo0['mux_sel']

            fifo1_empty = fifo1['empty']
            fifo1_per_full = fifo1['per_full']
            fifo1_full = fifo1['full']
            fifo1_mux_sel = fifo1['mux_sel']


            print "SS HMC reord grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_fifo0_ss_ctrl.write(reg=0)
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_fifo1_ss_ctrl.write(reg=0)


            print '------------------------'
            print 'fifo0_empty'
            print '-------------'
            print fifo0_empty[0:disp_length]
            print ''

            print 'fifo0_per_full'
            print '-------------'
            print fifo0_per_full[0:disp_length]
            print ''

            print 'fifo0_full'
            print '-------------'
            print fifo0_full[0:disp_length]
            print ''

            print 'fifo0_mux_sel'
            print '-------------'
            print fifo0_mux_sel[0:disp_length]
            print ''

            print '------------------------'
            print 'fifo1_empty'
            print '-------------'
            print fifo1_empty[0:disp_length]
            print ''

            print 'fifo1_per_full'
            print '-------------'
            print fifo1_per_full[0:disp_length]
            print ''

            print 'fifo1_full'
            print '-------------'
            print fifo1_full[0:disp_length]
            print ''

            print 'fifo1_mux_sel'
            print '-------------'
            print fifo1_mux_sel[0:disp_length]
            print ''

            print 'Fifo Samples: D00 - D07'
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

            print 'Fifo Samples: D10 - D17'
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

    # Output of Coarse Delay
    # ----------------------
    def output_data(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg  = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']

        print "Post is %s" % post
        print "Init is %s" % init

        # Set delay for test
        self.f.registers.delay0.write(initial=0)

        self.f.registers.sync_en_cd_out.write(reg=0)
        self.f.registers.man_dvalid.write(reg=0)

        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=0)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_en.write(reg=1)

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'

            self.f.registers.cd_out_ss_ctrl.write(reg=1)

            print 'Arming Snapblocks done'

            print "Grabbing CD in SS"
            rd_data = self.f.snapshots.cd_out_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            d00 = rd_data['d00']
            d01 = rd_data['d01']
            d02 = rd_data['d02']
            d03 = rd_data['d03']
            d04 = rd_data['d04']
            d05 = rd_data['d05']
            d06 = rd_data['d06']
            d07 = rd_data['d07']

            dvalid = rd_data['dvalid']
            sync = rd_data['sync']

            print "SS CD in grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_out_ss_ctrl.write(reg=0)

            cd_out = []

            for x in range(0, len(d00)):
                cd_out.extend([d00[x], d01[x], d02[x], d03[x],
                               d04[x], d05[x], d06[x], d07[x]])


            print 'Output Samples'
            print '-------------'

            print 'dvalid'
            print '-------------'
            print dvalid[0:disp_length]

            print 'sync'
            print '-------------'
            print sync[0:disp_length]

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


            # Plot channel Time-series
            plt.figure(1)
            plt.ion()
            plt.clf()
            plt.subplot(211)
            plt.plot(d00)
            plt.title('CD Out d0')

            plt.subplot(212)
            plt.plot(cd_out)
            plt.title('cd_out')

            plt.pause(0.01)

    # Delay compare
    # -------------
    def delay_test(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length, read_length,delay, hmc_bank, hmc_vault, sync_sel):

        self.skarab()

        self.f.registers.dvalid.write(reg=0)
        self.f.registers.sync_select.write(reg=sync_sel)
        self.f.registers.man_sync.write(reg=0)

        # Reset the plot counter
        plot_count = 0

        # Set delay for test
        self.f.registers.delay0.write(initial=delay)
        time.sleep(0.1)
        print "Delay is: %s" % self.f.registers.delay0.read()


        # Disable the dvalid
        self.f.registers.dvalid.write(reg=0)

        # sync_en_cd_in and sync_en_cd_out controls which sync is used for the snapshots. sync_en_* = 1 sets the SS to use the system sync. If 0, an artificial sync is generated.
        #self.f.registers.sync_en_cd_in.write(reg=0)
        #self.f.registers.sync_en_cd_out.write(reg=0)

        # Set the addressing scheme
        self.f.registers.hmc_addr_sel_pol0.write(sel=2)
        self.f.registers.hmc_addr_sel_pol1.write(sel=2)

        # Set the vault and bank 
        self.f.registers.hmc_vault_pol0.write(vault=hmc_vault)
        self.f.registers.hmc_vault_pol1.write(vault=hmc_vault)

        self.f.registers.hmc_bank_pol0.write(bank=hmc_bank)
        self.f.registers.hmc_bank_pol1.write(bank=hmc_bank)


        # Reset sync monitor
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=1)
        time.sleep(0.1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=0)

        #Arm and load
        self.f.registers.tl_cd0_control0.write(arm=1)
        self.f.registers.tl_cd0_control0.write(load_immediate=0)
        self.f.registers.tl_cd0_control0.write(arm=0)
        time.sleep(0.1)

        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']

        print "Post is %s" % post
        print "Init is %s" % init


        # Check if HMC bank and vault are ok
        vault_pol0 = self.f.registers.hmc_vault_pol0.read()
        bank_pol0 = self.f.registers.hmc_bank_pol0.read()
        vault_pol1 = self.f.registers.hmc_vault_pol1.read()
        bank_pol1 = self.f.registers.hmc_bank_pol1.read()
        print "Pol 0 Vault is %s" % vault_pol0
        print "Pol 0 Bank is %s" % bank_pol0
        print "Pol 1 Vault is %s" % vault_pol1
        print "Pol 1 Bank is %s" % bank_pol1
        print "--------------------------------"
        print " "


        print "Initial State"
        print "-------------"

        hmc_sync_in = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in.read()
        hmc_sync_out = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out.read()
        hmc_reord_sync = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_reord_sync.read()
        reord_sync = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_out.read()

        hmc_sync_in_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in_cnt.read()
        hmc_sync_out_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out_cnt.read()
        reord_sync_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_cnt.read()


        print ''
        print 'hmc_sync_in is %s' %hmc_sync_in
        print ''
        print 'hmc_sync_in_count is %s' % hmc_sync_in_count
        print ''
        print 'hmc_sync_out is %s' % hmc_sync_out
        print ''
        print 'hmc_sync_out_count is %s' % hmc_sync_out_count
        print ''
        print 'hmc_reord_sync is %s' %hmc_reord_sync
        print ''
        print 'reord_sync is %s' %reord_sync
        print ''
        print 'reord_sync_count is %s' %reord_sync_count
        print ''
        print "-------------"

        # Setup artificial sync if needed. Reset first, then enable.
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_en.write(reg=0)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=0)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=0)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_en.write(reg=0)

        # Reset sync monitor
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=0)

        print 'Resetting Sync and Dvalid registers'

        self.f.registers.man_sys_rst.write(reg=1)
        print 'wait'
        time.sleep(0.5)
        self.f.registers.man_sys_rst.write(reg=0)

        print 'Checking Initial Sync and Dvalid'

        sync_cnt = self.f.registers.sync_cnt.read()
        sync = self.f.registers.sync.read()

        dvalid_cnt = self.f.registers.valid80_cnt.read()
        dvalid = self.f.registers.valid80.read()

        print 'Sync is %s' %sync
        print 'Sync Count is %s' %sync_cnt
        print 'dvalid is %s' %dvalid
        print 'dvalid Count is %s' %dvalid_cnt


        # Arm the Snapshot Blocks
        # -----------------------
        #print 'Arming Snapblocks'
        #self.f.registers.cd_in_ss_ctrl.write(reg=1)
        #self.f.registers.cd_out_ss_ctrl.write(reg=1)
        #self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_debug_ss_ctrl.write(reg=1)
        #self.f.registers.cd_compensation0_cd_hmc_hmc_delay_ss_tag_out_ss_ctrl.write(reg=1)

        print 'Arming Snapblocks'
        self.f.snapshots.cd_in_ss.arm()
        self.f.snapshots.cd_out_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug0_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug1_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout0_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout1_p0_ss.arm()

        print 'Arming Snapblocks done'

        # Manually set sync and dvalid
        self.f.registers.man_sync.write(reg=1)
        print 'wait'
        time.sleep(0.5)
        self.f.registers.man_sync.write(reg=0)
        time.sleep(0.5)
        self.f.registers.dvalid.write(reg=1)
        print 'wait'
        time.sleep(0.5)


        print 'Checking Post-set Sync and Dvalid'

        sync_cnt = self.f.registers.sync_cnt.read()
        sync = self.f.registers.sync.read()

        dvalid_cnt = self.f.registers.valid80_cnt.read()
        dvalid = self.f.registers.valid80.read()

        print 'Sync is %s' %sync

        print 'Sync Count is %s' %sync_cnt

        print 'dvalid is %s' %dvalid

        print 'dvalid Count is %s' %dvalid_cnt
        print 'wait'
        time.sleep(1)

        print '-----------------------------------------------------------------------------------------------'
        print "Grabbing CD in"
        data_in = self.f.snapshots.cd_in_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing HMC debug data"
        hmc_debug0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug0_p0_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']
        hmc_debug1 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug1_p0_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing HMC din"
        hmc_din0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_p0_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']
        hmc_din1 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_p0_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing HMC dout"
        hmc_dout0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout0_p0_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']
        hmc_dout1 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout1_p0_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing CD out"
        data_out = self.f.snapshots.cd_out_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']
        print '-----------------------------------------------------------------------------------------------'

        # Grab captured sync in and out of the HMC
        hmc_sync_in = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in.read()
        hmc_sync_out = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out.read()
        hmc_reord_sync = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_reord_sync.read()
        reord_sync = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_out.read()

        hmc_sync_in_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in_cnt.read()
        hmc_sync_out_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out_cnt.read()
        reord_sync_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_cnt.read()

        # CD Input data
        din_00 = data_in['d00']
        din_01 = data_in['d01']
        din_02 = data_in['d02']
        din_03 = data_in['d03']
        din_04 = data_in['d04']
        din_05 = data_in['d05']
        din_06 = data_in['d06']
        din_07 = data_in['d07']

        # HMC Input data
        hmc_din0_00 = hmc_din0['d00']
        hmc_din0_01 = hmc_din0['d01']
        hmc_din0_02 = hmc_din0['d02']
        hmc_din0_03 = hmc_din0['d03']
        hmc_din0_04 = hmc_din0['d04']
        hmc_din0_05 = hmc_din0['d05']
        hmc_din0_06 = hmc_din0['d06']
        hmc_din0_07 = hmc_din0['d07']

        hmc_din1_00 = hmc_din1['d00']
        hmc_din1_01 = hmc_din1['d01']
        hmc_din1_02 = hmc_din1['d02']
        hmc_din1_03 = hmc_din1['d03']
        hmc_din1_04 = hmc_din1['d04']
        hmc_din1_05 = hmc_din1['d05']
        hmc_din1_06 = hmc_din1['d06']
        hmc_din1_07 = hmc_din1['d07']

        # HMC Output data
        hmc_dout0_00 = hmc_din0['d00']
        hmc_dout0_01 = hmc_din0['d01']
        hmc_dout0_02 = hmc_din0['d02']
        hmc_dout0_03 = hmc_din0['d03']
        hmc_dout0_04 = hmc_din0['d04']
        hmc_dout0_05 = hmc_din0['d05']
        hmc_dout0_06 = hmc_din0['d06']
        hmc_dout0_07 = hmc_din0['d07']

        hmc_dout1_00 = hmc_din1['d00']
        hmc_dout1_01 = hmc_din1['d01']
        hmc_dout1_02 = hmc_din1['d02']
        hmc_dout1_03 = hmc_din1['d03']
        hmc_dout1_04 = hmc_din1['d04']
        hmc_dout1_05 = hmc_din1['d05']
        hmc_dout1_06 = hmc_din1['d06']
        hmc_dout1_07 = hmc_din1['d07']

        # CD Output data
        dout_00 = data_out['d00']
        dout_01 = data_out['d01']
        dout_02 = data_out['d02']
        dout_03 = data_out['d03']
        dout_04 = data_out['d04']
        dout_05 = data_out['d05']
        dout_06 = data_out['d06']
        dout_07 = data_out['d07']


        win = hmc_debug0['win']
        wr_rdy = hmc_debug0['wr_rdy']
        waddr = hmc_debug0['waddr']
        rin = hmc_debug0['rin']
        rdaddr = hmc_debug0['rdaddr']
        tag_in = hmc_debug0['tag_in']
        dvalid = hmc_debug0['dvalid']
        rd_rdy = hmc_debug0['rd_rdy']
        tag_out = hmc_debug0['tag_out']

        hmc_dvalid_p0 = hmc_debug1['dvalid']
        hmc_rd_rdy_p0 = hmc_debug1['rd_rdy']
        hmc_tag_out_p0 = hmc_debug1['tag_out']

        # Toggle the capture control to allow a small window of capture time
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=0)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl_rst.write(reg=0)

        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=1)
        time.sleep(0.1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=0)

        # Read in the counters controlled by the capture
        wr_req_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_wr_req_count.read()
        rd_req_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_rd_req_count.read()
        cd_rd_dvalid_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_rd_dvalid_count.read()

        # Read HMC delay
        hmc_delay = self.f.registers.hmc_delay.read()
        cd_in_count_thresh = self.f.registers.cd_in_cnt_thresh.read()
        cd_out_count_thresh = self.f.registers.cd_out_cnt_thresh.read()

        print 'Input Samples'
        print '-------------'

        print 'D00'
        print '-------------'
        print din_00[0:read_length]

        print 'D01'
        print '-------------'
        print din_01[0:read_length]

        print 'D02'
        print '-------------'
        print din_02[0:read_length]

        print 'D03'
        print '-------------'
        print din_03[0:read_length]

        print 'D04'
        print '-------------'
        print din_04[0:read_length]

        print 'D05'
        print '-------------'
        print din_05[0:read_length]

        print 'D06'
        print '-------------'
        print din_06[0:read_length]

        print 'D07'
        print '-------------'
        print din_07[0:read_length]
        print ''

        print 'Output Samples'
        print '-------------'

        print 'D00'
        print '-------------'
        print dout_00[disp_length:disp_length+read_length]

        print 'D01'
        print '-------------'
        print dout_01[disp_length:disp_length+read_length]

        print 'D02'
        print '-------------'
        print dout_02[disp_length:disp_length+read_length]

        print 'D03'
        print '-------------'
        print dout_03[disp_length:disp_length+read_length]

        print 'D04'
        print '-------------'
        print dout_04[disp_length:disp_length+read_length]

        print 'D05'
        print '-------------'
        print dout_05[disp_length:disp_length+read_length]

        print 'D06'
        print '-------------'
        print dout_06[disp_length:disp_length+read_length]

        print 'D07'
        print '-------------'
        print dout_07[disp_length:disp_length+read_length]
        print ''

        print '----------------------------------------------------------------------------'
        print ''
        print 'Requested delay is %s' % delay
        print ''
        print 'Latency is %s' % hmc_delay
        print ''
        print 'cd_in_count_thresh is %s' % cd_in_count_thresh
        print ''
        print 'cd_out_count_thresh is %s' % cd_out_count_thresh
        print ''

        print '----------------------------------------------------------------------------'
        print ''
        print 'hmc_sync_in is %s' % hmc_sync_in
        print ''
        print 'hmc_sync_in_count is %s' % hmc_sync_in_count
        print ''
        print 'hmc_sync_out is %s' % hmc_sync_out
        print ''
        print 'hmc_sync_out_count is %s' % hmc_sync_out_count
        print ''
        print 'hmc_wr_err is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_err.read()
        print ''
        print 'hmc_rd_err is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_rd_err.read()
        print ''
        print 'hmc_wr_rd_clash is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_rd_rdy_clash.read()
        print ''

        print '----------------------------------------------------------------------------'
        print ''
        print 'hmc_reord_sync is %s' % hmc_reord_sync
        print ''
        print 'reord_sync is %s' % reord_sync
        print ''
        print 'reord_sync_count is %s' % reord_sync_count
        print ''

        print '----------------------------------------------------------------------------'
        print ''
        print 'wr_req_count is %s' % wr_req_count
        print ''
        print 'rd_req_count is %s' % rd_req_count
        print ''
        print 'cd_rd_dvalid_count is %s' % cd_rd_dvalid_count
        print ''

        print '----------------------------------------------------------------------------'
        print ''
        print 'wr_rdy is %s' % wr_rdy[disp_length:disp_length+read_length]
        print ''
        print 'win is %s' % win[disp_length:disp_length+read_length]
        print ''
        print 'waddr is %s' % waddr[disp_length:disp_length+read_length]
        print ''
        print '----------------------------------------------------------------------------'
        print ''
        print 'rd_rdy is %s' % rd_rdy[disp_length:disp_length+read_length]
        print ''
        print 'rin is %s' % rin[disp_length:disp_length+read_length]
        print ''
        print 'rdaddr is %s' % rdaddr[disp_length:disp_length+read_length]
        print ''
        print 'tag_in is %s' % tag_in[disp_length:disp_length+read_length]
        print ''
        print 'dvalid is %s' % dvalid[disp_length:disp_length+read_length]
        print ''
        print 'tag_out is %s' % tag_out[disp_length:disp_length+read_length]
        print ''

        print '----------------------------------------------------------------------------'
        print ''
        print 'dvalid is %s' % hmc_dvalid_p0[disp_length:disp_length+read_length]
        print ''
        print 'rd_rdy is %s' % hmc_rd_rdy_p0[disp_length:disp_length+read_length]
        print ''
        print 'tag_out is %s' % hmc_tag_out_p0[disp_length:disp_length+read_length]
        print ''
        print '----------------------------------------------------------------------------'
        print ''

        print 'HMC Input Samples'
        print '-------------'

        print 'D00'
        print '-------------'
        print hmc_din0_00[0:read_length]

        print 'D01'
        print '-------------'
        print hmc_din0_01[0:read_length]

        print 'D02'
        print '-------------'
        print hmc_din0_02[0:read_length]

        print 'D03'
        print '-------------'
        print hmc_din0_03[0:read_length]

        print 'D04'
        print '-------------'
        print hmc_din0_04[0:read_length]

        print 'D05'
        print '-------------'
        print hmc_din0_05[0:read_length]

        print 'D06'
        print '-------------'
        print hmc_din0_06[0:read_length]

        print 'D07'
        print '-------------'
        print hmc_din0_07[0:read_length]
        print ''

        print 'D08'
        print '-------------'
        print hmc_din1_00[0:read_length]

        print 'D09'
        print '-------------'
        print hmc_din1_01[0:read_length]

        print 'D10'
        print '-------------'
        print hmc_din1_02[0:read_length]

        print 'D11'
        print '-------------'
        print hmc_din1_03[0:read_length]

        print 'D12'
        print '-------------'
        print hmc_din1_04[0:read_length]

        print 'D13'
        print '-------------'
        print hmc_din1_05[0:read_length]

        print 'D14'
        print '-------------'
        print hmc_din1_06[0:read_length]

        print 'D15'
        print '-------------'
        print hmc_din1_07[0:read_length]
        print ''
        print '----------------------------------------------------------------------------'

        print 'HMC Output Samples'
        print '-------------'

        print 'D00'
        print '-------------'
        print hmc_dout0_00[0:read_length]

        print 'D01'
        print '-------------'
        print hmc_dout0_01[0:read_length]

        print 'D02'
        print '-------------'
        print hmc_dout0_02[0:read_length]

        print 'D03'
        print '-------------'
        print hmc_dout0_03[0:read_length]

        print 'D04'
        print '-------------'
        print hmc_dout0_04[0:read_length]

        print 'D05'
        print '-------------'
        print hmc_dout0_05[0:read_length]

        print 'D06'
        print '-------------'
        print hmc_dout0_06[0:read_length]

        print 'D07'
        print '-------------'
        print hmc_dout0_07[0:read_length]
        print ''

        print 'D08'
        print '-------------'
        print hmc_dout1_00[0:read_length]

        print 'D09'
        print '-------------'
        print hmc_dout1_01[0:read_length]

        print 'D10'
        print '-------------'
        print hmc_dout1_02[0:read_length]

        print 'D11'
        print '-------------'
        print hmc_dout1_03[0:read_length]

        print 'D12'
        print '-------------'
        print hmc_dout1_04[0:read_length]

        print 'D13'
        print '-------------'
        print hmc_dout1_05[0:read_length]

        print 'D14'
        print '-------------'
        print hmc_dout1_06[0:read_length]

        print 'D15'
        print '-------------'
        print hmc_dout1_07[0:read_length]
        print ''
        print '----------------------------------------------------------------------------'

    # Output of HMC FIFO
    # ------------------
    def qout(self,arm_mode,trig_mode,valid_mode,plot_count_max, disp_length):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg  = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']

        print "Post is %s" % post
        print "Init is %s" % init

        # Set delay for test
        self.f.registers.delay0.write(initial=0)

        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_en_qout.write(reg=0)
        self.f.registers.man_dvalid.write(reg=0)

        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=0)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_en.write(reg=1)

        while True:

            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1

            # Arm the Snapshot Blocks
            # ------------------------

            print 'Arming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_qout_ss_ctrl.write(reg=1)
            print 'Arming Snapblocks done'

            print "Grabbing HMC FIFO SS"
            rd_data = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_qout_ss.read(arm=arm_mode, man_trig=trig_mode, man_valid=valid_mode)['data']
            d0 = rd_data['d00']
            d1 = rd_data['d01']
            d2 = rd_data['d02']
            d3 = rd_data['d03']
            d4 = rd_data['d04']
            d5 = rd_data['d05']
            d6 = rd_data['d06']
            d7 = rd_data['d07']

            print "SS HMC FIFO grab complete"

            print 'Disarming Snapblocks'
            self.f.registers.cd_compensation0_cd_hmc_hmc_delay_qout_ss_ctrl.write(reg=0)

            qout = []

            for x in range(0, len(d0)):
                qout.extend([d0[x], d1[x], d2[x], d3[x],
                               d4[x], d5[x], d6[x], d7[x]])

            # Plot channel Time-series
            plt.figure(1)
            plt.ion()
            plt.clf()
            plt.plot(qout)
            plt.title('CD HMC FIFO d0')

            plt.pause(0.01)

    # Read Tag Order
    # --------------
    def read_tag_order(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length):

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
                self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_rd_tag_in_ss.read(arm=arm_mode,
                                                                                             man_trig=trig_mode,
                                                                                             man_valid=valid_mode)['data']
                rd_tag_in = hmc_rd_tag_in['rd_tag']
                rd_tag_in_dv = hmc_rd_tag_in['dvalid']

                print "rd_tag_in"
                print rd_tag_in[0:disp_length]
                print rd_tag_in_dv[0:disp_length]

                hmc_rd_tag_out = \
                        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_rd_tag_out_ss.read(arm=arm_mode,
                                                                                              man_trig=trig_mode,
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

                # Plot channel Time-series
                plt.figure(5)
                plt.ion()
                plt.clf()
                plt.subplot(211)
                plt.plot(rd_tag_in)
                plt.title('Tag in')

                plt.subplot(212)
                plt.plot(rd_tag_out)
                plt.title('Tag out')

                # Delay compare

    # -------------
    def sync_test(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length, sync_sel):

        self.skarab()

        # Reset the plot counter
        plot_count = 0

        # Disable the dvalid
        self.f.registers.dvalid.write(reg=0)
        self.f.registers.sync_select.write(reg=sync_sel)

        while True:
            # Iterate through the bins
            if plot_count == plot_count_max:
                break

            plot_count = plot_count + 1



            print 'Resetting Sync and Dvalid registers'

            self.f.registers.man_sys_rst.write(reg=1)
            print 'wait'
            time.sleep(0.1)
            self.f.registers.man_sys_rst.write(reg=0)

            print 'Checking Initial Sync and Dvalid'

            sync_cnt = self.f.registers.sync_cnt.read()
            sync = self.f.registers.sync.read()

            dvalid_cnt = self.f.registers.valid80_cnt.read()
            dvalid = self.f.registers.valid80.read()

            print 'Sync is %s' % sync
            print 'Sync Count is %s' % sync_cnt
            print 'dvalid is %s' % dvalid
            print 'dvalid Count is %s' % dvalid_cnt


            # Arm the Snapshot Blocks
            # -----------------------

            print 'Arming Snapblocks'
            self.f.snapshots.cd_in_ss.arm()
            print 'Arming Snapblocks done'

            # Manually set sync and dvalid
            self.f.registers.man_sync.write(reg=1)
            print 'wait'
            time.sleep(0.1)
            self.f.registers.man_sync.write(reg=0)
            time.sleep(0.1)
            self.f.registers.dvalid.write(reg=1)
            print 'wait'
            time.sleep(0.1)




            print 'Checking Post-set Sync and Dvalid'

            sync_cnt = self.f.registers.sync_cnt.read()
            sync = self.f.registers.sync.read()

            dvalid_cnt = self.f.registers.valid80_cnt.read()
            dvalid = self.f.registers.valid80.read()

            print 'Sync is %s' % sync

            print 'Sync Count is %s' % sync_cnt

            print 'dvalid is %s' % dvalid

            print 'dvalid Count is %s' % dvalid_cnt
            print 'wait'
            time.sleep(1)

            print "Grabbing CD in"
            data_in = self.f.snapshots.cd_in_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

            din_00 = data_in['d00']
            din_01 = data_in['d01']
            din_02 = data_in['d02']
            din_03 = data_in['d03']
            din_04 = data_in['d04']
            din_05 = data_in['d05']
            din_06 = data_in['d06']
            din_07 = data_in['d07']


            print '---------------------------------------------------------'


            sync_cnt = self.f.registers.sync_cnt.read()
            sync = self.f.registers.sync.read()

            dvalid_cnt = self.f.registers.valid80_cnt.read()
            dvalid = self.f.registers.valid80.read()

            print 'Sync is %s' %sync

            print 'Sync Count is %s' %sync_cnt

            print 'dvalid is %s' %dvalid

            print 'dvalid Count is %s' %dvalid_cnt

            print '---------------------------------------------------------'

            print 'Input Samples'
            print '-------------'

            print 'D00'
            print '-------------'
            print din_00[0:disp_length]

            print 'D01'
            print '-------------'
            print din_01[0:disp_length]

            print 'D02'
            print '-------------'
            print din_02[0:disp_length]

            print 'D03'
            print '-------------'
            print din_03[0:disp_length]

            print 'D04'
            print '-------------'
            print din_04[0:disp_length]

            print 'D05'
            print '-------------'
            print din_05[0:disp_length]

            print 'D06'
            print '-------------'
            print din_06[0:disp_length]

            print 'D07'
            print '-------------'
            print din_07[0:disp_length]
            print ''

