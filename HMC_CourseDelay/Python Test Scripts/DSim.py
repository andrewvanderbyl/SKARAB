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

HOST1 = 'skarab020304-01'
HOST2 = 'skarab020307-01'
roach_HOST = 'roach020A11'

# Programming file(s)
#prog_file_dsim = "/tmp/s_deng_rev1_13_wide_2017-11-27_1150.fpg"
#prog_file_dsim = "/tmp/s_deng_rev1_13_wide_2017-11-27_1657.fpg"
#prog_file_dsim = "/tmp/s_deng_rev1_13_wide_2017-11-28_1156.fpg"
#prog_file_dsim = "/tmp/s_deng_rev1_13_wide_2017-11-28_1355.fpg"
#prog_file_dsim = "/tmp/s_deng_rev1_13_wide_2017-11-28_1547.fpg"

#prog_file_dsim = "/tmp/s_deng_rev1_13_wide_2017-11-28_1718.fpg"

#prog_file_dsim = "/tmp/s_deng_rev1_13_wide_2017-11-29_1118.fpg"
#prog_file_dsim = "/tmp/s_deng_rev1_13_wide_2017-11-29_1406.fpg"
#prog_file_dsim = "/tmp/s_deng_rev1_13_wide_2017-12-03.fpg"
#prog_file_dsim = "/tmp/s_deng_rev1_13_wide_2017-12-11_0659.fpg"
#prog_file_dsim = "/tmp/s_deng_rev1_13_wide_2017-12-11_1256.fpg"
prog_file_dsim = "/tmp/s_deng_rev1_13_wide_2017-12-12_0951.fpg"




#prog_file_dsim = "/tmp/s_deng_tvg_rev1_13_ramp_2017-11-22_0856.fpg"

