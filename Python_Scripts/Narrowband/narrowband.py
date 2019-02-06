import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

HOST = 'skarab020303-01'

f = casperfpga.CasperFpga(HOST)

#f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m1k_2019-01-21_1557.fpg')
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

#f.registers.fd0_delay.write(initial=0)
#f.registers.fd0_delta_delay.write(delta=0)
#f.registers.fd0_phase.write(initial=0)
#f.registers.fd0_phase.write(delta=0)

f.registers.tl_cd0_control0.write(load_immediate=0)
f.registers.tl_cd0_control0.write(arm='pulse')


#f.registers.int_cwg_en.write(int_cwg=0)
f.registers.control.write(cd_bypass=0)

# Hold in reset
f.registers.control.write(sys_rst=1)

f.registers.control.write(cnt_rst='pulse')




for x in range(1):

    # Arm snapshots
    f.snapshots.snap_adc0_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.snap_adc1_ss.arm(man_trig=False, man_valid=False)
    
    #f.snapshots.snap_hmc_in_ss.arm(man_trig=False, man_valid=False)
    #f.snapshots.snap_hmc_out_ss.arm(man_trig=False, man_valid=False)
    
   
    #f.snapshots.snap_ddc_in_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.snap_fft_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.snap_fft1_ss.arm(man_trig=False, man_valid=False)
  
    f.snapshots.snap_nb_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.snap_nb1_ss.arm(man_trig=False, man_valid=False)

    f.snapshots.phase_compensation0_snap_fd_gen_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.phase_compensation0_fd_fs_snap_lookup_ss.arm(man_trig=False, man_valid=False)
    
    f.snapshots.snap_quant0_ss.arm(man_trig=False, man_valid=False)
#    f.snapshots.snap_quant1_ss.arm(man_trig=False, man_valid=False)

    # Release Reset
    f.registers.control.write(sys_rst='pulse')

    
    # Grab Snapshot data
    adc0 = f.snapshots.snap_adc0_ss.read(arm=False)['data']
    adc1 = f.snapshots.snap_adc1_ss.read(arm=False)['data']
    
    #hmc_in_ss = f.snapshots.snap_hmc_in_ss.read(arm=False)['data']
    
    #hmc_out_ss = f.snapshots.snap_hmc_out_ss.read(arm=False)['data']
        
    #ddc_in_ss = f.snapshots.snap_ddc_in_ss.read(arm=False)['data']
   
    fft_xil = f.snapshots.snap_fft_ss.read(arm=False)['data']
    fft_xil1 = f.snapshots.snap_fft1_ss.read(arm=False)['data']
    
    nb0_1 = f.snapshots.snap_nb_ss.read(arm=False)['data']
    nb0_2 = f.snapshots.snap_nb1_ss.read(arm=False)['data']

    fd_gen_ss = f.snapshots.phase_compensation0_snap_fd_gen_ss.read(arm=False)['data']
    lookup_ss = f.snapshots.phase_compensation0_fd_fs_snap_lookup_ss.read(arm=False)['data']

    quant0_ss = f.snapshots.snap_quant0_ss.read(arm=False)['data']
    
#    quant1_ss = f.snapshots.snap_quant1_ss.read(arm=False)['data']
    
    #Grab HMC Data
#    print f.registers.cd_hmc_hmc_delay_sync_status0.read()
#    print ''
#    print f.registers.cd_hmc_hmc_delay_status0.read()
#    print ''
#    print f.registers.cd_hmc_hmc_delay_status1.read()
#    print ''
#    print f.registers.cd_hmc_hmc_delay_status2.read()
#    print ''
#    print f.registers.cd_hmc_hmc_delay_status3.read()
#    print ''
    
#    print "Sync80: %s" % f.registers.sync80_cnt.read()
#    print ''
#    print "HMC Out Sync count: %s" % f.registers.hmc_out_sync_cnt.read()
    print ''    
    print "DDC IN Sync count: %s" % f.registers.ddc_in_sync_cnt.read()
    print ''  
    
    
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

    adc1_0 = adc1['p0_d0']
    adc1_1 = adc1['p0_d1']
    adc1_2 = adc1['p0_d2']
    adc1_3 = adc1['p0_d3']
    adc1_4 = adc1['p0_d4']
    adc1_5 = adc1['p0_d5']
    adc1_6 = adc1['p0_d6']
    adc1_7 = adc1['p0_d7']
    adc1_sync = adc1['sync']
    adc1_dv = adc1['dv']

