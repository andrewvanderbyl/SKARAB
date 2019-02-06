import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

hosts = ['skarab020303-01','skarab020308-01','skarab02030A-01','skarab02030E-01']


for x in hosts:
    print x

    f = casperfpga.CasperFpga(x)

    #f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m1k_temp_2019-01-31_1406.fpg')
    f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m1k_2019-02-06_0848.fpg')
    
    # Setup mixer oscillator
    mix_freq = ((100e6)*np.power(2,27))/1712e6
    f.registers.scale_cwg_osc.write(scale=0.95)
    f.registers.freq_cwg_osc.write(frequency=mix_freq)
    
    tvg_freq = ((108359375)*np.power(2,27))/1712e6
    f.registers.scale_cwg_osc1.write(scale=0.95)
    f.registers.freq_cwg_osc1.write(frequency=tvg_freq)
    
    # Set scale_p0_ddc0 and scale_p1_ddc0
    f.registers.scale_p0_ddc0.write(scale=0.95)
    f.registers.scale_p1_ddc0.write(scale=0.95)
    
    f.registers.dbg_sel.write(sel=0) #0 = Dsim input; 1 = Osc_tvg
    f.registers.osc_temp_dv_sel.write(sel=0) #0 = constant dv; 1 = periodic dv
    
    
    # set sync and dv mus sel
    f.registers.sync_del_sel.write(sel=0)
    f.registers.dv_del_sel.write(sel=0)
    f.registers.d0_del_sel.write(sel=0)
    
    f.registers.osc_sel.write(sel=0) #0 = Osc; 1 = input TVG
    
    f.registers.munge_sel.write(sel=0) #0 = munge; 1 = no munge
    
    f.registers.adc_munge.write(sel=0) #0 = no munge; 1 = munge
    f.registers.osc_munge.write(sel=0) #0 = no munge; 1 = munge

    # Set Delay values
    f.registers.delay0.write(initial=0)
    f.registers.delta_delay0.write(delta=0)
    f.registers.phase0.write(initial=0)
    f.registers.phase0.write(delta=0)
    
#    f.registers.fd0_delay.write(initial=0)
#    f.registers.fd0_delta_delay.write(delta=0)
#    f.registers.fd0_phase.write(initial=0)
#    f.registers.fd0_phase.write(delta=0)
    
    f.registers.tl_cd0_control0.write(load_immediate=0)
    f.registers.tl_cd0_control0.write(arm='pulse')
    
    
    #f.registers.int_cwg_en.write(int_cwg=0)
    f.registers.control.write(cd_bypass=0)
    
    f.registers.control.write(cnt_rst='pulse')
    f.registers.control.write(sys_rst='pulse')