#prog_file_feng = "/tmp/s_c856m4k_2017-11-17_0846.fpg"
prog_file_feng = "/tmp/s_c856m4k_2017-11-21_1714.fpg"

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

        print "Test DSim on SKARAB using FEng"

    # -------------------------------------------------------------------------------------------------------------
    def setup_FPGA_skarab_feng(self):

        # Create FPGA Object
        self.f = casperfpga.CasperFpga(HOST1)

        print 'FPGA Object Created'
        print "Communicating to SKARAB: %s" % HOST1

        try:
            self.f.upload_to_ram_and_program(prog_file_feng)
            print "Programming FPGA done"

        except:
            print "Programming Failed"

    def skarab_info_feng(self):
        print 'Grabbing System info'
        print "--------------------"

        print "Communicating to SKARAB: %s" % HOST1

        self.f = casperfpga.CasperFpga(HOST1)

        self.f.get_system_information(prog_file_feng)

        print 'Grabbing System info: Done'
        print "--------------------"
        print ''

    # -------------------------------------------------------------------------------------------------------------

    def setup_FPGA_skarab_dsim(self):

        # Create FPGA Object
        self.d = casperfpga.CasperFpga(HOST2)

        print 'FPGA Object Created'
        print "Communicating to SKARAB: %s" % HOST2

        try:
            self.d.upload_to_ram_and_program(prog_file_dsim)
            print "Programming FPGA done"

        except:
            print "Programming Failed"


    def skarab_info_dsim(self):
        print 'Grabbing System info'
        print "--------------------"

        print "Communicating to SKARAB: %s" % HOST2

        self.d = casperfpga.CasperFpga(HOST2)

        self.d.get_system_information(prog_file_dsim)


        print 'Grabbing System info: Done'
        print "--------------------"
        print ''

    # -------------------------------------------------------------------------------------------------------------

    def roach2_info(self):

        print 'Grabbing System info'
        print "--------------------"

        print "Communicating to ROACH: %s" % roach_HOST

        self.dr = casperfpga.CasperFpga(roach_HOST)

        self.dr.get_system_information()


        print 'Grabbing System info: Done'
        print "--------------------"
        print ''

    # -------------------------------------------------------------------------------------------------------------



    def run_dsim_roach(self, arm_mode, trig_mode, valid_mode):

        self.roach2_info()

        #print "Set IP Addr"
        #print "-----------"
        #print "Gbe0 is: 239.2.0.64"
        #self.f.registers.gbe_iptx0.write(reg=4009885760 + 4)
        #print "Gbe0 is: 239.2.0.65"
        #self.f.registers.gbe_iptx1.write(reg=4009885761 + 4)
        #print "Gbe0 is: 239.2.0.66"
        #self.f.registers.gbe_iptx2.write(reg=4009885762 + 4)
        #print "Gbe0 is: 239.2.0.67"
        #self.f.registers.gbe_iptx3.write(reg=4009885763 + 4)

        print "iptx0: %s" % self.d.registers.gbe_iptx0.read()
        print "iptx1: %s" % self.d.registers.gbe_iptx1.read()
        print "iptx2: %s" % self.d.registers.gbe_iptx2.read()
        print "iptx3: %s" % self.d.registers.gbe_iptx3.read()

        #print "Setting Port 7148"
        #self.f.registers.gbe_porttx.write(reg=7148)
        print "Port: %s" % self.d.registers.gbe_porttx.read()

        print "Starting DSim"
        print "-------------"

        # Set the DSim CWG0

        # Set the CWG scale
        self.d.registers.scale_cwg0.write(scale=0.5)
        self.d.registers.scale_out0.write(scale=0.5)

        self.d.registers.scale_cwg1.write(scale=0.5)
        self.d.registers.scale_out1.write(scale=0.5)

        # Set the frequency
        self.d.registers.freq_cwg0.write(frequency=8192000)
        self.d.registers.freq_cwg1.write(frequency=1000000)

        # Noise Control
        self.d.registers.scale_wng0.write(scale=0.0)
        self.d.registers.scale_wng1.write(scale=0.0)
        self.d.registers.scale_wng_corr.write(scale=0.0)

        # TVG Select
        #self.d.registers.orig_control.write(tvg_select0=1)
        #self.d.registers.orig_control.write(tvg_select1=1)

        #self.d.registers.test_control.write(sel_ramp80=1)
        #self.d.registers.test_control.write(rst_ramp80=0)

        # Traffic Control
        #self.d.registers.pol_traffic_trigger.write(pol0_tx_trigger=1)
        #self.d.registers.pol_traffic_trigger.write(pol1_tx_trigger=1)

        #self.d.registers.pol_tx_always_on.write(pol0_tx_always_on=1)
        #self.d.registers.pol_tx_always_on.write(pol1_tx_always_on=1)

        # Source Control
        #self.d.registers.src_sel_cntrl.write(src_sel_0=0)
        #self.d.registers.src_sel_cntrl.write(src_sel_1=0)

        # Sync Control
        #self.d.registers.orig_control.write(msync=1)
        #self.d.registers.orig_control.write(msync=0)
        #self.d.registers.gbecontrol.write(gbe0=1, gbe1=1, gbe2=1, gbe3=1)

        print "Done"
        print "----"

    def run_dsim_skarab(self, arm_mode, trig_mode, valid_mode):

        self.skarab_info_dsim()

        print self.d.system_info


        # Disable GBE's
        print ""
        print "Disabling Gbes"
        print ""
        self.d.registers.gbecontrol.write_int(0)


        self.d.registers.control.write(status_clr='pulse')
        #self.d.registers.control.write(gbe_rst='pulse')

        print ""
        print self.d.gbes.forty_gbe.read_counters()
        print ""

        print "Set IP Addr"
        print "-----------"
        print "Gbe0 is: 239.2.0.72"
        self.d.registers.gbe_iptx0.write(reg=4009885768)
        print "Gbe0 is: 239.2.0.73"
        self.d.registers.gbe_iptx1.write(reg=4009885769)
        print "Gbe0 is: 239.2.0.74"
        self.d.registers.gbe_iptx2.write(reg=4009885770)
        print "Gbe0 is: 239.2.0.75"
        self.d.registers.gbe_iptx3.write(reg=4009885771)
        print ""

        #self.d.registers.orig_control.write(mrst='pulse')
        #self.d.registers.orig_control.write(msync='pulse')
        #if self.d.gbes[0].get_port() != 30000:
        self.d.gbes.forty_gbe.set_port(30000)
        self.d.registers.gbe_porttx.write(reg=30000)
        print "Port: %s" % self.d.registers.gbe_porttx.read()
        print ""

        print "iptx0: %s" % self.d.registers.gbe_iptx0.read()
        print "iptx1: %s" % self.d.registers.gbe_iptx1.read()
        print "iptx2: %s" % self.d.registers.gbe_iptx2.read()
        print "iptx3: %s" % self.d.registers.gbe_iptx3.read()
        print ""

        self.d.registers.receptor_id.write(pol0_id=0, pol1_id=1)

        # ramp 80 or ramp 64?
        self.d.registers.test_control.write(sel_ramp80=True, rst_ramp80='pulse')

        print "Starting DSim"
        print "-------------"
        print ""

        # Set the DSim CWG0

        # Set the CWG scale
        self.d.registers.scale_cwg0.write(scale=0.5)
        self.d.registers.scale_out0.write(scale=0.5)

        self.d.registers.scale_cwg1.write(scale=0.5)
        self.d.registers.scale_out1.write(scale=0.5)

        # Set the frequency
        self.d.registers.freq_cwg0.write(frequency=1000000)
        self.d.registers.freq_cwg1.write(frequency=1000000)

        # Noise Control
        self.d.registers.scale_wng0.write(scale=0.0)
        self.d.registers.scale_wng1.write(scale=0.0)
        self.d.registers.scale_wng_corr.write(scale=0.0)

        # TVG Select
        self.d.registers.orig_control.write(tvg_select0=1)
        self.d.registers.orig_control.write(tvg_select1=1)

        #self.d.registers.test_control.write(sel_ramp80=1)
        #self.d.registers.test_control.write(rst_ramp80=0)

        # Traffic Control
        self.d.registers.pol_traffic_trigger.write(pol0_tx_trigger=1)
        self.d.registers.pol_traffic_trigger.write(pol1_tx_trigger=1)

        self.d.registers.pol_tx_always_on.write(pol0_tx_always_on=1)
        self.d.registers.pol_tx_always_on.write(pol1_tx_always_on=1)

        # Source Control
        self.d.registers.src_sel_cntrl.write(src_sel_0=0)
        self.d.registers.src_sel_cntrl.write(src_sel_1=0)


        # Sys Reset
        #print ""
        #print "Reset System"
        #print ""
        #self.d.registers.control.write(status_clr='pulse')
        #self.d.registers.control.write(gbe_rst='pulse')

        # Sync Control
        self.d.registers.orig_control.write(mrst='pulse')
        self.d.registers.orig_control.write(msync='pulse')

        # Arm the Snapshot Blocks
        # -----------------------
        print 'Arming Snapblocks'
        print "-----------------"

        self.d.snapshots.ss_fifo_in_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.d.snapshots.ss_localtime_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.d.snapshots.ss_cwg0_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        self.d.snapshots.ss_cwg1_ss.arm(man_trig=trig_mode, man_valid=valid_mode)

        #self.d.snapshots.ss_gbe_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        #self.d.snapshots.ss_gbe1_ss.arm(man_trig=trig_mode, man_valid=valid_mode)
        #self.d.snapshots.ss_gbe2_ss.arm(man_trig=trig_mode, man_valid=valid_mode)

        #print ""
        #print self.d.registers.gbecontrol.read()

        #print ""
        #print "Enable Gbes"
        #print ""
        #self.d.registers.gbecontrol.write(gbe0=1, gbe1=1, gbe2=1, gbe3=1)



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
        ss_cwg0 = self.d.snapshots.ss_cwg0_ss.read(arm=False)['data']

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



        ss_cwg1 = self.d.snapshots.ss_cwg1_ss.read(arm=False)['data']

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


        #print "Grabbing gbe ss"
        #ss_gbe_ss = self.d.snapshots.ss_gbe_ss.read(arm=False)['data']

        #gbe_rst = ss_gbe_ss['rst']
        #gbe_dv = ss_gbe_ss['dv']
        #gbe_txip = ss_gbe_ss['txip']
        #gbe_port = ss_gbe_ss['port']
        #gbe_eof = ss_cwg1['eof']
        #gbe_w0 = ss_cwg1['w0']

        #print ''
        #print gbe_rst[0:100]
        #print ''
        #print gbe_dv[0:100]
        #print ''
        #print gbe_txip[0:100]
        #print ''
        #print gbe_port[0:100]
        #print ''
        #print gbe_eof[0:100]
        #print ''
        #print gbe_w0[0:100]
        #print ''

        #print "localtime is %s" % localtime

        # Noise Histogram
        hist0 = np.histogram(cwg0)
        hist1 = np.histogram(cwg1)


        #plt.figure(1)
        #plt.ion()
        #plt.clf()
        #plt.plot(cwg0)

        #plt.figure(2)
        #plt.ion()
        #plt.clf()
        #plt.plot(cwg1)

        #plt.figure(3)
        #plt.ion()
        #plt.clf()
        #plt.plot(fifo_in)

        #plt.figure(4)
        #plt.ion()
        #plt.clf()
        #plt.plot(hist0[0])
        #plt.plot(hist1[0])

        plt.show()

        print ""
        print "Enable Gbes"
        print ""
        self.d.registers.gbecontrol.write_int(15)



        print self.d.registers.gbecontrol.read()
        print ""
        print self.d.gbes.forty_gbe.read_counters()

        #print ""
        #print "Disabling Gbes"
        #print ""
        #self.d.registers.gbecontrol.write_int(0)

        #print ""
        #print "Reset System"
        #print ""
        #self.d.registers.control.write(status_clr='pulse')
        #self.d.registers.control.write(gbe_rst='pulse')

        # Sync Control
        #self.d.registers.orig_control.write(mrst='pulse')
        #self.d.registers.orig_control.write(msync='pulse')

        print ""
        print " *** Done ***"
        print ""

    def feng_rx_data(self,data_port=7148, sd_ip='127.0.0.1', sd_port=7149, **kwargs):

        print "RX DSim data on Feng"
        print "--------------------"
        print ''

        #print 'Connect to DSim and configure'
        #print ""
        #self.roach2_info()

        print 'Connect to FEng and configure'
        print ""
        self.skarab_info_feng()

        print "Setup multicast receive"
        print ""
        #g = self.f.gbes["gbe0"]
        #g.multicast_receive?
        #g.multicast_receive('239.2.0.64', 4)

        g = self.f.gbes["gbe0"]
        # g.multicast_receive?
        #g.multicast_receive('239.2.0.64', 4)
        g.multicast_receive('239.2.0.72', 4)

        port = 30000
        print "Setting port to %s" % port
        g.set_port(port)

        print "Setup multicast receive done"
        print ""

        #Setup FEng
        self.f.registers.control.write(adc_snap_arm=1)
        self.f.registers.control.write(adc_snap_trig_select=1)

        # Plot ADC data
        # Arm the snapblocks
        print "Arming SS"
        print ""
        self.f.snapshots.snap_adc0_ss.arm(man_trig=True, man_valid=True)
        #self.f.snapshots.snap_adc1_ss.arm(man_trig=False, man_valid=False)


        print "RX counter %s" % self.f.gbes.gbe0.read_counters()['gbe0_rxctr']
        print "RX eof counter %s" % self.f.gbes.gbe0.read_counters()['gbe0_rxeofctr']
        print "RX err counter %s" % self.f.gbes.gbe0.read_counters()['gbe0_rxerrctr']
        print "RX valid counter %s" % self.f.gbes.gbe0.read_counters()['gbe0_rxvldctr']

        print "Grabbing RX Snap"
        snap = self.f.gbes.gbe0.read_rxsnap()['data']



        # Grab SS data
        print "Grabbing SS"
        print ""
        snap_adc0 = self.f.snapshots.snap_adc0_ss.read(arm=False)['data']
        #snap_adc1 = self.f.snapshots.snap_adc1_ss.read(arm=False)['data']

        p0_d0 = snap_adc0['p0_d0']
        p0_d1 = snap_adc0['p0_d1']
        p0_d2 = snap_adc0['p0_d2']
        p0_d3 = snap_adc0['p0_d3']
        p0_d4 = snap_adc0['p0_d4']
        p0_d5 = snap_adc0['p0_d5']
        p0_d6 = snap_adc0['p0_d6']
        p0_d7 = snap_adc0['p0_d7']

        print "Extracting Data"
        print ""
        # Recombine
        p0_data = []

        for x in range(0, len(p0_d0)):
            p0_data.extend([p0_d0[x], p0_d1[x], p0_d2[x], p0_d3[x], p0_d4[x], p0_d5[x], p0_d6[x], p0_d7[x]])


        plt.figure(1)
        plt.ion()
        plt.clf()
        plt.plot(p0_data)
        plt.show()

        #plt.figure(1)
        #plt.ion()
        #plt.clf()
        #plt.plot(snap)
        #plt.show()


    def run_dsim_skarab_ramp(self, arm_mode, trig_mode, valid_mode):

        self.skarab_info_dsim()

        # Disable GBE's
        print ""
        print "Disabling Gbes"
        print ""
        self.d.registers.gbecontrol.write_int(0)

        self.d.registers.control.write(status_clr='pulse')
        self.d.registers.control.write(gbe_rst='pulse')

        #self.d.registers.control.write(mrst='pulse')
        #self.d.registers.control.write(msync='pulse')

        print ""
        print self.d.gbes.forty_gbe.read_counters()
        print ""

        print "Set IP Addr"
        print "-----------"
        print "Gbe0 is: 239.2.0.72"
        self.d.registers.gbe_iptx0.write(reg=4009885768)
        print "Gbe0 is: 239.2.0.73"
        self.d.registers.gbe_iptx1.write(reg=4009885769)
        print "Gbe0 is: 239.2.0.74"
        self.d.registers.gbe_iptx2.write(reg=4009885770)
        print "Gbe0 is: 239.2.0.75"
        self.d.registers.gbe_iptx3.write(reg=4009885771)
        print ""

        self.d.gbes.forty_gbe.set_port(30000)
        self.d.registers.gbe_porttx.write(reg=30000)
        print "Port: %s" % self.d.registers.gbe_porttx.read()
        print ""

        print "iptx0: %s" % self.d.registers.gbe_iptx0.read()
        print "iptx1: %s" % self.d.registers.gbe_iptx1.read()
        print "iptx2: %s" % self.d.registers.gbe_iptx2.read()
        print "iptx3: %s" % self.d.registers.gbe_iptx3.read()
        print ""

        self.d.registers.receptor_id.write(pol0_id=0, pol1_id=1)

        # ramp 80 or ramp 64?
        self.d.registers.test_control.write(sel_ramp80=False, rst_ramp80='pulse')

        print ""
        print "Enable Gbes"
        print ""
        self.d.registers.gbecontrol.write_int(15)

        print self.d.registers.gbecontrol.read()
        print ""
        print self.d.gbes.forty_gbe.read_counters()

        print ""
        print " *** Done ***"
        print ""


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


