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

c=corr2.fxcorrelator.FxCorrelator('bob',config_source='/etc/corr/avdbyl_nb_half_test')
c.initialise(program=False,configure=False,require_epoch=False)

c.fops.set_fft_shift_all('8s')
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
#    for x in hosts:
#        print(x)
#
#        f = casperfpga.CasperFpga(x)
#        f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m32k_halfbw_2020-01-14_1505.fpg')
            
        # Setup mixer oscillator
        #-----------------------
#        mix_freq = ((100e6)*np.power(2,22))/1712e6
#       f.registers.freq_cwg_osc.write(frequency=mix_freq)
#        f.registers.fft_shift.write(fft_shift=21930) #21930, 55726, 21808
#        f.registers.control.write(sys_rst='pulse')
    
    
#main()