#    hmc_in_0 = hmc_in_ss['p0_d0']
#    hmc_in_1 = hmc_in_ss['p0_d1']
#    hmc_in_2 = hmc_in_ss['p0_d2']
#    hmc_in_3 = hmc_in_ss['p0_d3']
#    hmc_in_4 = hmc_in_ss['p0_d4']
#    hmc_in_5 = hmc_in_ss['p0_d5']
#    hmc_in_6 = hmc_in_ss['p0_d6']
#    hmc_in_7 = hmc_in_ss['p0_d7']
#    hmc_in_dv = hmc_in_ss['dv']
#    hmc_in_sync = hmc_in_ss['sync']
#    hmc_in_en = hmc_in_ss['en']
#
#    hmc_out_0 = hmc_out_ss['p0_d0']
#    hmc_out_1 = hmc_out_ss['p0_d1']
#    hmc_out_2 = hmc_out_ss['p0_d2']
#    hmc_out_3 = hmc_out_ss['p0_d3']
#    hmc_out_4 = hmc_out_ss['p0_d4']
#    hmc_out_5 = hmc_out_ss['p0_d5']
#    hmc_out_6 = hmc_out_ss['p0_d6']
#    hmc_out_7 = hmc_out_ss['p0_d7']
#    hmc_out_dv = hmc_out_ss['dv']
#    hmc_out_sync = hmc_out_ss['sync']
#    hmc_out_err = hmc_out_ss['err']

    
#    ddc_in_0 = ddc_in_ss['p0_d0']
#    ddc_in_1 = ddc_in_ss['p0_d1']
#    ddc_in_2 = ddc_in_ss['p0_d2']
#    ddc_in_3 = ddc_in_ss['p0_d3']
#    ddc_in_4 = ddc_in_ss['p0_d4']
#    ddc_in_5 = ddc_in_ss['p0_d5']
#    ddc_in_6 = ddc_in_ss['p0_d6']
#    ddc_in_7 = ddc_in_ss['p0_d7']
#    ddc_in_dv = ddc_in_ss['dv']
#    ddc_in_sync = ddc_in_ss['sync']
    
    fft_xil_real = fft_xil['real']
    fft_xil_imag = fft_xil['imag']
    fft_xil_complx = fft_xil_real + np.multiply(fft_xil_imag, 1j)
    fft_xil_sync = fft_xil['sync']
    fft_xil_dv = fft_xil['dv']
    
    fft_xil_real1 = fft_xil1['real']
    fft_xil_imag1 = fft_xil1['imag']
    fft_xil_complx1 = fft_xil_real1 + np.multiply(fft_xil_imag1, 1j)
    fft_xil_sync1 = fft_xil1['sync']
    fft_xil_dv1 = fft_xil1['dv']    
    
    nb_r0 = nb0_1['real0']
    nb_r1 = nb0_1['real1']
    nb_r2 = nb0_1['real2']
    nb_r3 = nb0_2['real3']
    nb_i0 = nb0_1['imag0']
    nb_i1 = nb0_1['imag1']
    nb_i2 = nb0_1['imag2']
    nb_i3 = nb0_2['imag3']
    
    
    
    init_phase = fd_gen_ss['init_phase']
    slope = fd_gen_ss['slope']
    idx = fd_gen_ss['idx']
    
    theta = lookup_ss['theta']
    cos = lookup_ss['cos']
    sin = lookup_ss['sin']
    

    q0_r0 = quant0_ss['real0']
    q0_i0 = quant0_ss['imag0']
    q0_r1 = quant0_ss['real1']
    q0_i1 = quant0_ss['imag1']
    q0_r2 = quant0_ss['real2']
    q0_i2 = quant0_ss['imag2']
    q0_r3 = quant0_ss['real3']
    q0_i3 = quant0_ss['imag3']

#    q1_r0 = quant1_ss['real0']
#    q1_i0 = quant1_ss['imag0']
#    q1_r1 = quant1_ss['real1']
#    q1_i1 = quant1_ss['imag1']
#    q1_r2 = quant1_ss['real2']
#    q1_i2 = quant1_ss['imag2']
#    q1_r3 = quant1_ss['real3']
#    q1_i3 = quant1_ss['imag3']
    
    # --------------------------------------------------------------------
    adc0_input = []
    adc1_input = []
    
    for x in range(0, len(adc0_0)):
        adc0_input.extend(
            [adc0_0[x], adc0_1[x], adc0_2[x], adc0_3[x], adc0_4[x], adc0_5[x], adc0_6[x], adc0_7[x]])

    for x in range(0, len(adc0_0)):
        adc1_input.extend(
            [adc1_0[x], adc1_1[x], adc1_2[x], adc1_3[x], adc1_4[x], adc1_5[x], adc1_6[x], adc1_7[x]])
 
    # --------------------------------------------------------------------
#    hmc_in = []
#    
#    for x in range(0, len(ddc_in_0)):
#        hmc_in.extend(
#            [hmc_in_0[x], hmc_in_1[x], hmc_in_2[x], hmc_in_3[x], hmc_in_4[x], hmc_in_5[x], hmc_in_6[x], hmc_in_7[x]])
#    
#    # --------------------------------------------------------------------
#    hmc_out = []
#    
#    for x in range(0, len(ddc_in_0)):
#        hmc_out.extend(
#            [hmc_out_0[x], hmc_out_1[x], hmc_out_2[x], hmc_out_3[x], hmc_out_4[x], hmc_out_5[x], hmc_out_6[x], hmc_out_7[x]])
#       
    # --------------------------------------------------------------------
