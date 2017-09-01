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

    def skarab_info(self):
        print 'Grabbing System info'
        print "--------------------"

        # Specify skarab to use
        # Spare SKARAB: skarab020304-01
        skarab_ip = '10.100.205.202'

        print "Communicating to SKARAB: %s" % skarab_ip

        self.f = casperfpga.CasperFpga(skarab_ip)

        self.f.get_system_information('/tmp/s_cd_hmc_v3_pol0_2017-8-31_1217.fpg')


        print 'Grabbing System info: Done'
        print "--------------------"
        print ''


    def skarab(self):

        print 'Grabbing System info'
        print "--------------------"

        # Specify skarab to use
        # Spare SKARAB: skarab020304-01
        skarab_ip = '10.100.205.202'

        # Correlator SKARAB
        #skarab_ip = '10.100.215.134'

        print "Communicating to SKARAB: %s" % skarab_ip

        self.f = casperfpga.CasperFpga(skarab_ip)

        #self.f = casperfpga.CasperFpga('skarab0304-01')

        self.f.get_system_information('/tmp/s_cd_hmc_v3_2017-9-1_1120.fpg')

        print 'Grabbing System info: Done'
        print ''

        print "Setup multicast receive"
        #g = self.f.gbes["gbe0"]
        #g.multicast_receive?
        #g.multicast_receive('239.2.0.64', 4)

        self.g = self.f.gbes["gbe0"]
        # g.multicast_receive?
        self.g.multicast_receive('239.2.0.64', 4)

        print "Setup multicast receive done"


        print "Core details"
        self.g.print_core_details()
        print "Counters"
        self.g.read_counters()
        print "Stats"
        self.g.get_stats()

        #f.registers.status_reo0.read()
        print "RX Dest IP"
        self.f.registers.rx_dest_ip.read()
        #f.registers.forty_gbe_status.read()
        #f.snapshots.snap_adc0_ss.print_snap(man_trig=True)
        #f.registers.control.write(adc_snap_trig_select=1)
        print "--------------------"


    def setup_FPGA(self):

        # Specify skarab to use
        # Spare SKARAB: skarab020304-01
        skarab_ip = '10.100.205.202'

        # Programming file
        #prog_file = "/tmp/s_cd_hmc_v2_pol0_2017-6-28_1459.fpg"

        prog_file = "/tmp/s_cd_hmc_v3_2017-9-1_1120.fpg"
        #prog_file = "/tmp/s_cd_hmc_v3_pol0_2017-8-31_1217.fpg"

        # Create FPGA Object
        #self.f = casperfpga.SkarabFpga(skarab_ip)
        self.f = casperfpga.CasperFpga(skarab_ip)

        print 'FPGA Object Created'

        try:
            self.f.upload_to_ram_and_program(prog_file)
            print "Programming FPGA done"

        except:
            print "Programming Failed"

    def setup_FPGA_feng(self):

        # Specify skarab to use
        # Spare SKARAB: skarab020304-01
        skarab_ip = '10.100.205.202'

        # Correlator SKARAB
        #skarab_ip = '10.100.215.134'


        # Programming file
        #prog_file = "/tmp/s_c856m4k_cd_2017-7-5_0954.fpg"
        prog_file = "/tmp/s_c856m4k_cd_2017-7-26_1427.fpg"

        # Create FPGA Object
        self.f = casperfpga.CasperFpga(skarab_ip)

        print 'FPGA Object Created'

        try:
            print "Programming SKARAB: %s" % skarab_ip
            self.f.upload_to_ram_and_program(prog_file)
            print "Programming FPGA done"

        except:
            print "Programming Failed"

    def prog_deng(self):

        # Specify skarab to use
        deng_ip = '192.168.65.195'

        # Programming file
        prog_file = "/tmp/r2_deng_tvg_rev1_13.fpg"

        # Create FPGA Object
        self.d = casperfpga.CasperFpga(deng_ip)

        try:
            self.d.upload_to_ram_and_program(prog_file)
            print "Programming Deng done"

        except:
            print "Programming Failed"


    def config_deng(self):

        self.d = casperfpga.CasperFpga('192.168.65.195')
        self.d.get_system_information()

        self.d.registers.control.write(tvg_select0=1)
        self.d.registers.control.write(tvg_select1=1)

        self.d.registers.src_sel_cntrl.write(src_sel_0=0)
        self.d.registers.src_sel_cntrl.write(src_sel_1=0)

        self.d.registers.start_load_time_msw.write(reg=0)
        self.d.registers.start_load_time_lsw.write(reg=0)
        self.d.registers.stop_load_time_msw.write(reg=0)
        self.d.registers.stop_load_time_lsw.write(reg=0)

        self.d.registers.scale_cwg0.write(scale=0.5)
        self.d.registers.scale_out0.write(scale=1)
        self.d.registers.freq_cwg0.write(frequency=100000)

        self.d.registers.pol_tx_always_on.write(pol0_tx_always_on=1)
        self.d.registers.pol_tx_always_on.write(pol1_tx_always_on=1)

        self.d.registers.control.write(gbe_txen=1)
        self.d.registers.gbecontrol.write(gbe0=1)
        self.d.registers.gbecontrol.write(gbe1=1)
        self.d.registers.gbecontrol.write(gbe2=1)
        self.d.registers.gbecontrol.write(gbe3=1)


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




    # Test: CD Pol0 Only
    # ------------------
    def delay_test(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length, read_length,delay, hmc_bank, hmc_vault, sync_sel):

        self.skarab()

        # Disable the dvalid
        self.f.registers.dvalid.write(reg=0)

        self.f.registers.control.write(sys_rst=1)
        self.f.registers.control.write(sys_rst=0)

        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_clear_hmc.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_clear_hmc.write(reg=0)

        #self.f.registers.addr_map_sel.write(reg=2)
        self.f.registers.sync_select.write(reg=sync_sel)
        self.f.registers.man_sync.write(reg=0)

        # Reset the plot counter
        plot_count = 0

        # Set delay for test
        self.f.registers.delay0.write(initial=delay)

        # sync_en_cd_in and sync_en_cd_out controls which sync is used for the snapshots. sync_en_* = 1 sets the SS to use the system sync. If 0, an artificial sync is generated.
        #self.f.registers.sync_en_cd_in.write(reg=0)
        #self.f.registers.sync_en_cd_out.write(reg=0)

        # Set the addressing scheme
        #self.f.registers.hmc_addr_sel_pol0.write(sel=2)
        #self.f.registers.hmc_addr_sel_pol1.write(sel=2)

        # Set the vault and bank
        #self.f.registers.hmc_vault_pol0.write(vault=hmc_vault)
        #self.f.registers.hmc_vault_pol1.write(vault=hmc_vault)

        #self.f.registers.hmc_bank_pol0.write(bank=hmc_bank)
        #self.f.registers.hmc_bank_pol1.write(bank=hmc_bank)


        # Reset sync monitor
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=0)

        #Arm and load
        self.f.registers.tl_cd0_control0.write(arm=1)
        self.f.registers.tl_cd0_control0.write(load_immediate=0)
        self.f.registers.tl_cd0_control0.write(arm=0)

        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']

        print "System Information"
        print "------------------"
        print 'Requested delay is %s' % delay
        print "Actual Delay is: %s" % self.f.registers.delay0.read()
        print " "

        print "HMC Status"
        print "----------"
        print "Post is %s" % post
        print "Init is %s" % init
        print " "

        print 'Checking Initial Sync and Dvalid states'
        print "---------------------------------------"

        print ''
        print 'Sync in is %s' % self.f.registers.sync.read()
        print 'Sync in count is %s' % self.f.registers.sync_cnt.read()
        print ''
        print 'Dvalid in is %s' % self.f.registers.valid80.read()
        print 'Dvalid in count is %s' % self.f.registers.valid80_cnt.read()
        print ''
        print 'hmc_sync_in is %s' %self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in.read()
        print 'hmc_sync_in_count is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in_cnt.read()
        print ''
        print 'hmc_sync_out is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out.read()
        print 'hmc_sync_out_count is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out_cnt.read()
        print ''
        print 'reord_sync is %s' %self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_out.read()
        print 'reord_sync_count is %s' %self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_cnt.read()
        print ''

        # Setup artificial sync if needed. Reset first, then enable.
        #self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_en.write(reg=0)
        #self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=0)
        #self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_rst.write(reg=0)
        #self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_counter_en.write(reg=0)

        # Reset sync monitor
        #self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=1)
        #self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=0)

        #print 'Resetting Sync and Dvalid registers'
        #self.f.registers.man_sys_rst.write(reg=1)
        #time.sleep(0.2)
        #self.f.registers.man_sys_rst.write(reg=0)
        #time.sleep(0.2)

        # Arm the Snapshot Blocks
        # -----------------------
        print 'Arming Snapblocks'
        print "-----------------"
        self.f.snapshots.cd_in_ss.arm()
        self.f.snapshots.cd_out_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug0_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug1_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout0_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout1_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord1_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_fifo0_ss.arm()
        #self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_fifo1_ss.arm()

        print 'Arming Snapblocks done'
        print "----------------------"

        print 'Check HMC clear done'
        print "--------------------"



        # Manually set sync and dvalid
        self.f.registers.man_sync.write(reg=1)
        self.f.registers.man_sync.write(reg=0)
        self.f.registers.dvalid.write(reg=1)

        print 'Checking Post-set Sync and Dvalid'
        print "---------------------------------"

        print 'Sync in is %s' %self.f.registers.sync.read()
        print 'Sync Count is %s' %self.f.registers.sync_cnt.read()
        print ''
        print 'Dvalid in is %s' %self.f.registers.valid80_cnt.read()
        print 'Dvalid Count is %s' %self.f.registers.valid80_cnt.read()
        print ''

        print 'Grabbing Snapshot Data'
        print "----------------------"

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

        print "Grabbing Reorder"
        hmc_reord0 = \
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord0_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']
        hmc_reord1 = \
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord1_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing FIFO"
        fifo0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_fifo0_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing CD out"
        data_out = self.f.snapshots.cd_out_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        # Grab captured sync in and out of the HMC
        hmc_sync_in = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in.read()
        hmc_sync_out = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out.read()

        hmc_sync_in_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in_cnt.read()
        hmc_sync_out_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out_cnt.read()

        #reord_sync = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_out.read()
        #reord_sync_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_cnt.read()

        # CD Input data
        din_00 = data_in['d00']
        din_01 = data_in['d01']
        din_02 = data_in['d02']
        din_03 = data_in['d03']
        din_04 = data_in['d04']
        din_05 = data_in['d05']
        din_06 = data_in['d06']
        din_07 = data_in['d07']
        
        cd_in_sync = data_in['sync']
        cd_in_dvalid = data_in['dvalid']

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
        hmc_dout0_00 = hmc_dout0['d00']
        hmc_dout0_01 = hmc_dout0['d01']
        hmc_dout0_02 = hmc_dout0['d02']
        hmc_dout0_03 = hmc_dout0['d03']
        hmc_dout0_04 = hmc_dout0['d04']
        hmc_dout0_05 = hmc_dout0['d05']
        hmc_dout0_06 = hmc_dout0['d06']
        hmc_dout0_07 = hmc_dout0['d07']

        hmc_dout1_00 = hmc_dout1['d00']
        hmc_dout1_01 = hmc_dout1['d01']
        hmc_dout1_02 = hmc_dout1['d02']
        hmc_dout1_03 = hmc_dout1['d03']
        hmc_dout1_04 = hmc_dout1['d04']
        hmc_dout1_05 = hmc_dout1['d05']
        hmc_dout1_06 = hmc_dout1['d06']
        hmc_dout1_07 = hmc_dout1['d07']

        # Reorder data
        r00 = hmc_reord0['d00']
        r01 = hmc_reord0['d01']
        r02 = hmc_reord0['d02']
        r03 = hmc_reord0['d03']
        r04 = hmc_reord0['d04']
        r05 = hmc_reord0['d05']
        r06 = hmc_reord0['d06']
        r07 = hmc_reord0['d07']
        r10 = hmc_reord1['d00']
        r11 = hmc_reord1['d01']
        r12 = hmc_reord1['d02']
        r13 = hmc_reord1['d03']
        r14 = hmc_reord1['d04']
        r15 = hmc_reord1['d05']
        r16 = hmc_reord1['d06']
        r17 = hmc_reord1['d07']
        ss_reord_dvalid = hmc_reord0['dvalid']
        ss_reord_sync = hmc_reord0['sync']


        # FIFO data
        f00 = fifo0['d00']
        f01 = fifo0['d01']
        f02 = fifo0['d02']
        f03 = fifo0['d03']
        f04 = fifo0['d04']
        f05 = fifo0['d05']
        f06 = fifo0['d06']
        f07 = fifo0['d07']
        #f10 = fifo1['d00']
        #f11 = fifo1['d01']
        #f12 = fifo1['d02']
        #f13 = fifo1['d03']
        #f14 = fifo1['d04']
        #f15 = fifo1['d05']
        #f16 = fifo1['d06']
        #f17 = fifo1['d07']

        #fifo0_empty = fifo0['empty']
        #fifo0_per_full = fifo0['per_full']
        #fifo0_full = fifo0['full']
        fifo0_mux_sel = fifo0['mux_sel']

        #fifo1_empty = fifo1['empty']
        #fifo1_per_full = fifo1['per_full']
        #fifo1_full = fifo1['full']
        #fifo1_mux_sel = fifo1['mux_sel']

        fifo0_dvalid = fifo0['dvalid']
        fifo0_sync = fifo0['sync']

        #fifo1_dvalid = fifo1['dvalid']
        #fifo1_sync = fifo1['sync']

        #fifo0_re = fifo0['re']
        #fifo1_re = fifo1['re']

        # CD Output data
        dout_00 = data_out['d00']
        dout_01 = data_out['d01']
        dout_02 = data_out['d02']
        dout_03 = data_out['d03']
        dout_04 = data_out['d04']
        dout_05 = data_out['d05']
        dout_06 = data_out['d06']
        dout_07 = data_out['d07']

        cd_out_sync = data_out['sync']
        cd_out_dvalid = data_out['dvalid']

        hmc_debug0_win = hmc_debug0['win']
        hmc_debug0_wr_rdy = hmc_debug0['wr_rdy']
        hmc_debug0_waddr = hmc_debug0['waddr']
        hmc_debug0_rin = hmc_debug0['rin']
        hmc_debug0_rdaddr = hmc_debug0['rdaddr']
        hmc_debug0_tag_in = hmc_debug0['tag_in']
        hmc_debug0_rd_rdy = hmc_debug0['rd_rdy']
        hmc_debug0_tag_out = hmc_debug0['tag_out']

        hmc_debug1_dvalid_p0 = hmc_debug1['dvalid']
        hmc_debug1_wr_rdy_p0 = hmc_debug1['wr_rdy']
        hmc_debug1_rd_rdy_p0 = hmc_debug1['rd_rdy']
        hmc_debug1_tag_out_p0 = hmc_debug1['tag_out']

        # Toggle the capture control to allow a small window of capture time
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=0)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl_rst.write(reg=0)

        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=0)

        # Read in the counters controlled by the capture
        wr_req_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_wr_req_count.read()
        rd_req_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_rd_req_count.read()
        cd_rd_dvalid_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_rd_dvalid_count.read()

        print ''
        print 'Latency Check'
        print "-------------"
        print 'Latency is %s' % self.f.registers.hmc_delay.read()
        print ''
        print 'cd_in_count_thresh is %s' % self.f.registers.cd_in_cnt_thresh.read()
        print ''
        print 'cd_out_count_thresh is %s' % self.f.registers.cd_out_cnt_thresh.read()
        print ''

        print 'Input Samples'
        print '-------------'

        print 'sync in is %s' % cd_in_sync[0:read_length]
        print 'dvalid in is %s' % cd_in_dvalid[0:read_length]
        print ' '

        print 'D00'
        print '---'
        print din_00[0:read_length]

        print 'D01'
        print '---'
        print din_01[0:read_length]

        print 'D02'
        print '---'
        print din_02[0:read_length]

        print 'D03'
        print '---'
        print din_03[0:read_length]

        print 'D04'
        print '---'
        print din_04[0:read_length]

        print 'D05'
        print '---'
        print din_05[0:read_length]

        print 'D06'
        print '---'
        print din_06[0:read_length]

        print 'D07'
        print '---'
        print din_07[0:read_length]
        print ''

        print 'Output Samples'
        print '--------------'

        print 'sync out is %s' % cd_out_sync[0:read_length]
        print 'dvalid out is %s' % cd_out_dvalid[0:read_length]
        print ' '

        print 'D00'
        print '---'
        print dout_00[disp_length:disp_length+read_length]

        print 'D01'
        print '---'
        print dout_01[disp_length:disp_length+read_length]

        print 'D02'
        print '---'
        print dout_02[disp_length:disp_length+read_length]

        print 'D03'
        print '---'
        print dout_03[disp_length:disp_length+read_length]

        print 'D04'
        print '---'
        print dout_04[disp_length:disp_length+read_length]

        print 'D05'
        print '---'
        print dout_05[disp_length:disp_length+read_length]

        print 'D06'
        print '---'
        print dout_06[disp_length:disp_length+read_length]

        print 'D07'
        print '---'
        print dout_07[disp_length:disp_length+read_length]
        print ''

        print 'HMC Debug'
        print '---------'
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
        print 'wr_req_count is %s' % wr_req_count
        print ''
        print 'rd_req_count is %s' % rd_req_count
        print ''
        print 'cd_rd_dvalid_count is %s' % cd_rd_dvalid_count
        print ''


        print 'HMC Input Samples'
        print '-----------------'
        print 'wr_rdy is %s' % hmc_debug0_wr_rdy[0:read_length]
        print ''
        print 'win is %s' % hmc_debug0_win[0:read_length]
        print ''
        print 'waddr is %s' % hmc_debug0_waddr[0:read_length]
        print ''
        print 'rd_rdy is %s' % hmc_debug0_rd_rdy[0:read_length]
        print ''
        print 'rin is %s' % hmc_debug0_rin[0:read_length]
        print ''
        print 'rdaddr is %s' % hmc_debug0_rdaddr[0:read_length]
        print ''
        print 'tag_in is %s' % hmc_debug0_tag_in[0:read_length]
        print ''
        print 'tag_out is %s' % hmc_debug0_tag_out[0:read_length]
        print ''

        print 'D00'
        print '---'
        print hmc_din0_00[0:read_length]

        print 'D01'
        print '---'
        print hmc_din0_01[0:read_length]

        print 'D02'
        print '---'
        print hmc_din0_02[0:read_length]

        print 'D03'
        print '---'
        print hmc_din0_03[0:read_length]

        print 'D04'
        print '---'
        print hmc_din0_04[0:read_length]

        print 'D05'
        print '---'
        print hmc_din0_05[0:read_length]

        print 'D06'
        print '---'
        print hmc_din0_06[0:read_length]

        print 'D07'
        print '---'
        print hmc_din0_07[0:read_length]
        print ''

        print 'D08'
        print '---'
        print hmc_din1_00[0:read_length]

        print 'D09'
        print '---'
        print hmc_din1_01[0:read_length]

        print 'D10'
        print '---'
        print hmc_din1_02[0:read_length]

        print 'D11'
        print '---'
        print hmc_din1_03[0:read_length]

        print 'D12'
        print '---'
        print hmc_din1_04[0:read_length]

        print 'D13'
        print '---'
        print hmc_din1_05[0:read_length]

        print 'D14'
        print '---'
        print hmc_din1_06[0:read_length]

        print 'D15'
        print '---'
        print hmc_din1_07[0:read_length]
        print ''


        print 'HMC Output Samples'
        print '------------------'
        print 'dvalid is %s' % hmc_debug1_dvalid_p0[0:read_length]
        print ''
        print 'wr_rdy is %s' % hmc_debug1_wr_rdy_p0[0:read_length]
        print ''
        print 'rd_rdy is %s' % hmc_debug1_rd_rdy_p0[0:read_length]
        print ''
        print 'tag_out is %s' % hmc_debug1_tag_out_p0[0:read_length]
        print ''

        print 'D00'
        print '---'
        print hmc_dout0_00[0:read_length]

        print 'D01'
        print '---'
        print hmc_dout0_01[0:read_length]

        print 'D02'
        print '---'
        print hmc_dout0_02[0:read_length]

        print 'D03'
        print '---'
        print hmc_dout0_03[0:read_length]

        print 'D04'
        print '---'
        print hmc_dout0_04[0:read_length]

        print 'D05'
        print '---'
        print hmc_dout0_05[0:read_length]

        print 'D06'
        print '---'
        print hmc_dout0_06[0:read_length]

        print 'D07'
        print '---'
        print hmc_dout0_07[0:read_length]
        print ''

        print 'D08'
        print '---'
        print hmc_dout1_00[0:read_length]

        print 'D09'
        print '---'
        print hmc_dout1_01[0:read_length]

        print 'D10'
        print '---'
        print hmc_dout1_02[0:read_length]

        print 'D11'
        print '---'
        print hmc_dout1_03[0:read_length]

        print 'D12'
        print '---'
        print hmc_dout1_04[0:read_length]

        print 'D13'
        print '---'
        print hmc_dout1_05[0:read_length]

        print 'D14'
        print '---'
        print hmc_dout1_06[0:read_length]

        print 'D15'
        print '---'
        print hmc_dout1_07[0:read_length]
        print ''


        print 'Reorder Debug'
        print '-------------'
        print 'reord_sync is %s' %self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_out.read()
        print ''
        print 'reord_sync_count is %s' %self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_cnt.read()
        print ''
        print 'reord_sync SS is %s' % ss_reord_sync[0:read_length]
        print ''
        print 'reord_dvalid SS is %s' % ss_reord_dvalid[0:read_length]
        print ''

        print 'Reorder Data'
        print '------------'

        print 'D00'
        print '---'
        print r00[0:read_length]

        print 'D01'
        print '---'
        print r01[0:read_length]

        print 'D02'
        print '---'
        print r02[0:read_length]

        print 'D03'
        print '---'
        print r03[0:read_length]

        print 'D04'
        print '---'
        print r04[0:read_length]

        print 'D05'
        print '---'
        print r05[0:read_length]

        print 'D06'
        print '---'
        print r06[0:read_length]

        print 'D07'
        print '---'
        print r07[0:read_length]
        print ''

        print 'D08'
        print '---'
        print r10[0:read_length]

        print 'D09'
        print '---'
        print r11[0:read_length]

        print 'D10'
        print '---'
        print r12[0:read_length]

        print 'D11'
        print '---'
        print r13[0:read_length]

        print 'D12'
        print '---'
        print r14[0:read_length]

        print 'D13'
        print '---'
        print r15[0:read_length]

        print 'D14'
        print '---'
        print r16[0:read_length]

        print 'D15'
        print '---'
        print r17[0:read_length]
        print ''


        print 'FIFO Debug'
        print '----------'
        print 'fifo0_mux_sel is %s' % fifo0_mux_sel[0:read_length]
        print ''
        print 'fifo0_sync is %s' % fifo0_sync[0:read_length]
        print ''
        print 'fifo0_dvalid is %s' % fifo0_dvalid[0:read_length]
        print ''

        print 'FIFO Data'
        print '---------'
        print 'D00'
        print '---'
        print f00[0:read_length]

        print 'D01'
        print '---'
        print f01[0:read_length]

        print 'D02'
        print '---'
        print f02[0:read_length]

        print 'D03'
        print '---'
        print f03[0:read_length]

        print 'D04'
        print '---'
        print f04[0:read_length]

        print 'D05'
        print '---'
        print f05[0:read_length]

        print 'D06'
        print '---'
        print f06[0:read_length]

        print 'D07'
        print '---'
        print f07[0:read_length]
        print ''

        # Disable the dvalid
        self.f.registers.dvalid.write(reg=0)

        # Delay compare
        # -------------

    # Test: CD Pol0 and Pol1
    # ----------------------
    def delay_test_dual_pol(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length, read_length, delay, hmc_bank,
                   hmc_vault, sync_sel):

        self.skarab()

        # Disable the dvalid
        self.f.registers.dvalid.write(reg=0)

        self.f.registers.control.write(sys_rst=1)
        self.f.registers.control.write(sys_rst=0)

        self.f.registers.addr_map_sel.write(reg=2)
        self.f.registers.sync_select.write(reg=sync_sel)
        self.f.registers.man_sync.write(reg=0)

        # Reset the plot counter
        plot_count = 0

        # Set delay for test
        self.f.registers.delay0.write(initial=delay)
        self.f.registers.delay1.write(initial=delay)

        # Reset sync monitor
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=0)

        # Arm and load
        self.f.registers.tl_cd0_control0.write(arm=1)
        self.f.registers.tl_cd0_control0.write(load_immediate=0)
        self.f.registers.tl_cd0_control0.write(arm=0)

        self.f.registers.tl_cd1_control0.write(arm=1)
        self.f.registers.tl_cd1_control0.write(load_immediate=0)
        self.f.registers.tl_cd1_control0.write(arm=0)

        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']

        print "System Information"
        print "------------------"
        print 'Requested delay is %s' % delay
        print "Actual Delay is: %s" % self.f.registers.delay0.read()
        print " "

        print "HMC Status"
        print "----------"
        print "Post is %s" % post
        print "Init is %s" % init
        print " "

        print 'Checking Initial Sync and Dvalid states'
        print "---------------------------------------"

        print ''
        print 'Sync in is %s' % self.f.registers.sync.read()
        print 'Sync in count is %s' % self.f.registers.sync_cnt.read()
        print ''
        print 'Dvalid in is %s' % self.f.registers.valid80.read()
        print 'Dvalid in count is %s' % self.f.registers.valid80_cnt.read()
        print ''
        print 'hmc_sync_in is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in.read()
        print 'hmc_sync_in_count is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in_cnt.read()
        print ''
        print 'hmc_sync_out is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out.read()
        print 'hmc_sync_out_count is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out_cnt.read()
        print ''
        print 'reord_sync is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_out.read()
        print 'reord_sync_count is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_cnt.read()
        print ''

        # Arm the Snapshot Blocks
        # -----------------------
        print 'Arming Snapblocks'
        print "-----------------"
        self.f.snapshots.cd_in_ss.arm()
        self.f.snapshots.cd_out_ss.arm()
        self.f.snapshots.cd_out1_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug0_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug1_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout0_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout1_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord1_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_fifo0_ss.arm()

        print 'Arming Snapblocks done'
        print "----------------------"

        # Manually set sync and dvalid
        self.f.registers.man_sync.write(reg=1)
        self.f.registers.man_sync.write(reg=0)
        self.f.registers.dvalid.write(reg=1)

        print 'Checking Post-set Sync and Dvalid'
        print "---------------------------------"

        print 'Sync in is %s' % self.f.registers.sync.read()
        print 'Sync Count is %s' % self.f.registers.sync_cnt.read()
        print ''
        print 'Dvalid in is %s' % self.f.registers.valid80_cnt.read()
        print 'Dvalid Count is %s' % self.f.registers.valid80_cnt.read()
        print ''

        print 'Grabbing Snapshot Data'
        print "----------------------"

        print "Grabbing CD in"
        data_in = self.f.snapshots.cd_in_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing HMC debug data"
        hmc_debug0 = \
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug0_p0_ss.read(arm=False, man_trig=trig_mode,
                                                                                 man_valid=valid_mode)['data']
        hmc_debug1 = \
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug1_p0_ss.read(arm=False, man_trig=trig_mode,
                                                                                 man_valid=valid_mode)['data']

        print "Grabbing HMC din"
        hmc_din0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_p0_ss.read(arm=False, man_trig=trig_mode,
                                                                                          man_valid=valid_mode)['data']
        hmc_din1 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_p0_ss.read(arm=False, man_trig=trig_mode,
                                                                                          man_valid=valid_mode)['data']

        print "Grabbing CD out"
        data_out_pol0 = self.f.snapshots.cd_out_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        data_out_pol1 = self.f.snapshots.cd_out1_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        # Grab captured sync in and out of the HMC
        hmc_sync_in = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in.read()
        hmc_sync_out = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out.read()

        hmc_sync_in_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in_cnt.read()
        hmc_sync_out_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out_cnt.read()

        # CD Input data
        din_00 = data_in['d00']
        din_01 = data_in['d01']
        din_02 = data_in['d02']
        din_03 = data_in['d03']
        din_04 = data_in['d04']
        din_05 = data_in['d05']
        din_06 = data_in['d06']
        din_07 = data_in['d07']

        cd_in_sync = data_in['sync']
        cd_in_dvalid = data_in['dvalid']

        # CD Output data
        dout_00 = data_out_pol0['d00']
        dout_01 = data_out_pol0['d01']
        dout_02 = data_out_pol0['d02']
        dout_03 = data_out_pol0['d03']
        dout_04 = data_out_pol0['d04']
        dout_05 = data_out_pol0['d05']
        dout_06 = data_out_pol0['d06']
        dout_07 = data_out_pol0['d07']

        dout_10 = data_out_pol1['d00']
        dout_11 = data_out_pol1['d01']
        dout_12 = data_out_pol1['d02']
        dout_13 = data_out_pol1['d03']
        dout_14 = data_out_pol1['d04']
        dout_15 = data_out_pol1['d05']
        dout_16 = data_out_pol1['d06']
        dout_17 = data_out_pol1['d07']

        cd_out_sync = data_out_pol0['sync']
        cd_out_dvalid = data_out_pol0['dvalid']

        hmc_debug0_win = hmc_debug0['win']
        hmc_debug0_wr_rdy = hmc_debug0['wr_rdy']
        hmc_debug0_waddr = hmc_debug0['waddr']
        hmc_debug0_rin = hmc_debug0['rin']
        hmc_debug0_rdaddr = hmc_debug0['rdaddr']
        hmc_debug0_tag_in = hmc_debug0['tag_in']
        hmc_debug0_rd_rdy = hmc_debug0['rd_rdy']
        hmc_debug0_tag_out = hmc_debug0['tag_out']

        hmc_debug1_dvalid_p0 = hmc_debug1['dvalid']
        hmc_debug1_wr_rdy_p0 = hmc_debug1['wr_rdy']
        hmc_debug1_rd_rdy_p0 = hmc_debug1['rd_rdy']
        hmc_debug1_tag_out_p0 = hmc_debug1['tag_out']

        # Toggle the capture control to allow a small window of capture time
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=0)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl_rst.write(reg=0)

        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=0)

        # Read in the counters controlled by the capture
        wr_req_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_wr_req_count.read()
        rd_req_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_rd_req_count.read()
        cd_rd_dvalid_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_rd_dvalid_count.read()

        print ''
        print 'Latency Check'
        print "-------------"
        print 'Latency is %s' % self.f.registers.hmc_delay.read()
        print ''
        print 'cd_in_count_thresh is %s' % self.f.registers.cd_in_cnt_thresh.read()
        print ''
        print 'cd_out_count_thresh is %s' % self.f.registers.cd_out_cnt_thresh.read()
        print ''

        print 'Input Samples'
        print '-------------'

        print 'sync in is %s' % cd_in_sync[0:read_length]
        print 'dvalid in is %s' % cd_in_dvalid[0:read_length]
        print ' '

        print 'D00'
        print '---'
        print din_00[0:read_length]

        print 'D01'
        print '---'
        print din_01[0:read_length]

        print 'D02'
        print '---'
        print din_02[0:read_length]

        print 'D03'
        print '---'
        print din_03[0:read_length]

        print 'D04'
        print '---'
        print din_04[0:read_length]

        print 'D05'
        print '---'
        print din_05[0:read_length]

        print 'D06'
        print '---'
        print din_06[0:read_length]

        print 'D07'
        print '---'
        print din_07[0:read_length]
        print ''

        print 'Output Samples: Pol0'
        print '--------------------'

        print 'sync out is %s' % cd_out_sync[0:read_length]
        print 'dvalid out is %s' % cd_out_dvalid[0:read_length]
        print ' '

        print 'D00'
        print '---'
        print dout_00[disp_length:disp_length + read_length]

        print 'D01'
        print '---'
        print dout_01[disp_length:disp_length + read_length]

        print 'D02'
        print '---'
        print dout_02[disp_length:disp_length + read_length]

        print 'D03'
        print '---'
        print dout_03[disp_length:disp_length + read_length]

        print 'D04'
        print '---'
        print dout_04[disp_length:disp_length + read_length]

        print 'D05'
        print '---'
        print dout_05[disp_length:disp_length + read_length]

        print 'D06'
        print '---'
        print dout_06[disp_length:disp_length + read_length]

        print 'D07'
        print '---'
        print dout_07[disp_length:disp_length + read_length]
        print ''

        print 'Output Samples: Pol1'
        print '--------------------'
        print 'D00'
        print '---'
        print dout_10[disp_length:disp_length + read_length]

        print 'D01'
        print '---'
        print dout_11[disp_length:disp_length + read_length]

        print 'D02'
        print '---'
        print dout_12[disp_length:disp_length + read_length]

        print 'D03'
        print '---'
        print dout_13[disp_length:disp_length + read_length]

        print 'D04'
        print '---'
        print dout_14[disp_length:disp_length + read_length]

        print 'D05'
        print '---'
        print dout_15[disp_length:disp_length + read_length]

        print 'D06'
        print '---'
        print dout_16[disp_length:disp_length + read_length]

        print 'D07'
        print '---'
        print dout_17[disp_length:disp_length + read_length]
        print ''

        print 'HMC Debug'
        print '---------'
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
        #print ''
        #print 'hmc_wr_err is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_err_pol1.read()
        #print ''
        #print 'hmc_rd_err is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_rd_err_pol1.read()
        #print ''
        #print 'hmc_wr_rd_clash is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_rd_rdy_clash_pol1.read()
        print ''
        print 'wr_req_count is %s' % wr_req_count
        print ''
        print 'rd_req_count is %s' % rd_req_count
        print ''
        print 'cd_rd_dvalid_count is %s' % cd_rd_dvalid_count
        print ''


        # Disable the dvalid
        self.f.registers.dvalid.write(reg=0)

    # Test: FEng front-end with CD
    # ----------------------------
    def feng_cd(self, arm_mode, trig_mode, valid_mode, read_length, delay, offset):

        self.skarab()

        # Set the trig_arm
        self.f.registers.control.write(adc_snap_arm=0)

        # Set Impulse values
        self.f.registers.impulse0.write(offset=0)
        self.f.registers.impulse0.write(amplitude=0.5)

        self.f.registers.impulse1.write(offset=0)
        self.f.registers.impulse1.write(amplitude=0.5)



        # Set delay for test
        self.f.registers.delay0.write(initial=delay)
        self.f.registers.delay1.write(initial=delay)

        # Arm and load
        #self.f.registers.tl_cd0_control0.write(arm=1)
        #self.f.registers.tl_cd0_control0.write(load_immediate=1)
        #self.f.registers.tl_cd0_control0.write(arm=0)

        #self.f.registers.tl_cd1_control0.write(arm=1)
        #self.f.registers.tl_cd1_control0.write(load_immediate=1)
        #self.f.registers.tl_cd1_control0.write(arm=0)

        self.f.registers.tl_cd0_control.write(arm=1)
        self.f.registers.tl_cd0_control.write(load_immediate=1)
        self.f.registers.tl_cd0_control.write(arm=0)

        self.f.registers.tl_cd1_control.write(arm=1)
        self.f.registers.tl_cd1_control.write(load_immediate=1)
        self.f.registers.tl_cd1_control.write(arm=0)

        # Enable the TVG
        self.f.registers.control.write(tvg_adc=1)

        # Reset sync monitor
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=0)

        # Set the Snap trig time (if used)
        self.f.registers.trig_time_msw.write(msw=0)
        self.f.registers.trig_time_lsw.write(lsw=0)

        # Set the Snap trig source
        self.f.registers.control.write(adc_snap_trig_select=1)

        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']

        print "System Information"
        print "------------------"
        print 'Requested delay is %s' % delay
        print "Actual Delay is: %s" % self.f.registers.delay0.read()
        print "Loaded value is: %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_delay.read()
        print " "
        print "Amplitude and Offset P0 is %s" % self.f.registers.impulse0.read()
        print "Amplitude and Offset P1 is %s" % self.f.registers.impulse1.read()
        print " "

        print "HMC Status"
        print "----------"
        print "Post is %s" % post
        print "Init is %s" % init
        print " "

        print 'Checking Initial Sync and Dvalid states'
        print "---------------------------------------"

        print ''
        print 'hmc_sync_in is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in.read()
        print 'hmc_sync_in_count is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in_cnt.read()
        print ''
        print 'hmc_sync_out is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out.read()
        print 'hmc_sync_out_count is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out_cnt.read()
        print ''
        print 'reord_sync is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_out.read()
        print 'reord_sync_count is %s' % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_reord_sync_cnt.read()
        print ''

        # Set trig offsets
        self.f.registers.cd_out_ss_trig_offset.write(reg=offset)
        self.f.registers.cd_out1_ss_trig_offset.write(reg=offset)


        # Arm the Snapshot Blocks
        # -----------------------
        print 'Arming Snapblocks'
        print "-----------------"
        self.f.snapshots.snap_adc0_ss.arm()
        self.f.snapshots.snap_adc1_ss.arm()

        self.f.snapshots.cd_out_ss.arm()
        self.f.snapshots.cd_out1_ss.arm()

        self.f.snapshots.reord_addr_db_ss.arm()

        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug0_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug1_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout0_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_dout1_p0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord0_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_reord1_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_fifo0_ss.arm()


        print 'Arming Snapblocks done'
        print "----------------------"

        print 'Starting TVG'
        print "------------"

        # Force a relock
        self.f.registers.control.write(sys_rst=1)
        self.f.registers.control.write(sys_rst=0)

        # Set the trig_arm
        self.f.registers.control.write(adc_snap_arm=1)

        print 'Grabbing Debug data'
        print "-------------------"
        print "db_trig is %s" % self.f.registers.db_trig.read()
        print "db_dvalid is %s" % self.f.registers.db_dvalid.read()
        print "db_sync is %s" % self.f.registers.db_sync.read()
        print "db_unpack_sync is %s" % self.f.registers.db_unpack_sync.read()
        print "db_unpack_dvalid is %s" % self.f.registers.db_unpack_dvalid.read()
        print " "
        
        # Check if any clashes exist
        print "Pol0 HMC write clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_err_p0.read()
        print "Pol0 HMC read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_rd_err_p0.read()
        print "Pol0 HMC write/read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_rd_rdy_clash_p0.read()
        print "Pol1 HMC write clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_err_p1.read()
        print "Pol1 HMC read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_rd_err_p1.read()
        print "Pol1 HMC write/read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_rd_rdy_clash_p1.read()
        print ''
        print "--------------------------------------------------------------------------------------------------------"

                                
        print 'Grabbing Snapshot Data'
        print "----------------------"
        
        print "Grabbing snap_adc0"
        data_in = self.f.snapshots.snap_adc0_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']
        
        '''
        print "Grabbing HMC debug data"
        hmc_debug0 = \
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug0_p0_ss.read(arm=False, man_trig=trig_mode,
                                                                                 man_valid=valid_mode)['data']
        hmc_debug1 = \
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug1_p0_ss.read(arm=False, man_trig=trig_mode,
                                                                                 man_valid=valid_mode)['data']

        print "Grabbing HMC din"
        hmc_din0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_p0_ss.read(arm=False, man_trig=trig_mode,
                                                                                          man_valid=valid_mode)['data']
        hmc_din1 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_p0_ss.read(arm=False, man_trig=trig_mode,
                                                                                          man_valid=valid_mode)['data']
                                                                                          
        '''

                                                                                          
        print "Grabbing CD out"
        data_out_pol0 = self.f.snapshots.cd_out_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        data_out_pol1 = self.f.snapshots.cd_out1_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        # Grab captured sync in and out of the HMC
        hmc_sync_in = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in.read()
        hmc_sync_out = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out.read()

        hmc_sync_in_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_in_cnt.read()
        hmc_sync_out_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_sync_out_cnt.read()

        # CD Input data
        din_00 = data_in['d0']
        din_01 = data_in['d1']
        din_02 = data_in['d2']
        din_03 = data_in['d3']
        din_04 = data_in['d4']
        din_05 = data_in['d5']
        din_06 = data_in['d6']
        din_07 = data_in['d7']

        # CD Output data
        dout_00 = data_out_pol0['d00']
        dout_01 = data_out_pol0['d01']
        dout_02 = data_out_pol0['d02']
        dout_03 = data_out_pol0['d03']
        dout_04 = data_out_pol0['d04']
        dout_05 = data_out_pol0['d05']
        dout_06 = data_out_pol0['d06']
        dout_07 = data_out_pol0['d07']

        dout_10 = data_out_pol1['d00']
        dout_11 = data_out_pol1['d01']
        dout_12 = data_out_pol1['d02']
        dout_13 = data_out_pol1['d03']
        dout_14 = data_out_pol1['d04']
        dout_15 = data_out_pol1['d05']
        dout_16 = data_out_pol1['d06']
        dout_17 = data_out_pol1['d07']

        cd_out_sync = data_out_pol0['sync']
        cd_out_dvalid = data_out_pol0['dvalid']

        '''
        hmc_debug0_win = hmc_debug0['win']
        hmc_debug0_wr_rdy = hmc_debug0['wr_rdy']
        hmc_debug0_waddr = hmc_debug0['waddr']
        hmc_debug0_rin = hmc_debug0['rin']
        hmc_debug0_rdaddr = hmc_debug0['rdaddr']
        hmc_debug0_tag_in = hmc_debug0['tag_in']
        hmc_debug0_rd_rdy = hmc_debug0['rd_rdy']
        hmc_debug0_tag_out = hmc_debug0['tag_out']

        hmc_debug1_dvalid_p0 = hmc_debug1['dvalid']
        hmc_debug1_wr_rdy_p0 = hmc_debug1['wr_rdy']
        hmc_debug1_rd_rdy_p0 = hmc_debug1['rd_rdy']
        hmc_debug1_tag_out_p0 = hmc_debug1['tag_out']
        '''


        # Toggle the capture control to allow a small window of capture time
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=0)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl_rst.write(reg=0)

        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=0)

        # Read in the counters controlled by the capture
        wr_req_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_wr_req_count.read()
        rd_req_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_rd_req_count.read()
        cd_rd_dvalid_count = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_rd_dvalid_count.read()

        print ''
        print 'Reord Readout Add Check'
        print "-----------------------"
        print "Grabbing Reord Debug"
        reord_addr = self.f.snapshots.reord_addr_db_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print 'P0 Addr'
        print '-------'
        print reord_addr['p0_addr'][0:read_length]

        print 'P0 bram_en'
        print '----------'
        print reord_addr['p0_bram_en'][0:read_length]

        print 'P1 Addr'
        print '-------'
        print reord_addr['p1_addr'][0:read_length]

        print 'P1 bram_en'
        print '----------'
        print reord_addr['p1_bram_en'][0:read_length]


        print ''
        print 'Latency Check'
        print "-------------"
        #print 'cd_in_count_thresh is %s' % self.f.registers.cd_in_cnt_thresh.read()
        #print ''
        #print 'cd_out_count_thresh is %s' % self.f.registers.cd_out_cnt_thresh.read()
        #print ''

        print 'Input Samples'
        print '-------------'

        #print 'sync in is %s' % cd_in_sync[0:read_length]
        #print 'dvalid in is %s' % cd_in_dvalid[0:read_length]
        #print ' '
        
        print 'D00'
        print '---'
        print din_00[0:read_length]

        print 'D01'
        print '---'
        print din_01[0:read_length]

        print 'D02'
        print '---'
        print din_02[0:read_length]

        print 'D03'
        print '---'
        print din_03[0:read_length]

        print 'D04'
        print '---'
        print din_04[0:read_length]

        print 'D05'
        print '---'
        print din_05[0:read_length]

        print 'D06'
        print '---'
        print din_06[0:read_length]

        print 'D07'
        print '---'
        print din_07[0:read_length]
        print ''
    
        print 'Output Samples: Pol0'
        print '--------------------'

        #print 'sync out is %s' % cd_out_sync[0:read_length]
        #print 'dvalid out is %s' % cd_out_dvalid[0:read_length]
        #print ' '

        
        print 'D00'
        print '---'
        print dout_00[0:read_length]

        print 'D01'
        print '---'
        print dout_01[0:read_length]

        print 'D02'
        print '---'
        print dout_02[0:read_length]

        print 'D03'
        print '---'
        print dout_03[0:read_length]

        print 'D04'
        print '---'
        print dout_04[0:read_length]

        print 'D05'
        print '---'
        print dout_05[0:read_length]

        print 'D06'
        print '---'
        print dout_06[0:read_length]

        print 'D07'
        print '---'
        print dout_07[0:read_length]
        print ''

        print 'Output Samples: Pol1'
        print '--------------------'
        print 'D00'
        print '---'
        print dout_10[0:read_length]

        print 'D01'
        print '---'
        print dout_11[0:read_length]

        print 'D02'
        print '---'
        print dout_12[0:read_length]

        print 'D03'
        print '---'
        print dout_13[0:read_length]

        print 'D04'
        print '---'
        print dout_14[0:read_length]

        print 'D05'
        print '---'
        print dout_15[0:read_length]

        print 'D06'
        print '---'
        print dout_16[0:read_length]

        print 'D07'
        print '---'
        print dout_17[0:read_length]
        print ''

        '''
        print 'HMC Debug'
        print '---------'
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
        print 'wr_req_count is %s' % wr_req_count
        print ''
        print 'rd_req_count is %s' % rd_req_count
        print ''
        print 'cd_rd_dvalid_count is %s' % cd_rd_dvalid_count
        print ''

        '''
        # Plot lin_plot results
        #plt.figure(1)
        #plt.ion()
        #plt.clf()

        #plt.plot(din_00[0:read_length])
        #plt.show()

    def change_delay(self, arm_mode, trig_mode, valid_mode, read_length, delay):

        self.skarab()

        print "System Information"
        print "------------------"

        print "Amplitude and Offset P0 is %s" % self.f.registers.impulse0.read()
        print "Amplitude and Offset P1 is %s" % self.f.registers.impulse1.read()
        print " "

        print "Last set HMC Delay Pol0 is %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_delay.read()
        print "Last set HMC Delay Pol1 is %s" % self.f.registers.cd_compensation1_cd_hmc_hmc_delay_hmc_delay.read()
        print ''

        print "Last set Barrel Shift Delay Pol0 is %s" % self.f.registers.wb_prog_delay_bs_delay0.read()
        print "Last set Barrel Shift Delay Pol1 is %s" % self.f.registers.wb_prog_delay1_bs_delay1.read()
        print ''

        print "-------------"
        print "Setting Delay"
        print "-------------"
        print ''

        # Set delay for test
        self.f.registers.delay0.write(initial=delay)
        self.f.registers.delay1.write(initial=delay)

        # Arm and load
        '''
        self.f.registers.tl_cd0_control0.write(arm=1)
        self.f.registers.tl_cd0_control0.write(load_immediate=1)
        self.f.registers.tl_cd0_control0.write(arm=0)

        self.f.registers.tl_cd1_control0.write(arm=1)
        self.f.registers.tl_cd1_control0.write(load_immediate=1)
        self.f.registers.tl_cd1_control0.write(arm=0)

        self.f.registers.tl_cd_bs0_control0.write(arm=1)
        self.f.registers.tl_cd_bs0_control0.write(load_immediate=1)
        self.f.registers.tl_cd_bs0_control0.write(arm=0)

        self.f.registers.tl_cd_bs1_control0.write(arm=1)
        self.f.registers.tl_cd_bs1_control0.write(load_immediate=1)
        self.f.registers.tl_cd_bs1_control0.write(arm=0)
        '''

        self.f.registers.tl_cd0_control.write(arm=1)
        self.f.registers.tl_cd0_control.write(load_immediate=1)
        self.f.registers.tl_cd0_control.write(arm=0)

        self.f.registers.tl_cd1_control.write(arm=1)
        self.f.registers.tl_cd1_control.write(load_immediate=1)
        self.f.registers.tl_cd1_control.write(arm=0)



        print "Delay 0 is %s" % self.f.registers.delay0.read()
        print "Delay 1 is %s" % self.f.registers.delay1.read()
        print ''

        print "HMC delay Pol0 set as: %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_delay.read()
        print "HMC delay Pol1 set as: %s" % self.f.registers.cd_compensation1_cd_hmc_hmc_delay_hmc_delay.read()
        print ''

        print "Barrel Shift Delay Pol0 is %s" % self.f.registers.wb_prog_delay_bs_delay0.read()
        print "Barrel Shift Delay Pol1 is %s" % self.f.registers.wb_prog_delay1_bs_delay1.read()
        print ''
        print "--------------------------------------------------------------------------------------------------------"

        # Reset the Counters
        self.f.registers.count_rst.write(rst=1)
        self.f.registers.count_rst.write(rst=0)

        # Check if any clashes exist
        print "Pol0 HMC write clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_err_p0.read()
        print "Pol0 HMC read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_rd_err_p0.read()
        print "Pol0 HMC write/read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_rd_rdy_clash_p0.read()
        print "Pol1 HMC write clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_err_p1.read()
        print "Pol1 HMC read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_rd_err_p1.read()
        print "Pol1 HMC write/read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_rd_rdy_clash_p1.read()
        print ''
        print "--------------------------------------------------------------------------------------------------------"


        # Read the delay
        print "d80_data_delay is %s" % self.f.registers.d80_data_delay.read()
        print "cd_data_delay Pol0 is %s" % self.f.registers.cd_data_pol0_delay.read()
        print "cd_data_delay Pol1 (p0 sync) is %s" % self.f.registers.cd_data_pol1_delay.read()
        print "cd_data_delay Pol1 is %s" % self.f.registers.cd_data_pol1_delay1.read()
        print ''
        print "Check if the input impulse counter is spinning %s" % self.f.registers.d80_pol0_count.read()
        print "Check if the Spectrum edge counter is spinning %s" % self.f.registers.spec_edge_count.read()
        print "Check if the output impulse (Pol0) counter is spinning %s" % self.f.registers.cd_out_pol0_count.read()
        print "Check if the output impulse (Pol1) counter is spinning %s" % self.f.registers.cd_out_pol1_count.read()
        print "Check if the output impulse (Pol1) counter1 is spinning %s" % self.f.registers.cd_out_pol1_count1.read()
        print ''

        #self.f.snapshots.snap_adc0_ss.arm()
        #self.f.snapshots.snap_adc1_ss.arm()

        #self.f.snapshots.cd_out_ss.arm()
        #self.f.snapshots.cd_out1_ss.arm()

        #print "Grabbing CD out"
        #data_out_pol0 = self.f.snapshots.cd_out_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        #data_out_pol1 = self.f.snapshots.cd_out1_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        # CD Output data
        #dout_00 = data_out_pol0['d00']
        #dout_01 = data_out_pol0['d01']
        #dout_02 = data_out_pol0['d02']
        #dout_03 = data_out_pol0['d03']
        #dout_04 = data_out_pol0['d04']
        #dout_05 = data_out_pol0['d05']
        #dout_06 = data_out_pol0['d06']
        #dout_07 = data_out_pol0['d07']

        #dout_10 = data_out_pol1['d00']
        #dout_11 = data_out_pol1['d01']
        #dout_12 = data_out_pol1['d02']
        #dout_13 = data_out_pol1['d03']
        #dout_14 = data_out_pol1['d04']
        #dout_15 = data_out_pol1['d05']
        #dout_16 = data_out_pol1['d06']
        #dout_17 = data_out_pol1['d07']

        #print 'Output Samples: Pol0'
        #print '--------------------'

        # print 'sync out is %s' % cd_out_sync[0:read_length]
        # print 'dvalid out is %s' % cd_out_dvalid[0:read_length]
        # print ' '

        '''
        print 'D00'
        print '---'
        print dout_00[0:read_length]

        print 'D01'
        print '---'
        print dout_01[0:read_length]

        print 'D02'
        print '---'
        print dout_02[0:read_length]

        print 'D03'
        print '---'
        print dout_03[0:read_length]

        print 'D04'
        print '---'
        print dout_04[0:read_length]

        print 'D05'
        print '---'
        print dout_05[0:read_length]

        print 'D06'
        print '---'
        print dout_06[0:read_length]

        print 'D07'
        print '---'
        print dout_07[0:read_length]
        print ''

        print 'Output Samples: Pol1'
        print '--------------------'
        print 'D00'
        print '---'
        print dout_10[0:read_length]

        print 'D01'
        print '---'
        print dout_11[0:read_length]

        print 'D02'
        print '---'
        print dout_12[0:read_length]

        print 'D03'
        print '---'
        print dout_13[0:read_length]

        print 'D04'
        print '---'
        print dout_14[0:read_length]

        print 'D05'
        print '---'
        print dout_15[0:read_length]

        print 'D06'
        print '---'
        print dout_16[0:read_length]

        print 'D07'
        print '---'
        print dout_17[0:read_length]
        print ''
        '''



    # HMC Debug
    # ---------
    def hmc_debug(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length, read_length):

        # Check if HMC post and init are ok
        post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        init_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        post = post_reg['data']
        init = init_reg['data']

        print "HMC Status"
        print "----------"
        print "Post is %s" % post
        print "Init is %s" % init
        print " "


        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug1_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_i_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_i_ss.arm()

        print "Grab SS"
        hmc_debug = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_debug1_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        hmc_debug_din0 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din0_i_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        hmc_debug_din1 = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_hmc_din1_i_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']


        # HMC debug
        print ''
        print 'HMC debug (extra)'
        print "-------------"
        print 'hmc_debug0_win is %s' % hmc_debug['win'][0:read_length]
        print 'hmc_debug0_wr_rdy is %s' % hmc_debug['wr_rdy'][0:read_length]
        print 'hmc_debug0_waddr_p0 is %s' % hmc_debug['waddr_p0'][0:read_length]
        print 'hmc_debug0_waddr_p1 is %s' % hmc_debug['waddr_p1'][0:read_length]
        print 'hmc_debug0_rin is %s' % hmc_debug['rin'][0:read_length]
        print 'hmc_debug0_rdaddr is %s' % hmc_debug['rdaddr'][0:read_length]
        print 'hmc_debug0_tag_in is %s' % hmc_debug['tag_in'][0:read_length]
        print 'hmc_debug0_rd_rdy is %s' % hmc_debug['rd_rdy'][0:read_length]
        print 'hmc_debug0_tag_out is %s' % hmc_debug['tag_out'][0:read_length]
        print 'hmc_clear_done is %s' % hmc_debug['clear_done'][0:read_length]
        print 'reord_addr is %s' % hmc_debug['reord_addr'][0:read_length]
        print 'reord_wea is %s' % hmc_debug['reord_wea'][0:read_length]

        print ''

        hmc_din0_i_00 = hmc_debug_din0['d00']
        hmc_din0_i_01 = hmc_debug_din0['d01']
        hmc_din0_i_02 = hmc_debug_din0['d02']
        hmc_din0_i_03 = hmc_debug_din0['d03']
        hmc_din0_i_04 = hmc_debug_din0['d04']
        hmc_din0_i_05 = hmc_debug_din0['d05']
        hmc_din0_i_06 = hmc_debug_din0['d06']
        hmc_din0_i_07 = hmc_debug_din0['d07']

        hmc_din1_i_00 = hmc_debug_din1['d00']
        hmc_din1_i_01 = hmc_debug_din1['d01']
        hmc_din1_i_02 = hmc_debug_din1['d02']
        hmc_din1_i_03 = hmc_debug_din1['d03']
        hmc_din1_i_04 = hmc_debug_din1['d04']
        hmc_din1_i_05 = hmc_debug_din1['d05']
        hmc_din1_i_06 = hmc_debug_din1['d06']
        hmc_din1_i_07 = hmc_debug_din1['d07']

        print 'D00'
        print '---'
        print hmc_din0_i_00[0:read_length]

        print 'D01'
        print '---'
        print hmc_din0_i_01[0:read_length]

        print 'D02'
        print '---'
        print hmc_din0_i_02[0:read_length]

        print 'D03'
        print '---'
        print hmc_din0_i_03[0:read_length]

        print 'D04'
        print '---'
        print hmc_din0_i_04[0:read_length]

        print 'D05'
        print '---'
        print hmc_din0_i_05[0:read_length]

        print 'D06'
        print '---'
        print hmc_din0_i_06[0:read_length]

        print 'D07'
        print '---'
        print hmc_din0_i_07[0:read_length]
        print ''

        print 'D08'
        print '---'
        print hmc_din1_i_00[0:read_length]

        print 'D09'
        print '---'
        print hmc_din1_i_01[0:read_length]

        print 'D10'
        print '---'
        print hmc_din1_i_02[0:read_length]

        print 'D11'
        print '---'
        print hmc_din1_i_03[0:read_length]

        print 'D12'
        print '---'
        print hmc_din1_i_04[0:read_length]

        print 'D13'
        print '---'
        print hmc_din1_i_05[0:read_length]

        print 'D14'
        print '---'
        print hmc_din1_i_06[0:read_length]

        print 'D15'
        print '---'
        print hmc_din1_i_07[0:read_length]
        print ''

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





    def reorder(self, arm_mode, trig_mode, valid_mode, plot_count_max, disp_length, delay, read_length, sync_sel):
        self.skarab_info()


        # Disable the dvalid
        self.f.registers.dvalid.write(reg=0)

        self.f.registers.control.write(sys_rst=1)
        self.f.registers.control.write(sys_rst=0)

        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_clear_hmc.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_clear_hmc.write(reg=0)

        self.f.registers.sync_select.write(reg=sync_sel)
        self.f.registers.man_sync.write(reg=0)

        # Reset the plot counter
        plot_count = 0

        # Set delay for test
        self.f.registers.delay0.write(initial=delay)

        # Reset sync monitor
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=0)

        #Arm and load
        self.f.registers.tl_cd0_control.write(arm=1)
        self.f.registers.tl_cd0_control.write(load_immediate=0)
        self.f.registers.tl_cd0_control.write(arm=0)


        # Set the trig_arm
        self.f.registers.control.write(adc_snap_arm=0)

        # Enable the TVG
        self.f.registers.control.write(tvg_adc=0)

        # Reset sync monitor
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=0)


        print "System Information"
        print "------------------"
        print 'Requested delay is %s' % delay
        print "Actual Delay is: %s" % self.f.registers.delay0.read()
        # print "Loaded value is: %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_delay.read()
        print " "
        #print "Amplitude and Offset P0 is %s" % self.f.registers.impulse0.read()
        #print "Amplitude and Offset P1 is %s" % self.f.registers.impulse1.read()
        print " "

        print 'Checking Initial Sync and Dvalid states'
        print "---------------------------------------"

        # Arm the Snapshot Blocks
        # -----------------------
        print 'Arming Snapblocks'
        print "-----------------"

        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reorda_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reordb_ss.arm()

        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reord_din_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reord_dout_ss.arm()

        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_Reorder_cntrl_reord_int_ss.arm()

        print " "


        print 'Starting TVG'
        print "------------"

        # Check if any clashes exist
        print "Pol0 HMC write clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_err_p0.read()
        print "Pol0 HMC read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_rd_err_p0.read()
        print "Pol0 HMC write/read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_rd_rdy_clash_p0.read()
        print "Pol1 HMC write clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_err_p1.read()
        print "Pol1 HMC read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_rd_err_p1.read()
        print "Pol1 HMC write/read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_rd_rdy_clash_p1.read()
        print ''
        print "--------------------------------------------------------------------------------------------------------"

        # Force a relock
        self.f.registers.control.write(sys_rst=1)
        self.f.registers.control.write(sys_rst=0)

        # Set the trig_arm
        #self.f.registers.control.write(adc_snap_arm=1)
        #print " "

        # Manually set sync and dvalid
        self.f.registers.man_sync.write(reg=1)
        self.f.registers.man_sync.write(reg=0)
        self.f.registers.dvalid.write(reg=1)

        print 'Grabbing Snapshot Data'
        print "----------------------"

        print "Grabbing snap_reorda"
        reorda = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reorda_ss.read(arm=False, man_trig=trig_mode,
                                                                                        man_valid=valid_mode)['data']
        print "Grabbing snap_reordb"
        reordb = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reordb_ss.read(arm=False, man_trig=trig_mode,
                                                                                        man_valid=valid_mode)['data']

        print "Grabbing snap_reordb"
        reord_int = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_Reorder_cntrl_reord_int_ss.read(arm=False, man_trig=trig_mode,
                                                                                        man_valid=valid_mode)['data']

        print "Grabbing snap_reord_datain"
        reord_datain = \
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reord_din_ss.read(arm=False, man_trig=trig_mode,
                                                                                     man_valid=valid_mode)['data']

        print "Grabbing snap_reord_dataout"
        reord_dataout = \
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_reord_dout_ss.read(arm=False, man_trig=trig_mode,
                                                                                      man_valid=valid_mode)['data']

        reord_addra_s1 = reorda['addra']
        reord_addrb_s1 = reorda['addrb']
        reord_ena_s1 = reorda['ena']
        reord_enb_s1 = reorda['enb']
        reord_p0_ph1_rdy_s1 = reorda['p0_ph1_rdy']
        reord_p0_ph2_rdy_s1 = reorda['p0_ph2_rdy']
        reord_p1_ph1_rdy_s1 = reorda['p1_ph1_rdy']
        reord_p1_ph2_rdy_s1 = reorda['p1_ph2_rdy']

        reord_addrb_s2 = reordb['addrb']
        reord_enb_s2 = reordb['enb']
        reord_p0_ph1_rdy_s2 = reordb['p0_ph1_rdy']
        reord_p0_ph2_rdy_s2 = reordb['p0_ph2_rdy']
        reord_p1_ph1_rdy_s2 = reordb['p1_ph1_rdy']
        reord_p1_ph2_rdy_s2 = reordb['p1_ph2_rdy']

        reord_int_rd_addr_en = reord_int['rd_addr_en']
        reord_int_bram_rd_en = reord_int['bram_rd_en']
        reord_int_bram_rd_addr_full = reord_int['bram_rd_addr_full']
        reord_int_bram_rd_addr = reord_int['bram_rd_addr']
        reord_int_rst = reord_int['rst']
        reord_int_rst_reg = reord_int['reg_rst']
        reord_int_wr_en = reord_int['wr_en']
        reord_int_wr_cnt = reord_int['wr_cnt']
        reord_int_reord_p0_ph1_rdy_s2 = reord_int['p0_ph1_rdy']
        reord_int_reord_p0_ph2_rdy_s2 = reord_int['p0_ph2_rdy']
        reord_int_reord_p1_ph1_rdy_s2 = reord_int['p1_ph1_rdy']
        reord_int_reord_p1_ph2_rdy_s2 = reord_int['p1_ph2_rdy']


        reord_datain_0 = reord_datain['d0']
        reord_datain_1 = reord_datain['d1']
        reord_datain_2 = reord_datain['d2']
        reord_datain_3 = reord_datain['d3']
        reord_datain_4 = reord_datain['d4']
        reord_datain_5 = reord_datain['d5']
        reord_datain_6 = reord_datain['d6']
        reord_datain_7 = reord_datain['d7']

        reord_dataout_0 = reord_dataout['d0']
        reord_dataout_1 = reord_dataout['d1']
        reord_dataout_2 = reord_dataout['d2']
        reord_dataout_3 = reord_dataout['d3']
        reord_dataout_4 = reord_dataout['d4']
        reord_dataout_5 = reord_dataout['d5']
        reord_dataout_6 = reord_dataout['d6']
        reord_dataout_7 = reord_dataout['d7']

        # Toggle the capture control to allow a small window of capture time
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=0)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl_rst.write(reg=0)

        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=0)



        print ''
        print 'Pack the input correctly'
        print '------------------------'
        input = []

        for x in range(0, len(reord_datain_0)):
            input.extend([reord_datain_0[x], reord_datain_1[x], reord_datain_2[x], reord_datain_3[x], reord_datain_4[x], reord_datain_5[x], reord_datain_6[x], reord_datain_7[x]])

        print ''
        print 'Pack the CD output'
        print '------------------'
        output = []


        for x in range(0, len(reord_dataout_0)):
            output.extend([reord_dataout_0[x], reord_dataout_1[x], reord_dataout_2[x], reord_dataout_3[x], reord_dataout_4[x], reord_dataout_5[x],
                              reord_dataout_6[x], reord_dataout_7[x]])


        print ''
        print 'Repack Done'
        print '-----------'

        print ''
        print 'Plotting figures'
        print '----------------'

        plt.figure(1)
        plt.ion()
        plt.clf()
        plt.subplot(211)
        plt.plot(reord_addra_s1)
        plt.subplot(212)
        plt.plot(reord_ena_s1)

        plt.figure(2)
        plt.ion()
        plt.clf()
        plt.subplot(211)
        plt.plot(reord_addrb_s1)
        plt.subplot(212)
        plt.plot(reord_enb_s1)

        plt.figure(3)
        plt.ion()
        plt.clf()
        plt.subplot(411)
        plt.plot(reord_p0_ph1_rdy_s1)
        plt.subplot(412)
        plt.plot(reord_p0_ph2_rdy_s1)
        plt.subplot(413)
        plt.plot(reord_p1_ph1_rdy_s1)
        plt.subplot(414)
        plt.plot(reord_p1_ph2_rdy_s1)

        plt.figure(4)
        plt.ion()
        plt.clf()
        plt.subplot(211)
        plt.plot(reord_addrb_s2)
        plt.subplot(212)
        plt.plot(reord_enb_s2)

        plt.figure(5)
        plt.ion()
        plt.clf()
        plt.subplot(411)
        plt.plot(reord_p0_ph1_rdy_s2)
        plt.subplot(412)
        plt.plot(reord_p0_ph2_rdy_s2)
        plt.subplot(413)
        plt.plot(reord_p1_ph1_rdy_s2)
        plt.subplot(414)
        plt.plot(reord_p1_ph2_rdy_s2)


        plt.figure(6)
        plt.ion()
        plt.clf()
        plt.plot(input[0:read_length])

        plt.figure(7)
        plt.ion()
        plt.clf()
        plt.plot(output[0:read_length])



        plt.show()

        # Spare





    # PFB
    # ---
    def pfb(self, arm_mode, trig_mode, valid_mode, delay, read_length):

        self.skarab()

        # Set the trig_arm
        self.f.registers.control.write(adc_snap_arm=0)

        # Set Impulse values
        self.f.registers.impulse0.write(offset=0)
        self.f.registers.impulse0.write(amplitude=0.5)

        self.f.registers.impulse1.write(offset=0)
        self.f.registers.impulse1.write(amplitude=0.5)

        # Set delay for test
        self.f.registers.delay0.write(initial=delay)
        self.f.registers.delay1.write(initial=delay)

        # Arm and load
        self.f.registers.tl_cd0_control.write(arm=1)
        self.f.registers.tl_cd0_control.write(load_immediate=1)
        self.f.registers.tl_cd0_control.write(arm=0)

        self.f.registers.tl_cd1_control.write(arm=1)
        self.f.registers.tl_cd1_control.write(load_immediate=1)
        self.f.registers.tl_cd1_control.write(arm=0)

        # Enable the TVG
        self.f.registers.control.write(tvg_adc=0)

        self.f.registers.adc_en0.write(en=0)
        self.f.registers.adc_en1.write(en=0)

        # Reset sync monitor
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_sync_mon_rst.write(reg=0)

        # Set the Snap trig time (if used)
        self.f.registers.trig_time_msw.write(msw=0)
        self.f.registers.trig_time_lsw.write(lsw=0)

        # Set the Snap trig source
        self.f.registers.control.write(adc_snap_trig_select=0)

        # Check if HMC post and init are ok
        #post_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_post.read()
        #init_reg = self.f.registers.cd_compensation0_cd_hmc_hmc_delay_cd_hmc_init.read()
        #post = post_reg['data']
        #init = init_reg['data']

        print "System Information"
        print "------------------"
        print 'Requested delay is %s' % delay
        print "Actual Delay is: %s" % self.f.registers.delay0.read()
        #print "Loaded value is: %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_delay.read()
        print " "
        print "Amplitude and Offset P0 is %s" % self.f.registers.impulse0.read()
        print "Amplitude and Offset P1 is %s" % self.f.registers.impulse1.read()
        print " "

        print "HMC Status"
        print "----------"
        #print "Post is %s" % post
        #print "Init is %s" % init
        print " "

        print 'Checking Initial Sync and Dvalid states'
        print "---------------------------------------"

        # Arm the Snapshot Blocks
        # -----------------------
        print 'Arming Snapblocks'
        print "-----------------"
        self.f.snapshots.snap_adc0_ss.arm()
        self.f.snapshots.snap_adc1_ss.arm()

        self.f.snapshots.snap_pre_pfb0_ss.arm()
        #self.f.snapshots.snap_pre_pfb1_ss.arm()
        #self.f.snapshots.snap_pre_pfb2_ss.arm()


        self.f.snapshots.snap_pfb0_ss.arm()
        #self.f.snapshots.snap_pfb1_ss.arm()

        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_snap_reorda_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_snap_reordb_ss.arm()

        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_snap_reord_datain_ss.arm()
        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_snap_reord_dataout_ss.arm()

        self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_Reorder_cntrl_snap_reord_int_ss.arm()

        print " "


        print 'Starting TVG'
        print "------------"

        # Force a relock
        self.f.registers.control.write(sys_rst=1)
        self.f.registers.control.write(sys_rst=0)

        # Set the trig_arm
        self.f.registers.control.write(adc_snap_arm=1)
        print " "


        # Check if any clashes exist
        print "Pol0 HMC write clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_err_p0.read()
        print "Pol0 HMC read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_rd_err_p0.read()
        print "Pol0 HMC write/read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_rd_rdy_clash_p0.read()
        print "Pol1 HMC write clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_err_p1.read()
        print "Pol1 HMC read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_rd_err_p1.read()
        print "Pol1 HMC write/read clash %s" % self.f.registers.cd_compensation0_cd_hmc_hmc_delay_hmc_wr_rd_rdy_clash_p1.read()
        print ''
        print "--------------------------------------------------------------------------------------------------------"

        print ''
        print "Set trig time"
        local_time_msw = self.f.registers.local_time_msw.read()
        print "Local Time (msw) is %s" % local_time_msw['data']['timestamp_msw']

        #Set new trig time
        self.f.registers.trig_time_msw.write(msw = local_time_msw['data']['timestamp_msw'] + 2)

        print "Trig Time (msw) is %s" % self.f.registers.trig_time_msw.read()
        print ''

        print 'Grabbing Snapshot Data'
        print "----------------------"

        print "Grabbing snap_adc0"
        data_in0 = self.f.snapshots.snap_adc0_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing snap_adc1"
        data_in1 = self.f.snapshots.snap_adc1_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing snap_pre_pfb0"
        pre_pfb0 = self.f.snapshots.snap_pre_pfb0_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        #print "Grabbing snap_pre_pfb1"
        #pre_pfb1 = self.f.snapshots.snap_pre_pfb1_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        #print "Grabbing snap_pre_pfb1"
        #pre_pfb2 = self.f.snapshots.snap_pre_pfb2_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']


        print "Grabbing snap_pfb0"
        pfb0 = self.f.snapshots.snap_pfb0_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        #print "Grabbing snap_pfb0"
        #pfb1 = self.f.snapshots.snap_pfb1_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing snap_reorda"
        reorda = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_snap_reorda_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing snap_reordb"
        reordb = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_snap_reordb_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']


        print "Grabbing snap_reord_datain"
        reord_datain = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_snap_reord_datain_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing snap_reord_dataout"
        reord_dataout = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_snap_reord_dataout_ss.read(arm=False, man_trig=trig_mode, man_valid=valid_mode)['data']

        print "Grabbing snap_reordb"
        reord_int = self.f.snapshots.cd_compensation0_cd_hmc_hmc_delay_Reorder_cntrl_snap_reord_int_ss.read(arm=False, man_trig=False,
                                                                                        man_valid=False)['data']


        # CD Input data pol0
        sync_input =  data_in0['sync']
        dv_input = data_in0['dv']

        din_00 = data_in0['d0']
        din_01 = data_in0['d1']
        din_02 = data_in0['d2']
        din_03 = data_in0['d3']
        din_04 = data_in0['d4']
        din_05 = data_in0['d5']
        din_06 = data_in0['d6']
        din_07 = data_in0['d7']

        # CD Input data pol1
        din_10 = data_in1['d0']
        din_11 = data_in1['d1']
        din_12 = data_in1['d2']
        din_13 = data_in1['d3']
        din_14 = data_in1['d4']
        din_15 = data_in1['d5']
        din_16 = data_in1['d6']
        din_17 = data_in1['d7']


        # CD Output data
        sync_pre_pfb = pre_pfb0['sync']
        dv_pre_pfb = pre_pfb0['dv']

        pre_pfb0_0 = pre_pfb0['d0']
        pre_pfb0_1 = pre_pfb0['d1']
        pre_pfb0_2 = pre_pfb0['d2']
        pre_pfb0_3 = pre_pfb0['d3']
        pre_pfb0_4 = pre_pfb0['d4']
        pre_pfb0_5 = pre_pfb0['d5']
        pre_pfb0_6 = pre_pfb0['d6']
        pre_pfb0_7 = pre_pfb0['d7']

        '''
        pre_pfb1_0 = pre_pfb1['d0']
        pre_pfb1_1 = pre_pfb1['d1']
        pre_pfb1_2 = pre_pfb1['d2']
        pre_pfb1_3 = pre_pfb1['d3']
        pre_pfb1_4 = pre_pfb1['d4']
        pre_pfb1_5 = pre_pfb1['d5']
        pre_pfb1_6 = pre_pfb1['d6']
        pre_pfb1_7 = pre_pfb1['d7']

        pre_pfb2_0 = pre_pfb2['d0']
        pre_pfb2_1 = pre_pfb2['d1']
        pre_pfb2_2 = pre_pfb2['d2']
        pre_pfb2_3 = pre_pfb2['d3']
        pre_pfb2_4 = pre_pfb2['d4']
        pre_pfb2_5 = pre_pfb2['d5']
        pre_pfb2_6 = pre_pfb2['d6']
        pre_pfb2_7 = pre_pfb2['d7']
        '''

        sync_pfb = pfb0['sync']
        dv_pfb = pfb0['dv']

        pfb0_r0 = pfb0['r0']
        pfb0_r1 = pfb0['r1']
        pfb0_r2 = pfb0['r2']
        pfb0_r3 = pfb0['r3']
        pfb0_i0 = pfb0['i0']
        pfb0_i1 = pfb0['i1']
        pfb0_i2 = pfb0['i2']
        pfb0_i3 = pfb0['i3']

        '''
        pfb1_r0 = pfb1['r0']
        pfb1_r1 = pfb1['r1']
        pfb1_r2 = pfb1['r2']
        pfb1_r3 = pfb1['r3']
        pfb1_i0 = pfb1['i0']
        pfb1_i1 = pfb1['i1']
        pfb1_i2 = pfb1['i2']
        pfb1_i3 = pfb1['i3']
        '''

        reord_addra_s1 = reorda['addra']
        reord_addrb_s1 = reorda['addrb']
        reord_ena_s1 = reorda['ena']
        reord_enb_s1 = reorda['enb']
        reord_p0_ph1_rdy_s1 = reorda['p0_ph1_rdy']
        reord_p0_ph2_rdy_s1 = reorda['p0_ph2_rdy']
        reord_p1_ph1_rdy_s1 = reorda['p1_ph1_rdy']
        reord_p1_ph2_rdy_s1 = reorda['p1_ph2_rdy']

        reord_addrb_s2 = reordb['addrb']
        reord_enb_s2 = reordb['enb']
        reord_p0_ph1_rdy_s2 = reordb['p0_ph1_rdy']
        reord_p0_ph2_rdy_s2 = reordb['p0_ph2_rdy']
        reord_p1_ph1_rdy_s2 = reordb['p1_ph1_rdy']
        reord_p1_ph2_rdy_s2 = reordb['p1_ph2_rdy']

        reord_int_rd_addr_en = reord_int['rd_addr_en']
        reord_int_bram_rd_en = reord_int['bram_rd_en']
        reord_int_bram_rd_addr_full = reord_int['bram_rd_addr_full']
        reord_int_bram_rd_addr = reord_int['bram_rd_addr']
        reord_int_rst = reord_int['rst']
        reord_int_rst_reg = reord_int['reg_rst']
        reord_int_wr_en = reord_int['wr_en']
        reord_int_wr_cnt = reord_int['wr_cnt']
        reord_int_reord_p0_ph1_rdy_s2 = reord_int['p0_ph1_rdy']
        reord_int_reord_p0_ph2_rdy_s2 = reord_int['p0_ph2_rdy']
        reord_int_reord_p1_ph1_rdy_s2 = reord_int['p1_ph1_rdy']
        reord_int_reord_p1_ph2_rdy_s2 = reord_int['p1_ph2_rdy']

        reord_int_reord_half_reg1 = reord_int['half_reg1']
        reord_int_reord_half_reg2 = reord_int['half_reg2']
        reord_int_reord_full_reg1 = reord_int['full_reg1']
        reord_int_reord_full_reg2 = reord_int['full_reg2']
        reord_int_reord_half_reg_rst = reord_int['half_reg_rst']
        reord_int_reord_full_reg_rst = reord_int['full_reg_rst']
        reord_int_reord_cnt_en1 = reord_int['cnt_en1']
        reord_int_reord_cnt_en2 = reord_int['cnt_en2']
        reord_int_reord_out_lower = reord_int['out_lower']

        reord_datain_0 = reord_datain['d0']
        reord_datain_1 = reord_datain['d1']
        reord_datain_2 = reord_datain['d2']
        reord_datain_3 = reord_datain['d3']
        reord_datain_4 = reord_datain['d4']
        reord_datain_5 = reord_datain['d5']
        reord_datain_6 = reord_datain['d6']
        reord_datain_7 = reord_datain['d7']

        reord_dataout_0 = reord_dataout['d0']
        reord_dataout_1 = reord_dataout['d1']
        reord_dataout_2 = reord_dataout['d2']
        reord_dataout_3 = reord_dataout['d3']
        reord_dataout_4 = reord_dataout['d4']
        reord_dataout_5 = reord_dataout['d5']
        reord_dataout_6 = reord_dataout['d6']
        reord_dataout_7 = reord_dataout['d7']


        # Toggle the capture control to allow a small window of capture time
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=0)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl_rst.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl_rst.write(reg=0)

        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=1)
        self.f.registers.cd_compensation0_cd_hmc_hmc_delay_dvalid_capture_cntrl.write(reg=0)

        print ''
        print 'Pack the input correctly'
        print '------------------------'
        input = []

        for x in range(0, len(din_00)):
            input.extend([din_00[x], din_01[x], din_02[x], din_03[x], din_04[x], din_05[x], din_06[x], din_07[x]])

        print ''
        print 'Pack the CD output'
        print '------------------'
        cd_output = []


        for x in range(0, len(pre_pfb0_0)):
            cd_output.extend([pre_pfb0_0[x], pre_pfb0_1[x], pre_pfb0_2[x], pre_pfb0_3[x], pre_pfb0_4[x], pre_pfb0_5[x], pre_pfb0_6[x], pre_pfb0_7[x]])


        print ''
        print 'Pack the PFB output correctly'
        print '-----------------------------'

        pfb_pol0_real = []
        pfb_pol0_imag = []
        pfb_pol1_real = []
        pfb_pol1_imag = []

        for x in range(0, len(pfb0_r0)):
            pfb_pol0_real.extend([pfb0_r0[x], pfb0_r1[x], pfb0_r2[x], pfb0_r3[x]])
            pfb_pol0_imag.extend([pfb0_i0[x], pfb0_i1[x], pfb0_i2[x], pfb0_i3[x]])

            #pfb_pol1_real.extend([pfb1_r0[x], pfb1_r1[x], pfb1_r2[x], pfb1_r3[x]])
            #pfb_pol1_imag.extend([pfb1_i0[x], pfb1_i1[x], pfb1_i2[x], pfb1_i3[x]])

        print ''
        print 'Repack Done'
        print '-----------'



        print ''
        print 'Plotting figures'
        print '----------------'


        plt.figure(1)
        plt.ion()
        plt.clf()
        plt.plot(input[0:read_length*2])

        plt.figure(2)
        plt.ion()
        plt.clf()
        plt.plot(cd_output[0:read_length*2])

        plt.figure(3)
        plt.ion()
        plt.clf()
        plt.subplot(411)
        plt.plot(reord_int_wr_en)
        plt.subplot(412)
        plt.plot(reord_int_wr_cnt)
        plt.subplot(413)
        plt.plot(reord_int_reord_half_reg1)
        plt.subplot(414)
        plt.plot(reord_int_reord_full_reg1)

        plt.figure(4)
        plt.ion()
        plt.clf()
        plt.subplot(411)
        plt.plot(reord_int_reord_half_reg2)
        plt.subplot(412)
        plt.plot(reord_int_reord_full_reg2)
        plt.subplot(413)
        plt.plot(reord_int_reord_cnt_en1)
        plt.subplot(414)
        plt.plot(reord_int_reord_cnt_en2)

        plt.figure(5)
        plt.ion()
        plt.clf()
        plt.subplot(411)
        plt.plot(reord_int_reord_p0_ph1_rdy_s2)
        plt.subplot(412)
        plt.plot(reord_int_reord_p1_ph1_rdy_s2)
        plt.subplot(413)
        plt.plot(reord_int_reord_p0_ph2_rdy_s2)
        plt.subplot(414)
        plt.plot(reord_int_reord_p1_ph2_rdy_s2)

        embed()

        '''
        reord_int_rd_addr_en
        reord_int_bram_rd_en
        reord_int_bram_rd_addr_full
        reord_int_bram_rd_addr
        reord_int_rst
        reord_int_rst_reg
        reord_int_wr_en
        reord_int_wr_cnt
        reord_int_reord_p0_ph1_rdy_s2
        reord_int_reord_p0_ph2_rdy_s2
        reord_int_reord_p1_ph1_rdy_s2
        reord_int_reord_p1_ph2_rdy_s2

        reord_int_reord_half_reg1
        reord_int_reord_half_reg2
        reord_int_reord_full_reg1
        reord_int_reord_full_reg2
        reord_int_reord_half_reg_rst
        reord_int_reord_full_reg_rst
        reord_int_reord_cnt_en1
        reord_int_reord_cnt_en2
        reord_int_reord_out_lower
        '''


        '''
        # Time Domain of input
        plt.figure(1)
        plt.ion()
        plt.clf()
        #plt.plot(input[0:read_length])
        plt.plot(input)


        # Freq Domain of input
        fft_input = np.fft.fft(input[0:read_length])
        plt.figure(2)
        plt.ion()
        plt.clf()
        plt.plot(20 * np.log10(np.power(fft_input[0:read_length], 2)))


        # Time Domain of CD output
        plt.figure(3)
        plt.ion()
        plt.clf()
        #plt.plot(cd_output[0:read_length])
        plt.plot(cd_output)

        # Freq Domain of CD output
        fft_cd_output = np.fft.fft(cd_output[0:read_length])
        plt.figure(4)
        plt.ion()
        plt.clf()
        plt.plot(20 * np.log10(np.power(fft_cd_output[0:read_length], 2)))


        pfb_pol0_cmplx = pfb_pol0_real + ([i * 1j for i in pfb_pol0_imag])

        pfb_pol1_cmplx = pfb_pol1_real + ([i * 1j for i in pfb_pol1_imag])

        log_pfb_pol0 = 20 * np.log10(np.power(pfb_pol0_cmplx, 2))


        plt.figure(5)
        plt.ion()
        plt.clf()
        plt.subplot(311)
        plt.plot(log_pfb_pol0)

        plt.subplot(312)
        plt.plot(sync_pfb)

        plt.subplot(313)
        plt.plot(dv_pfb)


        plt.figure(6)
        plt.ion()
        plt.clf()
        plt.subplot(811)
        plt.plot(reord_addra)
        plt.subplot(812)
        plt.plot(reord_addrb)
        plt.subplot(813)
        plt.plot(reord_ena)
        plt.subplot(814)
        plt.plot(reord_enb)
        plt.subplot(815)
        plt.plot(reord_p0_ph1_rdy)
        plt.subplot(816)
        plt.plot(reord_p0_ph2_rdy)
        plt.subplot(817)
        plt.plot(reord_p1_ph1_rdy)
        plt.subplot(818)
        plt.plot(reord_p1_ph2_rdy)

        '''



        plt.show()

























        # Spare

        '''
        # Plot Outputs
        plt.figure(6)
        plt.ion()
        plt.clf()
        plt.subplot(811)
        plt.plot(din_00[0:read_length])
        plt.subplot(812)
        plt.plot(din_01[0:read_length])
        plt.subplot(813)
        plt.plot(din_02[0:read_length])
        plt.subplot(814)
        plt.plot(din_03[0:read_length])
        plt.subplot(815)
        plt.plot(din_04[0:read_length])
        plt.subplot(816)
        plt.plot(din_05[0:read_length])
        plt.subplot(817)
        plt.plot(sync_input[0:read_length])
        plt.subplot(818)
        plt.plot(dv_input[0:read_length])
        '''

        '''
        plt.figure(2)
        plt.ion()
        plt.clf()
        plt.subplot(811)
        plt.plot(din_10[0:read_length])
        plt.subplot(812)
        plt.plot(din_11[0:read_length])
        plt.subplot(813)
        plt.plot(din_12[0:read_length])
        plt.subplot(814)
        plt.plot(din_13[0:read_length])
        plt.subplot(815)
        plt.plot(din_14[0:read_length])
        plt.subplot(816)
        plt.plot(din_15[0:read_length])
        plt.subplot(817)
        plt.plot(din_16[0:read_length])
        plt.subplot(818)
        plt.plot(din_17[0:read_length])

        # Plot Outputs
        plt.figure(3)
        plt.ion()
        plt.clf()
        plt.subplot(811)
        plt.plot(pre_pfb0_0[0:read_length])
        plt.subplot(812)
        plt.plot(pre_pfb0_1[0:read_length])
        plt.subplot(813)
        plt.plot(pre_pfb0_2[0:read_length])
        plt.subplot(814)
        plt.plot(pre_pfb0_3[0:read_length])
        plt.subplot(815)
        plt.plot(pre_pfb0_4[0:read_length])
        plt.subplot(816)
        plt.plot(pre_pfb0_5[0:read_length])
        plt.subplot(817)
        plt.plot(sync_pre_pfb[0:read_length])
        plt.subplot(818)
        plt.plot(dv_pre_pfb[0:read_length])
        '''

        '''
        plt.figure(4)
        plt.ion()
        plt.clf()
        plt.subplot(811)
        plt.plot(pre_pfb1_0[0:read_length])
        plt.subplot(812)
        plt.plot(pre_pfb1_1[0:read_length])
        plt.subplot(813)
        plt.plot(pre_pfb1_2[0:read_length])
        plt.subplot(814)
        plt.plot(pre_pfb1_3[0:read_length])
        plt.subplot(815)
        plt.plot(pre_pfb1_4[0:read_length])
        plt.subplot(816)
        plt.plot(pre_pfb1_5[0:read_length])
        plt.subplot(817)
        plt.plot(sync_pre_pfb[0:read_length])
        plt.subplot(818)
        plt.plot(dv_pre_pfb[0:read_length])
        '''

        '''
        plt.figure(6)
        plt.ion()
        plt.clf()
        plt.subplot(611)
        plt.plot(log_pfb1_r0)
        plt.plot(log_pfb1_i0)

        plt.subplot(612)
        plt.plot(log_pfb1_r1)
        plt.plot(log_pfb1_i1)

        plt.subplot(613)
        plt.plot(log_pfb1_r2)
        plt.plot(log_pfb1_i2)

        plt.subplot(614)
        plt.plot(log_pfb1_r3)
        plt.plot(log_pfb1_i3)

        plt.subplot(615)
        plt.plot(sync_pfb)

        plt.subplot(616)
        plt.plot(dv_pfb)
        '''