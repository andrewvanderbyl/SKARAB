import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

HOST = 'skarab020303-01'

f = casperfpga.CasperFpga(HOST)

f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m1k_2019-01-14_1223.fpg')

# Setup mixer oscillator
mix_freq = ((100e6)*np.power(2,27))/1712e6
f.registers.scale_cwg_osc.write(scale=0.95)
f.registers.freq_cwg_osc.write(frequency=mix_freq)

# Set scale_p0_ddc0 and scale_p1_ddc0
f.registers.scale_p0_ddc0.write(scale=0.95)
f.registers.scale_p1_ddc0.write(scale=0.95)

f.registers.osc_sel.write(sel=0)

#f.registers.int_cwg_en.write(int_cwg=0)
#f.registers.control.write(cd_bypass=0)
f.registers.control.write(cnt_rst='pulse')
f.registers.control.write(sys_rst='pulse')


for x in range(1):
    print x

    # Arm snapshots
    f.snapshots.snap_adc0_ss.arm(man_trig=False, man_valid=False)
    
    f.snapshots.snap_ddc_in_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.snap_osc_ss.arm(man_trig=False, man_valid=False)
    
    f.snapshots.snap_mix_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.snap_mix1_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.snap_mix2_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.snap_mix3_ss.arm(man_trig=False, man_valid=False)
    
    f.snapshots.snap_ddc_out_ss.arm(man_trig=False, man_valid=False)
    
    f.snapshots.snap_fft_ss.arm(man_trig=False, man_valid=False)
 
    f.snapshots.snap_nb_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.snap_nb1_ss.arm(man_trig=False, man_valid=False)
    
    # Grab Snapshot data
    adc0 = f.snapshots.snap_adc0_ss.read(arm=False)['data']
 
    ddc_in_ss = f.snapshots.snap_ddc_in_ss.read(arm=False)['data']
    osc = f.snapshots.snap_osc_ss.read(arm=False)['data']
    
    mix = f.snapshots.snap_mix_ss.read(arm=False)['data']
    mix1 = f.snapshots.snap_mix1_ss.read(arm=False)['data']
    mix2 = f.snapshots.snap_mix2_ss.read(arm=False)['data']
    mix3 = f.snapshots.snap_mix3_ss.read(arm=False)['data']
        
    print x  
    ddc_out_ss = f.snapshots.snap_ddc_out_ss.read(arm=False)['data']
    
    fft_xil = f.snapshots.snap_fft_ss.read(arm=False)['data']
    
    nb0_1 = f.snapshots.snap_nb_ss.read(arm=False)['data']
    nb0_2 = f.snapshots.snap_nb1_ss.read(arm=False)['data']
    
    print x    
    adc0_0 = adc0['p0_d0']
    adc0_1 = adc0['p0_d1']
    adc0_2 = adc0['p0_d2']
    adc0_3 = adc0['p0_d3']
    adc0_4 = adc0['p0_d4']
    adc0_5 = adc0['p0_d5']
    adc0_6 = adc0['p0_d6']
    adc0_7 = adc0['p0_d7']
    adc_sync = adc0['sync']
    adc_dv = adc0['dv']
    

    osc_0 = osc['p0_d0']
    osc_1 = osc['p0_d1']
    osc_2 = osc['p0_d2']
    osc_3 = osc['p0_d3']
    osc_4 = osc['p0_d4']
    osc_5 = osc['p0_d5']
    osc_6 = osc['p0_d6']
    osc_7 = osc['p0_d7']
    osc_dv = osc['dv']
    osc_sync = osc['sync']
    
    ddc_in_0 = ddc_in_ss['p0_d0']
    ddc_in_1 = ddc_in_ss['p0_d1']
    ddc_in_2 = ddc_in_ss['p0_d2']
    ddc_in_3 = ddc_in_ss['p0_d3']
    ddc_in_4 = ddc_in_ss['p0_d4']
    ddc_in_5 = ddc_in_ss['p0_d5']
    ddc_in_6 = ddc_in_ss['p0_d6']
    ddc_in_7 = ddc_in_ss['p0_d7']
    ddc_in_dv = ddc_in_ss['dv']
    ddc_in_sync = ddc_in_ss['sync']
    
    mix_0 = mix['p0_d0']
    mix_1 = mix['p0_d1']
    mix_2 = mix['p0_d2']
    mix_3 = mix['p0_d3']
    mix_4 = mix['p0_d4']
    mix_5 = mix['p0_d5']
    mix_6 = mix['p0_d6']
    mix_7 = mix['p0_d7']
    mix_dv = mix['dv']
    mix_sync = mix['sync']
    
    mix1_0 = mix1['p0_d0']
    mix1_1 = mix1['p0_d1']
    mix1_2 = mix1['p0_d2']
    mix1_3 = mix1['p0_d3']
    mix1_4 = mix1['p0_d4']
    mix1_5 = mix1['p0_d5']
    mix1_6 = mix1['p0_d6']
    mix1_7 = mix1['p0_d7']
    mix1_dv = mix1['dv']
    mix1_sync = mix1['sync']

    mix2_0 = mix2['p0_d0']
    mix2_1 = mix2['p0_d1']
    mix2_2 = mix2['p0_d2']
    mix2_3 = mix2['p0_d3']
    
    mix3_4 = mix3['p0_d4']
    mix3_5 = mix3['p0_d5']
    mix3_6 = mix3['p0_d6']
    mix3_7 = mix3['p0_d7']
    mix2_dv = mix2['dv']
    mix2_sync = mix2['sync']
    
    ddc_out = ddc_out_ss['ddc0']
    ddc_out_dv = ddc_out_ss['dv']
    ddc_out_sync = ddc_out_ss['sync']
    
    fft_real = fft_xil['real']
    fft_imag = fft_xil['imag']
    fft_complx = fft_real + np.multiply(fft_imag, 1j)
    fft_sync = fft_xil['sync']
    fft_dv = fft_xil['dv']
    
    nb_r0 = nb0_1['real0']
    nb_r1 = nb0_1['real1']
    nb_r2 = nb0_1['real2']
    nb_r3 = nb0_2['real3']
    nb_i0 = nb0_1['imag0']
    nb_i1 = nb0_1['imag1']
    nb_i2 = nb0_1['imag2']
    nb_i3 = nb0_2['imag3']

    
    # --------------------------------------------------------------------
    pfb0_input = []
    pfb1_input = []
    
    for x in range(0, len(adc0_0)):
        pfb0_input.extend(
            [adc0_0[x], adc0_1[x], adc0_2[x], adc0_3[x], adc0_4[x], adc0_5[x], adc0_6[x], adc0_7[x]])
      
    # --------------------------------------------------------------------
    ddc_in = []
    
    for x in range(0, len(ddc_in_0)):
        ddc_in.extend(
            [ddc_in_0[x], ddc_in_1[x], ddc_in_2[x], ddc_in_3[x], ddc_in_4[x], ddc_in_5[x], ddc_in_6[x], ddc_in_7[x]])

    # --------------------------------------------------------------------
    osc_in = []
    
    for x in range(0, len(osc_0)):
        osc_in.extend(
            [osc_0[x], osc_1[x], osc_2[x], osc_3[x], osc_4[x], osc_5[x], osc_6[x], osc_7[x]])
        
    # --------------------------------------------------------------------
    mix_out = []
    for x in range(0, len(mix_0)):
        mix_out.extend(
            [mix_0[x], mix_1[x], mix_2[x], mix_3[x], mix_4[x], mix_5[x], mix_6[x], mix_7[x]])
    
    mix1_out = []
    for x in range(0, len(mix1_0)):
        mix1_out.extend(
            [mix1_0[x], mix1_1[x], mix1_2[x], mix1_3[x], mix1_4[x], mix1_5[x], mix1_6[x], mix1_7[x]])    

    mix23_out = []
    for x in range(0, len(mix2_0)):
        mix23_out.extend(
            [mix2_0[x], mix2_1[x], mix2_2[x], mix2_3[x], mix3_4[x], mix3_5[x], mix3_6[x], mix3_7[x]])    

    
    ## --------------------------------------------------------------------
    
    nb_real = []
    nb_imag = []
    
    for x in range(0, len(nb_r0)):
        nb_real.extend(
            [nb_r0[x], nb_r1[x], nb_r2[x], nb_r3[x]])
    
    for x in range(0, len(nb_i0)):
        nb_imag.extend(
            [nb_i0[x], nb_i1[x], nb_i2[x], nb_i3[x]])
    nb_complx_sq = nb_real + np.multiply(nb_imag, 1j)

    # --------------------------------------------------------------------
    
    print "Counters"
    print 'DDC Sync Count'
    print f.registers.ddc_sync_cnt.read()
    print 'NB Sync Count'
    print f.registers.nb_sync_cnt.read()
    
    # --------------------------------------------------------------------
    
