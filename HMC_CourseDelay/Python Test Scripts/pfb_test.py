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
prog_file = "/tmp/pfb_fft_test_2017-11-15_1206.fpg"

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

        print "FFT Shift"
        print "---------"
        self.f.registers.fft_shift.write(fft_shift=0)
        print "FFT shift is %s" % self.f.registers.fft_shift.read()
        print ""

        print "Spectrum Accumulation"
        print "---------------------"
        self.f.registers.spectrum_limit.write(reg=np.power(2,accumulation_len))
        print "Spectrum accumulation limit is %s" % self.f.registers.spectrum_limit.read()
        print ""

        self.f.registers.tvg_sel.write(tvg_sel=0)
        self.f.registers.debug_sel.write(tvg_sel=0)

        print "Set the DSim"
        print "------------"

        # Set the CWG scale
        self.f.registers.scale_cwg0.write(scale=0.25)
        self.f.registers.scale_out0.write(scale=1.0)

        # Set the frequency
        self.f.registers.freq_cwg0.write(frequency=8192000)

        # Noise Control
        self.f.registers.scale_wng0.write(scale=0.5)

        # Arm the Snapshot Blocks
        # -----------------------
        print 'Arming Snapblocks'
        print "-----------------"
        print ""
        #self.f.snapshots.ss_pfb_real_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        #self.f.snapshots.ss_pfb_imag_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_pfb_real_sq_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_pfb_imag_sq_ss.arm(man_trig=trig_mode, man_valid=valid_mode)

        self.f.snapshots.ss_pfb_real_dir_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.f.snapshots.ss_pfb_imag_dir_ss.arm(man_trig=trig_mode, man_valid=valid_mode)

        print 'Reset'
        print "-----"
        print ""
        # Sync Control
        self.f.registers.sys_rst.write(rst='pulse')


        print "Check Sync"
        print "----------"
        print "PFB Sync in %s" % self.f.registers.pfbin_sync_count.read()
        print "PFB Sync out %s" % self.f.registers.pfbout_sync_count.read()
        print ""

        print "PFB OF"
        print "------"
        print "PFB OF is %s" % self.f.registers.pfb_of.read()
        print ""



        print "Check Spectrum Counter"
        print "----------------------"
        print "Spectrum Counter is %s" % self.f.registers.spectrum_counter.read()
        print ""

        while self.f.registers.spectrum_counter.read() < self.f.registers.spectrum_limit.read():
            print "Spectrum Counter is %s" % self.f.registers.spectrum_counter.read()


        print ""
        print 'Grabbing Snapshot Data'
        print "----------------------"
        print ""


        print "Grabbing ss_pfb_real_dir and ss_pfb_imag_dir"
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

        for x in range(0, len(pfb_real_dir)):
            pfb_real_dir.extend(
                [pfb_real0_dir[x], pfb_real1_dir[x], pfb_real2_dir[x], pfb_real3_dir[x]])

            pfb_imag_dir.extend(
                [pfb_imag0_dir[x], pfb_imag1_dir[x], pfb_imag2_dir[x], pfb_imag3_dir[x]])

        complx_dir = pfb_real_dir + np.multiply(pfb_imag_dir,1j)

        '''
        print "Grabbing ss_pfb_real_ss and ss_pfb_imag_ss"
        ss_pfb_real = self.f.snapshots.ss_pfb_real_ss.read(arm=False)['data']
        ss_pfb_imag = self.f.snapshots.ss_pfb_imag_ss.read(arm=False)['data']

        pfb_real0 = ss_pfb_real['pfb2_r0']
        pfb_real1 = ss_pfb_real['pfb2_r1']
        pfb_real2 = ss_pfb_real['pfb2_r2']
        pfb_real3 = ss_pfb_real['pfb2_r3']

        pfb_imag0 = ss_pfb_imag['pfb2_i0']
        pfb_imag1 = ss_pfb_imag['pfb2_i1']
        pfb_imag2 = ss_pfb_imag['pfb2_i2']
        pfb_imag3 = ss_pfb_imag['pfb2_i3']

        pfb_real = []
        pfb_imag = []

        for x in range(0, len(pfb_real0)):
            pfb_real.extend(
                [pfb_real0[x], pfb_real1[x], pfb_real2[x], pfb_real3[x]])

            pfb_imag.extend(
                [pfb_imag0[x], pfb_imag1[x], pfb_imag2[x], pfb_imag3[x]])

        '''

        print "Grabbing ss_pfb_real_sq and ss_pfb_imag_sq"
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



        plt.figure(1)
        plt.ion()
        plt.clf()
        plt.plot(np.abs(np.abs(complx_dir)))

        plt.figure(2)
        plt.ion()
        plt.clf()
        plt.semilogy(np.abs(np.abs(complx_dir)))

        plt.figure(3)
        plt.ion()
        plt.semilogy(np.abs(np.abs(complx_sq)))



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


