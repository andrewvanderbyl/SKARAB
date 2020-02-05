#! /usr/bin/python3
""" Setup FEngines for the Narrowband Correlator 

Usage:
    Mixing frequency is required
    FFT_Shift is required
    Hosts is required
"""

import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

hosts = ['skarab020a03-01','skarab020918-01','skarab02091b-01','skarab020A45-01']

print(hosts)

c=corr2.fxcorrelator.FxCorrelator('bob',config_source='/etc/corr/avdbyl_nb_53.ini')
c.initialise(program=False,configure=False,require_epoch=False)

c.fops.set_fft_shift_all('12s')
c.fops.set_center_freq(100e6)


#if __name__=='__main__':
#    main()

#def main():
#    setup_feng()

#def setup_feng():
#    """Setup the FEngine Hosts in the correlator
    
#    Args: 
#        None
#    """
for x in hosts:
    print(x)


    f = casperfpga.CasperFpga(x)
    f.get_system_information('/home/avanderbyl/fpgs/s_c53m32k_2020-01-27_0725.fpg')
    #f.registers.demux_sel.write(sel=0)

    if x == 'skarab020a03-01':
        print('True')
        
        # Arm snapshots
        f.snapshots.ddc_ss.arm(man_trig=False, man_valid=False)
        f.snapshots.ss_cwg_ss.arm(man_trig=False, man_valid=False)
        f.snapshots.DDC_ddc_ss.arm(man_trig=False, man_valid=False)
        f.snapshots.DDC_dec_ss.arm(man_trig=False, man_valid=False)
        f.snapshots.DDC_mix_ss.arm(man_trig=False, man_valid=False)
        
        cwg = f.snapshots.ss_cwg_ss.read(arm=False)['data']
        cwg_re = cwg['osc_re']
        cwg_im = cwg['osc_im']
        pol_re = cwg['pol0_re']
        pol_im = cwg['pol0_im']
        
        cwg_sync = cwg['sync']
        cwg_dv = cwg['dv']


        mix = f.snapshots.DDC_mix_ss.read(arm=False)['data']
        mix_re = mix['pol0_re1']
        mix_sync = mix['sync']
        mix_dv = mix['dv']

        dec = f.snapshots.DDC_dec_ss.read(arm=False)['data']
        dec_re = dec['pol0_re1']
        dec_sync = dec['sync']
        dec_dv = dec['dec_dv']
        load_dv = dec['load_dv']

        ddc = f.snapshots.ddc_ss.read(arm=False)['data']
        ddc_re = ddc['pol0_re']
        ddc_im = ddc['pol0_im']
        ddc_sync = ddc['sync']
        ddc_dv = ddc['dv']

        ddc_int = f.snapshots.DDC_ddc_ss.read(arm=False)['data']
        ddc_int_re1 = ddc_int['pol0_re1']
        ddc_int_re9 = ddc_int['pol0_re9']
        ddc_int_re17 = ddc_int['pol0_re17']
        ddc_int_re25 = ddc_int['pol0_re25']
      
        ddc_int_sync = ddc_int['sync']
        ddc_int_dv = ddc_int['dv']
    
        plt.figure(1)
        plt.clf()
        plt.subplot(211)
        plt.plot(mix_re)
        plt.subplot(212)
        plt.plot(mix_dv)
        plt.plot(mix_sync)

        plt.figure(2)
        plt.clf()
        plt.subplot(211)
        plt.plot(dec_re)
        plt.subplot(212)
        plt.plot(dec_dv)
        plt.plot(load_dv)
        plt.plot(dec_sync)

        plt.figure(3)
        plt.clf()
        plt.subplot(211)
        plt.plot(ddc_int_re1)
        plt.plot(ddc_int_re9)        
        plt.subplot(212)
        plt.plot(ddc_int_dv)
        plt.plot(ddc_int_sync)

        plt.figure(4)
        plt.clf()
        plt.subplot(211)
        plt.plot(ddc_re)
        plt.plot(ddc_im)        
        plt.subplot(212)
        plt.plot(ddc_dv)
        plt.plot(ddc_sync)

        plt.figure(5)
        plt.clf()
        plt.subplot(311)
        plt.plot(cwg_re)
        plt.plot(cwg_im)        
        plt.subplot(312)
        plt.plot(pol_re)
        plt.plot(pol_im)   
        plt.subplot(313)
        plt.plot(ddc_dv)
        plt.plot(ddc_sync)


        plt.show()
 