#    plt.figure(1)
#    plt.clf()
#    plt.plot(pfb0_input)
#    plt.plot(adc0_0)
#    plt.plot(adc_dv)
#    plt.plot(adc_sync)

#    plt.figure(1)
#    plt.clf()
#    plt.plot(unpack0)
#    plt.plot(upack0_0)
#    plt.plot(upack0_dv)
#    plt.plot(upack0_sync)    
    
           
    #plt.figure(1)
    #plt.clf()
    #plt.plot(pfb1_input)
    #plt.plot(adc1_0)
    #plt.plot(adc1_dv)
    #plt.plot(adc1_sync)
    
#    plt.figure(2)
#    plt.clf()
#    plt.plot(ddc_in)
#    plt.plot(ddc_in_0)
#    plt.plot(ddc_in_dv)
        
    #plt.figure(4);
    #fft_ddc_in = np.fft.fft(ddc_in[5:5+1024])
    #plt.plot(np.abs(fft_ddc_in))
    #plt.semilogy(np.abs(fft_ddc_in))

#    plt.figure(3)
#    plt.clf()
#    plt.plot(mix23_out)
#    plt.plot(mix2_dv)  
#    plt.plot(mix2_0)  
    
#    plt.figure(4)
#    plt.clf()
#    plt.plot(mix1_out)
#    plt.plot(mix1_0)
#    plt.plot(mix_dv)
#    plt.plot(mix_sync)
#    
    
#    plt.figure(5)
#    plt.clf()
#    plt.plot(mix_out)
#    plt.plot(mix_0)
#    plt.plot(mix_dv)
#    plt.plot(mix_sync)
    
#    plt.figure(6)
#    plt.clf()
#    plt.plot(osc_in)
#    plt.plot(osc_dv)
#    plt.plot(osc_0)
#    
#    
#    plt.figure(7);
#    fft_mix = np.fft.fft(mix_out[1:(1+4096)])
#    plt.semilogy(np.abs(fft_mix))
#    
#    plt.figure(8);
#    plt.plot(ddc_out)
#    plt.plot(ddc_out_dv)
#    plt.plot(ddc_out_sync)
    
    
    plt.figure(9);
    fft_ddc_out = np.fft.fft(ddc_out[1:(1+4096)])
    plt.semilogy(np.abs(fft_ddc_out))
    
    
    plt.figure(10)
    plt.semilogy(np.abs(fft_complx))
    #plt.plot(np.abs(fft_complx))
    plt.plot(np.multiply(fft_dv,0.1))
    plt.plot(np.multiply(fft_sync,0.5))
    
    plt.figure(11)
    plt.semilogy(np.abs(nb_complx_sq))
        
    plt.show()

