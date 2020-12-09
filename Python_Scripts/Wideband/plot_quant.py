import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

host = 'skarab020A03-01'

f = casperfpga.CasperFpga(host)

# Known good 2018 build
# ---------------------
f.get_system_information('/srv/bofs/feng/s_c856m32k_dbg_2019-10-14_1639.fpg')   

# Test FPGS
# ---------
#f.get_system_information('/srv/bofs/feng/s_c856m32k_dbg_2019-10-08_1817.fpg')   
#f.get_system_information('/home/avanderbyl/fpgs/s_c856m32k_2018_2019-10-30_1535.fpg')   

count = 0
while (count < 1):
    count = count + 1
    f.snapshots.snap_quant0_ss.arm(man_trig=False, man_valid=False)
    
    
    print 'Grabbing CD Out'  
    adc0_snap = f.snapshots.snap_adc0_ss.read()['data'] 
    
    adc_d0 = adc0_snap['p0_d0']
    adc_d1 = adc0_snap['p0_d1']
    adc_d2 = adc0_snap['p0_d2']
    adc_d3 = adc0_snap['p0_d3']
    adc_d4 = adc0_snap['p0_d4']
    adc_d5 = adc0_snap['p0_d5']
    adc_d6 = adc0_snap['p0_d6']
    adc_d7 = adc0_snap['p0_d7']
           
    adc0_out = []
                                   
    for x in range(0, len(adc_d0)):
        adc0_out.extend(
            [adc_d0[x], adc_d1[x], adc_d2[x], adc_d3[x], adc_d4[x], adc_d5[x], adc_d6[x], adc_d7[x]])
        
    
    
    
    
    
    
    
    quant_snap = f.snapshots.snap_quant0_ss.read(arm=False)['data'] 
            
    real0 = quant_snap['real0']
    imag0 = quant_snap['imag0']
    real1 = quant_snap['real1']
    imag1 = quant_snap['imag1']
    real2 = quant_snap['real2']
    imag2 = quant_snap['imag2']
    real3 = quant_snap['real3']
    imag3 = quant_snap['imag3']
             
    quant_real = []
    quant_imag = []
                           
    for x in range(0, len(real0)):
        quant_real.extend(
            [real0[x], real1[x], real2[x], real3[x]])
                            
    for x in range(0, len(imag0)):
        quant_imag.extend(
            [imag0[x], imag1[x], imag2[x], imag3[x]])
                
    q0_complx = quant_real + np.multiply(quant_imag, 1j)
            
 
    
    plt.figure(1)
    plt.clf()
    plt.plot(adc0_out)
 
    
    plt.figure(2)
    plt.clf()
    plt.semilogy(np.square(np.abs(q0_complx)))
    plt.show()

