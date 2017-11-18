# Setup FEng
#import pylab as plt

import matplotlib.pyplot as plt
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

HOST = 'skarab020304-01'

# Programming file
prog_file = "/tmp/pfb_fft_test_2017-11-17_1642.fpg"

class pfb:
    def __init__(self):
        #logging.basicConfig()
        #casperfpga.skarab_fpga.logging.getLogger().setLevel(casperfpga.skarab_fpga.logging.DEBUG)
        print "Test PFB on SKARAB"

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


    def pfb_test(self, trig_mode, valid_mode, accumulation_len):

        self.skarab_info()

        print "Disable System"
        print "--------------"
        self.f.registers.sys_en.write(en=0)
        self.f.registers.bram_clr.write(reg=0)


        print "Clear BRAM"
        print "----------"
        self.f.registers.bram_clr.write(reg=1)

        print 'BRAM clear done is %s' % self.f.registers.bram_clear_done.read()

        while self.f.registers.bram_clear_done.read()['data']['reg'] < 1:
            print 'Waiting for BRAM clear done'

        print 'Clear Done complete'
        print ''
        self.f.registers.bram_clr.write(reg=0)

        print "FFT Shift"
        print "---------"
        self.f.registers.fft_shift.write(fft_shift=8191)
        print "FFT shift is %s" % self.f.registers.fft_shift.read()
        print ""

        print "Spectrum Accumulation"
        print "---------------------"
        self.f.registers.spectrum_limit.write(limit=np.power(2,accumulation_len))
        print "Spectrum accumulation limit is %s" % self.f.registers.spectrum_limit.read()
        print ""

        self.f.registers.tvg_sel.write(tvg_sel=0)
        self.f.registers.debug_sel.write(sel=0)

        print "Set the DSim"
        print "------------"

        # Set the CWG scale
        self.f.registers.scale_cwg0.write(scale=0.75)
        self.f.registers.scale_out0.write(scale=1.0)

        # Set the frequency
        self.f.registers.freq_cwg0.write(frequency=8192000)

        # Noise Control
        self.f.registers.scale_wng0.write(scale=0.0)

        # Arm the Snapshot Blocks
        # -----------------------
        print 'Arming Snapblocks'
        print "-----------------"
        print ""
        self.f.snapshots.ss_pfb_real_sq_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_pfb_imag_sq_ss.arm(man_trig=trig_mode, man_valid=valid_mode)

        self.f.snapshots.ss_pfb_sq1_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_pfb_sq2_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_pfb_sq3_ss.arm(man_trig=trig_mode, man_valid=valid_mode)



        self.f.snapshots.ss_pfb_real_dir_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_pfb_imag_dir_ss.arm(man_trig=trig_mode, man_valid=valid_mode)

        self.f.snapshots.ss_pfb_cwg_ss.arm(man_trig=trig_mode, man_valid=valid_mode)

        self.f.snapshots.ss_pfb_tp_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_pfb_tp1_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_pfb_tp2_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_pfb_tp3_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_pfb_tp4_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_pfb_tp5_ss.arm(man_trig=trig_mode, man_valid=valid_mode)

        print 'Reset'
        print "-----"
        print ""
        # Sync Control
        self.f.registers.sys_rst.write(rst='pulse')

        print "Check Spectrum Counter"
        print "----------------------"
        print "Spectrum Counter is %s" % self.f.registers.spectrum_counter.read()
        print ""
        print "Spectrum Counter (SS) is %s" % self.f.registers.spectrum_counter_ss.read()
        print ""

        print "Check Sync"
        print "----------"
        print "PFB Sync in %s" % self.f.registers.pfbin_sync_count.read()
        print "PFB Sync out %s" % self.f.registers.pfbout_sync_count.read()
        print ""

        print "*************"
        print 'System Enable'
        print "*************"
        print ""
        self.f.registers.sys_en.write(en=1)


        print "PFB OF"
        print "------"
        print "PFB OF is %s" % self.f.registers.pfb_of.read()
        print ""

        print "Check Spectrum Counter"
        print "----------------------"
        print "Spectrum Counter is %s" % self.f.registers.spectrum_counter.read()
        print ""
        print "Spectrum Counter (SS) is %s" % self.f.registers.spectrum_counter_ss.read()
        print ""

        print "Check Sync"
        print "----------"
        print "PFB Sync in %s" % self.f.registers.pfbin_sync_count.read()
        print "PFB Sync out %s" % self.f.registers.pfbout_sync_count.read()
        print ""

        spec_limit = self.f.registers.spectrum_limit.read()

        while self.f.registers.spectrum_counter.read()['data']['reg'] < spec_limit['data']['limit']:
            print "Spectrum Counter is %s" % self.f.registers.spectrum_counter.read()

        #-----------------------------------------------------------------------------------------------------------

        print ""
        print "----------------------"
        print 'Grabbing Snapshot Data'
        print "----------------------"
        print ""

        #-----------------------------------------------------------------------------------------------------------
        print "Grabbing CWG data"
        print ""
        ss_cwg = self.f.snapshots.ss_pfb_cwg_ss.read(arm=False)['data']

        cwg0 = ss_cwg['d0']
        cwg1 = ss_cwg['d1']
        cwg2 = ss_cwg['d2']
        cwg3 = ss_cwg['d3']
        cwg4 = ss_cwg['d4']
        cwg5 = ss_cwg['d5']
        cwg6 = ss_cwg['d6']
        cwg7 = ss_cwg['d7']

        cwg = []

        for x in range(0, len(cwg0)):
            cwg.extend(
                [cwg0[x], cwg1[x], cwg2[x], cwg3[x], cwg4[x], cwg5[x], cwg6[x], cwg7[x]])

        #-----------------------------------------------------------------------------------------------------------

        print ""
        print 'Grabbing Snapshot TP'
        print "--------------------"
        print ""

        ss_tp = self.f.snapshots.ss_pfb_tp_ss.read(arm=False)['data']
        ss_tp1 = self.f.snapshots.ss_pfb_tp1_ss.read(arm=False)['data']
        ss_tp2 = self.f.snapshots.ss_pfb_tp2_ss.read(arm=False)['data']
        ss_tp3 = self.f.snapshots.ss_pfb_tp3_ss.read(arm=False)['data']
        ss_tp4 = self.f.snapshots.ss_pfb_tp4_ss.read(arm=False)['data']
        ss_tp5 = self.f.snapshots.ss_pfb_tp5_ss.read(arm=False)['data']

        # Input squared
        tp_in0 = ss_tp['pfb2_r0']
        tp_in1 = ss_tp['pfb2_r1']
        tp_in2 = ss_tp['pfb2_r2']
        tp1_in0 = ss_tp1['pfb2_r3']

        tp1_in1 = ss_tp1['pfb2_i0']
        tp1_in2 = ss_tp1['pfb2_i1']
        tp2_in0 = ss_tp2['pfb2_i2']
        tp2_in1 = ss_tp2['pfb2_i3']

        # Feedback
        tp3_in0 = ss_tp3['pfb2_r0']
        tp3_in1 = ss_tp3['pfb2_r1']
        tp3_in2 = ss_tp3['pfb2_r2']
        tp4_in0 = ss_tp4['pfb2_r3']

        tp4_in1 = ss_tp4['pfb2_i0']
        tp4_in2 = ss_tp4['pfb2_i1']
        tp5_in0 = ss_tp5['pfb2_i2']
        tp5_in1 = ss_tp5['pfb2_i3']

        # Recombine
        in_sq_real = []
        in_sq_imag = []
        fb_real = []
        fb_imag = []


        for x in range(0, len(tp_in0)):
            in_sq_real.extend([tp_in0[x], tp_in1[x], tp_in2[x], tp1_in0[x]])
            in_sq_imag.extend([tp1_in1[x], tp1_in2[x], tp2_in0[x], tp2_in1[x]])

            fb_real.extend([tp3_in0[x], tp3_in1[x], tp3_in2[x], tp4_in0[x]])
            fb_imag.extend([tp4_in1[x], tp4_in2[x], tp5_in0[x], tp5_in1[x]])


        complx_in_sq = in_sq_real + np.multiply(in_sq_imag,1j)
        complx_fb = fb_real + np.multiply(fb_imag, 1j)

        #embed()
        #-----------------------------------------------------------------------------------------------------------

        print "Grabbing ss_pfb_real_dir and ss_pfb_imag_dir"
        print ""
        ss_pfb_real_dir = self.f.snapshots.ss_pfb_real_dir_ss.read(arm=False)['data']
        ss_pfb_imag_dir = self.f.snapshots.ss_pfb_imag_dir_ss.read(arm=False)['data']

        pfb_real0_dir = ss_pfb_real_dir['pfb2_r0']
        pfb_real1_dir = ss_pfb_real_dir['pfb2_r1']
        pfb_real2_dir = ss_pfb_real_dir['pfb2_r2']
        pfb_real3_dir = ss_pfb_real_dir['pfb2_r3']

        pfb_imag0_dir = ss_pfb_imag_dir['pfb2_i0']
        pfb_imag1_dir = ss_pfb_imag_dir['pfb2_i1']
        pfb_imag2_dir = ss_pfb_imag_dir['pfb2_i2']
        pfb_imag3_dir = ss_pfb_imag_dir['pfb2_i3']


        pfb_real_dir = []
        pfb_imag_dir = []

        for x in range(0, len(pfb_real0_dir)):
            pfb_real_dir.extend(
                [pfb_real0_dir[x], pfb_real1_dir[x], pfb_real2_dir[x], pfb_real3_dir[x]])

            pfb_imag_dir.extend(
                [pfb_imag0_dir[x], pfb_imag1_dir[x], pfb_imag2_dir[x], pfb_imag3_dir[x]])

        complx_dir = pfb_real_dir + np.multiply(pfb_imag_dir,1j)

        #-----------------------------------------------------------------------------------------------------------

        print "Grabbing ss_pfb_real_sq and ss_pfb_imag_sq"
        print ""
        ss_pfb_real_square = self.f.snapshots.ss_pfb_real_sq_ss.read(arm=False)['data']
        ss_pfb_imag_square = self.f.snapshots.ss_pfb_imag_sq_ss.read(arm=False)['data']

        pfb_real0_sq = ss_pfb_real_square['pfb2_r0']
        pfb_real1_sq = ss_pfb_real_square['pfb2_r1']
        pfb_real2_sq = ss_pfb_real_square['pfb2_r2']
        pfb_real3_sq = ss_pfb_real_square['pfb2_r3']

        pfb_imag0_sq = ss_pfb_imag_square['pfb2_i0']
        pfb_imag1_sq = ss_pfb_imag_square['pfb2_i1']
        pfb_imag2_sq = ss_pfb_imag_square['pfb2_i2']
        pfb_imag3_sq = ss_pfb_imag_square['pfb2_i3']


        pfb_real_sq = []
        pfb_imag_sq = []

        for x in range(0, len(pfb_real0_sq)):
            pfb_real_sq.extend(
                [pfb_real0_sq[x], pfb_real1_sq[x], pfb_real2_sq[x], pfb_real3_sq[x]])

            pfb_imag_sq.extend(
                [pfb_imag0_sq[x], pfb_imag1_sq[x], pfb_imag2_sq[x], pfb_imag3_sq[x]])

        complx_sq = pfb_real_sq + np.multiply(pfb_imag_sq,1j)

        #-----------------------------------------------------------------------------------------------------------

        print "Grabbing ss_pfb_sq1, ss_pfb_sq2, ss_pfb_sq3"
        print ""
        ss_pfb_sq1 = self.f.snapshots.ss_pfb_sq1_ss.read(arm=False)['data']
        ss_pfb_sq2 = self.f.snapshots.ss_pfb_sq2_ss.read(arm=False)['data']
        ss_pfb_sq3 = self.f.snapshots.ss_pfb_sq3_ss.read(arm=False)['data']

        pfb_real0_sq_full = ss_pfb_sq1['pfb2_r0']
        pfb_real1_sq_full = ss_pfb_sq1['pfb2_r1']
        pfb_real2_sq_full = ss_pfb_sq1['pfb2_r2']
        pfb_real3_sq_full = ss_pfb_sq2['pfb2_r3']

        pfb_imag0_sq_full = ss_pfb_sq2['pfb2_i0']
        pfb_imag1_sq_full = ss_pfb_sq2['pfb2_i1']
        pfb_imag2_sq_full = ss_pfb_sq3['pfb2_i2']
        pfb_imag3_sq_full = ss_pfb_sq3['pfb2_i3']

        pfb_real_sq_full = []
        pfb_imag_sq_full = []

        for x in range(0, len(pfb_real0_sq)):
            pfb_real_sq_full.extend(
                [pfb_real0_sq_full[x], pfb_real1_sq_full[x], pfb_real2_sq_full[x], pfb_real3_sq_full[x]])

            pfb_imag_sq_full.extend(
                [pfb_imag0_sq_full[x], pfb_imag1_sq_full[x], pfb_imag2_sq_full[x], pfb_imag3_sq_full[x]])

        complx_sq_full = pfb_real_sq_full + np.multiply(pfb_imag_sq_full,1j)

        #-----------------------------------------------------------------------------------------------------------


        print "Check Spectrum Counter (SS)"
        print "---------------------------"
        print "Spectrum Counter is %s" % self.f.registers.spectrum_counter_ss.read()
        print ""


        #plt.figure(1)
        #plt.ion()
        #plt.clf()
        #plt.plot(cwg)

        #plt.figure(2)
        #plt.ion()
        #plt.clf()
        #plt.subplot(211)
        #plt.plot(np.abs(complx_dir))
        #plt.subplot(212)
        #plt.semilogy(np.abs(complx_dir))

        plt.figure(3)
        plt.ion()
        plt.clf()
        plt.subplot(211)
        plt.plot(np.abs(complx_in_sq))
        plt.subplot(212)
        plt.semilogy(np.abs(complx_in_sq))

        plt.figure(4)
        plt.ion()
        plt.clf()
        plt.subplot(211)
        plt.plot(np.abs(complx_fb))
        plt.subplot(212)
        plt.semilogy(np.abs(complx_fb))

        plt.figure(5)
        plt.ion()
        plt.clf()
        plt.subplot(211)
        plt.plot(np.abs(complx_sq))
        plt.subplot(212)
        plt.semilogy(np.abs(complx_sq))

        #plt.figure(6)
        #plt.ion()
        #plt.clf()
        #plt.subplot(211)
        #plt.plot(np.abs(complx_sq_full))
        #plt.subplot(212)
        #plt.semilogy(np.abs(complx_sq_full))




        plt.show()

        print ""
        print "Disable System"
        print "--------------"
        self.f.registers.sys_en.write(en=0)

        print ""
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