#    ddc_in = []
#    
#    for x in range(0, len(ddc_in_0)):
#        ddc_in.extend(
#            [ddc_in_0[x], ddc_in_1[x], ddc_in_2[x], ddc_in_3[x], ddc_in_4[x], ddc_in_5[x], ddc_in_6[x], ddc_in_7[x]])

    # --------------------------------------------------------------------
    
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
    
    q0_real = []
    q0_imag = []
    
    for x in range(0, len(q0_r0)):
        q0_real.extend(
            [q0_r0[x], q0_r1[x], q0_r2[x], q0_r3[x]])
    
    for x in range(0, len(q0_i0)):
        q0_imag.extend(
            [q0_i0[x], q0_i1[x], q0_i2[x], q0_i3[x]])
    q0_complx_sq = q0_real + np.multiply(q0_imag, 1j)

    # --------------------------------------------------------------------

#    q1_real = []
#    q1_imag = []
#    
#    for x in range(0, len(q1_r0)):
#        q1_real.extend(
#            [q1_r0[x], q1_r1[x], q1_r2[x], q1_r3[x]])
#    
#    for x in range(0, len(q1_i0)):
#        q1_imag.extend(
#            [q1_i0[x], q1_i1[x], q1_i2[x], q1_i3[x]])
#    q1_complx_sq = q1_real + np.multiply(q1_imag, 1j)

    # --------------------------------------------------------------------


    
    print "Counters"
    print 'DDC Sync Count'
    print f.registers.ddc_sync_cnt.read()
    print 'NB Sync Count'
    print f.registers.nb_sync_cnt.read()
    
    # --------------------------------------------------------------------
    
#    plt.figure(1)
#    plt.clf()
#    plt.subplot(411)
#    plt.plot(adc0_input)
#    plt.subplot(412)
#    plt.plot(adc0_0)
#    plt.subplot(413)
#    plt.plot(adc_dv)
#    plt.plot(adc_sync)
#    plt.subplot(414)
#    fft_adc = np.fft.fft(adc0_input[5:5+8192])
#    plt.semilogy(np.abs(fft_adc))

    plt.figure(2)
    plt.clf()
    plt.subplot(411)
    plt.plot(adc1_input)
    plt.subplot(412)
    plt.plot(adc1_0)
    plt.subplot(413)
    plt.plot(adc1_dv)
    plt.plot(adc1_sync)
    plt.subplot(414)
    fft_adc1 = np.fft.fft(adc1_input[5:5+8192])
    plt.semilogy(np.abs(fft_adc1))

#    plt.figure(2)
#    plt.clf()
#    plt.plot(hmc_in)
#    plt.plot(hmc_in_dv)
#    plt.plot(hmc_in_sync)
#    plt.plot(hmc_in_en)    
#    
#           
#    plt.figure(3)
#    plt.clf()
#    plt.plot(hmc_out)
#    plt.plot(hmc_out_dv)
#    plt.plot(hmc_out_sync)
#    plt.plot(hmc_out_err)
    
#    plt.figure(4)
#    plt.clf()
#    plt.plot(ddc_in)
#    plt.plot(ddc_in_0)
#    plt.plot(ddc_in_dv)
        
#    plt.figure(5);
#    fft_ddc_in = np.fft.fft(ddc_in[5:5+8192])
#    plt.plot(np.abs(fft_ddc_in))
#    plt.semilogy(np.abs(fft_ddc_in))
    
#    plt.figure(10)
#    plt.clf()
#    plt.subplot(311)
#    plt.semilogy(np.abs(fft_xil_complx))
#    plt.subplot(312)
#    plt.semilogy(np.abs(fft_xil_complx1))
#    plt.subplot(313)
#    plt.plot(np.multiply(fft_xil_dv,0.1))
#    plt.plot(np.multiply(fft_xil_sync,0.5))
    
    plt.figure(11)    
    plt.subplot(211)
    plt.semilogy(np.abs(nb_complx_sq))
    plt.subplot(212)
    plt.semilogy(np.abs(q0_complx_sq))
#    plt.subplot(313)
#    plt.semilogy(np.abs(q1_complx_sq))
    
#    plt.figure(13)
#    plt.subplot(311)
#    plt.plot(init_phase)
#    plt.subplot(312)
#    plt.plot(slope)
#    plt.subplot(313)
#    plt.plot(idx)
#
#    plt.figure(14)
#    plt.subplot(311)
#    plt.plot(theta)
#    plt.subplot(312)
#    plt.plot(cos)
#    plt.subplot(313)
#    plt.plot(sin)
    
        
    plt.show()

