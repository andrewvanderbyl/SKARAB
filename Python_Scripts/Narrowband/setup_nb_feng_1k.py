import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

hosts = ['skarab020303-01','skarab020308-01','skarab02030A-01','skarab02030E-01']

for x in hosts:
    print x

    f = casperfpga.CasperFpga(x)

    #f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m1k_new_2019-05-07_0706.fpg')
    #f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m1k_new_2019-05-09_0658.fpg')
    #f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m1k_new_2019-05-10_2331.fpg')
    
    #f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m1k_new_2019-05-13_1334.fpg')
    #f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m1k_2019-05-20_0818.fpg')
    
    #f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m1k_2019-05-21_1032.fpg')
    f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m1k_2019-05-24_1055.fpg')
    
    
    
    # Select CD Bypass
    #-----------------
    f.registers.control.write(cd_bypass=0)
   
    # Setup mixer oscillator
    #-----------------------
    mix_freq = ((53500000)*np.power(2,22))/1712e6
    f.registers.scale_cwg_osc.write(scale=0.9)
    f.registers.freq_cwg_osc.write(frequency=mix_freq)
    
    # TVG Control
    #------------
    f.registers.osc_sel.write(sel=0) #0 = Osc; 1 = input TVG
    
    # Set scale_p0_ddc0 and scale_p1_ddc0
    #------------------------------------
    f.registers.scale_p0_ddc0.write(scale=0.9)
    f.registers.scale_p1_ddc0.write(scale=0.9)
    
    # Setup FFT
    f.registers.fft_fwd_inv.write(fwd_inv=1)
    f.registers.fft_shift.write(fft_shift=511)
    
    f.registers.nb_pfb_conf_tvalid.write(tvalid=0)    
    f.registers.nb_pfb_tvalid_sel.write(sel=0)

    f.registers.nb_pfb_data_tready.write(rdy=1)
    f.registers.nb_pfb_tready_sel.write(sel=0)

    f.registers.nb_pfb_data_tlast.write(rdy=0)
    f.registers.nb_pfb_tlast_sel.write(sel=0)
	
    #f.registers.time_sel.write(sel=0)

    if x == 'skarab020303-01':  
        print "Setting Delays"
        print x
        f.registers.delay_whole0.write(initial=0)
        f.registers.delay_frac0.write(initial=0.0)
        f.registers.delta_delay_whole0.write(initial=0.0)
        f.registers.delta_delay_frac0.write(initial=0.0)
        f.registers.phase0.write(initial=0.0)
        f.registers.phase0.write(delta=0.0)
        
        print f.registers.delay_whole0.read()
        print f.registers.delay_frac0.read()
        print f.registers.delta_delay_whole0.read()
        print f.registers.delta_delay_frac0.read()
        print f.registers.phase0.read()
        print f.registers.phase0.read()        
    else:
        print "Setting Delays"
        print x
        f.registers.delay_whole0.write(initial=0)
        f.registers.delay_frac0.write(initial=0.0)
        f.registers.delta_delay_whole0.write(initial=0.0)
        f.registers.delta_delay_frac0.write(initial=0.0)
        f.registers.phase0.write(initial=0.0)
        f.registers.phase0.write(delta=0.0)
        
        print f.registers.delay_whole0.read()
        print f.registers.delay_frac0.read()
        print f.registers.delta_delay_whole0.read()
        print f.registers.delta_delay_frac0.read()
        print f.registers.phase0.read()
        print f.registers.phase0.read()   


    print 'Arming Snapshots'    
    #f.snapshots.snap_adc0_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.snap_adc2_ss.arm(man_trig=True, man_valid=True)
    #f.snapshots.ss_osc_ss.arm(man_trig=False, man_valid=False)   

    f.snapshots.DDC_snap_mix_ss.arm(man_trig=False, man_valid=False)   
    #f.snapshots.DDC_mix_in_p0_ss.arm(man_trig=False, man_valid=False)    
    #f.snapshots.DDC_mix_in_osc_ss.arm(man_trig=False, man_valid=False)    
        
    #f.snapshots.nb_pfb_ss_fir_in_ss.arm(man_trig=False, man_valid=False)
    #f.snapshots.nb_pfb_ss_fir_out_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.nb_pfb_ss_fir_out1_ss.arm(man_trig=False, man_valid=False)
    
    f.snapshots.nb_pfb_ss_fft2_ss.arm(man_trig=False, man_valid=False)

    f.snapshots.nb_pfb_ss_nb_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.nb_pfb_ss_nb1_ss.arm(man_trig=False, man_valid=False)
    
    f.snapshots.phase_compensation0_delay_gen_ss_inputs_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.phase_compensation0_delay_gen_delay_gen_delay_calc_calc_ss.arm(man_trig=True, man_valid=True)
    f.snapshots.phase_compensation0_delay_gen_delay_gen_delay_calc_calc1_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.phase_compensation0_fd_fs_ss_fd_fs_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.phase_compensation0_fd_fs_ss_fd_fs1_ss.arm(man_trig=False, man_valid=False)
    
    #f.snapshots.snap_tg_ss.arm(man_trig=False, man_valid=False)
#    f.snapshots.ss_tg_cd_ss.arm(man_trig=False, man_valid=False)
#    f.snapshots.ss_tg_pfb_ss.arm(man_trig=False, man_valid=False)
#    f.snapshots.ss_tg_ct_ss.arm(man_trig=False, man_valid=False)

    f.snapshots.snap_quant0_ss.arm(man_trig=False, man_valid=False)

    print 'Setting up ss time trig'
    f.registers.arm_ss_ts_rst.write(en='pulse')
    f.registers.ts_ss_lock.write(en=0)
    f.registers.arm_ts_ss_lock.write(en='pulse')
    f.registers.ss_trig_time_add.write(time=((1712e6/2048)*5*1))
       
    

    print 'Arming Done' 
    f.registers.tl_cd0_control0.write(arm='pulse')    
    f.registers.tl_cd0_control0.write(load_immediate='pulse')    
    f.registers.control.write(cnt_rst='pulse')
    f.registers.control.write(sys_rst='pulse')


    if x == 'skarab020303-01': 
   
        print 'FDFS offset values'
        print f.registers.dds_fft_bin.read()
        print f.registers.dds_fft_phase_offset.read()
                
        # Grab ADC data and Quant data as a sanity check    
        #-----------------------------------------------
        #adc0 = f.snapshots.snap_adc0_ss.read(arm=False)['data']
        adc2 = f.snapshots.snap_adc2_ss.read(arm=False)['data']
        #osc_ss = f.snapshots.ss_osc_ss.read(arm=False)['data']
        
        ddc_snap_mix = f.snapshots.DDC_snap_mix_ss.read(arm=False)['data']
        #ddc_mix_p0 = f.snapshots.DDC_mix_in_p0_ss.read(arm=False)['data']
        #ddc_mix_osc = f.snapshots.DDC_mix_in_osc_ss.read(arm=False)['data']
        
        #fir_in = f.snapshots.nb_pfb_ss_fir_in_ss.read(arm=False)['data']
        #fir_out = f.snapshots.nb_pfb_ss_fir_out_ss.read(arm=False)['data']
        fir_out1 = f.snapshots.nb_pfb_ss_fir_out1_ss.read(arm=False)['data']
        
        fft2 = f.snapshots.nb_pfb_ss_fft2_ss.read(arm=False)['data']
        
        nb_fft = f.snapshots.nb_pfb_ss_nb_ss.read(arm=False)['data']
        nb_fft1 = f.snapshots.nb_pfb_ss_nb1_ss.read(arm=False)['data']
        
        inputs = f.snapshots.phase_compensation0_delay_gen_ss_inputs_ss.read(arm=False)['data']
        delay_calc = f.snapshots.phase_compensation0_delay_gen_delay_gen_delay_calc_calc_ss.read(arm=False)['data']
        delay_coeff = f.snapshots.phase_compensation0_delay_gen_delay_gen_delay_calc_calc1_ss.read(arm=False)['data']
        fd_fs = f.snapshots.phase_compensation0_fd_fs_ss_fd_fs_ss.read(arm=False)['data']
        fd_fs1 = f.snapshots.phase_compensation0_fd_fs_ss_fd_fs1_ss.read(arm=False)['data']
        
        quant0_ss = f.snapshots.snap_quant0_ss.read(arm=False)['data']
         
        
        # ****  ADC  ****
        #adc0_0 = adc0['p0_d0']
        #adc0_1 = adc0['p0_d1']
        #adc0_2 = adc0['p0_d2']
        #adc0_3 = adc0['p0_d3']
        #adc0_4 = adc0['p0_d4']
        #adc0_5 = adc0['p0_d5']
        #adc0_6 = adc0['p0_d6']
        #adc0_7 = adc0['p0_d7']
        #adc_sync = adc0['sync']
        #adc_dv = adc0['dv']    
        
        adc2_0 = adc2['p0_d0']
        adc2_1 = adc2['p0_d1']
        adc2_2 = adc2['p0_d2']
        adc2_3 = adc2['p0_d3']
        adc2_4 = adc2['p0_d4']
        adc2_5 = adc2['p0_d5']
        adc2_6 = adc2['p0_d6']
        adc2_7 = adc2['p0_d7']
        adc2_sync = adc2['sync']
        adc2_dv = adc2['dv']  
        adc2_trig = adc2['trig']
        adc2_trig_time = adc2['trig_time']

        print 'ADC trig time'  
        print adc2_trig[0:10]
        print adc2_trig_time[0:10]
        print 'curr_time_adc' 
        print f.registers.ss_time_trig_cap_curr_time_adc.read()
        print 'cap_time_adc' 
        print f.registers.ss_time_trig_cap_time_adc.read()
        print 'time_sum_adc' 
        print f.registers.ss_time_trig_cap_time_sum_adc.read()
        
                
        #osc_0 = osc_ss['p0_d0']
        #osc_1 = osc_ss['p0_d1']
        #osc_2 = osc_ss['p0_d2']
        #osc_3 = osc_ss['p0_d3']
        #osc_4 = osc_ss['p0_d4']
        #osc_5 = osc_ss['p0_d5']
        #osc_6 = osc_ss['p0_d6']
        #osc_7 = osc_ss['p0_d7']
        #pfbin_sync = osc_ss['sync_in']
        #pfbin_dv = osc_ss['dv_in']  
        #ddc_sync = osc_ss['sync']
        #ddc_dv_in = osc_ss['dv']  
        
        #mix_p0_0 = ddc_mix_p0['p0_d0']
        #mix_p0_1 = ddc_mix_p0['p0_d1']
        #mix_p0_2 = ddc_mix_p0['p0_d2']
        #mix_p0_3 = ddc_mix_p0['p0_d3']
        #mix_p0_4 = ddc_mix_p0['p0_d4']
        #mix_p0_5 = ddc_mix_p0['p0_d5']
        #mix_p0_6 = ddc_mix_p0['p0_d6']
        #mix_p0_7 = ddc_mix_p0['p0_d7']
        #mix_p0_sync = ddc_mix_p0['sync']
        #mix_p0_dv = ddc_mix_p0['dv'] 
        #
        #mix_osc_0 = ddc_mix_osc['p0_d0']
        #mix_osc_1 = ddc_mix_osc['p0_d1']
        #mix_osc_2 = ddc_mix_osc['p0_d2']
        #mix_osc_3 = ddc_mix_osc['p0_d3']
        #mix_osc_4 = ddc_mix_osc['p0_d4']
        #mix_osc_5 = ddc_mix_osc['p0_d5']
        #mix_osc_6 = ddc_mix_osc['p0_d6']
        #mix_osc_7 = ddc_mix_osc['p0_d7']
        #mix_osc_sync = ddc_mix_osc['sync']
        #mix_osc_dv = ddc_mix_osc['dv'] 
        
        
        #------------------------------------------------------------------------------
        #adc0_input = []
        #    
        #for x in range(0, len(adc0_0)):
        #    adc0_input.extend(
        #        [adc0_0[x], adc0_1[x], adc0_2[x], adc0_3[x], adc0_4[x], adc0_5[x], adc0_6[x], adc0_7[x]])
        #------------------------------------------------------------------------------
        adc2_input = []
            
        for x in range(0, len(adc2_0)):
            adc2_input.extend(
                [adc2_0[x], adc2_1[x], adc2_2[x], adc2_3[x], adc2_4[x], adc2_5[x], adc2_6[x], adc2_7[x]])
        
        #------------------------------------------------------------------------------
        #osc_input = []
        #    
        #for x in range(0, len(osc_0)):
        #    osc_input.extend(
        #        [osc_0[x], osc_1[x], osc_2[x], osc_3[x], osc_4[x], osc_5[x], osc_6[x], osc_7[x]])
        
        #------------------------------------------------------------------------------
        #mix_p0_input = []
        #    
        #for x in range(0, len(mix_p0_0)):
        #    mix_p0_input.extend(
        #        [mix_p0_0[x], mix_p0_1[x], mix_p0_2[x], mix_p0_3[x], mix_p0_4[x], mix_p0_5[x], mix_p0_6[x], mix_p0_7[x]])
        #
        ##------------------------------------------------------------------------------osc_input = []
        #mix_osc_input = [] 
        #
        #for x in range(0, len(mix_osc_0)):
        #    mix_osc_input.extend(
        #        [mix_osc_0[x], mix_osc_1[x], mix_osc_2[x], mix_osc_3[x], mix_osc_4[x], mix_osc_5[x], mix_osc_6[x], mix_osc_7[x]])
        
        #------------------------------------------------------------------------------
        
        # ****  MIXER  ****
        mix0_0 = ddc_snap_mix['p0_d0']
        mix0_1 = ddc_snap_mix['p0_d1']
        mix0_2 = ddc_snap_mix['p0_d2']
        mix0_3 = ddc_snap_mix['p0_d3']
        mix0_4 = ddc_snap_mix['p0_d4']
        mix0_5 = ddc_snap_mix['p0_d5']
        mix0_6 = ddc_snap_mix['p0_d6']
        mix0_7 = ddc_snap_mix['p0_d7']
        mix_sync = ddc_snap_mix['sync']
        mix_dv = ddc_snap_mix['dv'] 
        
        mix = []
            
        for x in range(0, len(mix0_0)):
            mix.extend(
                [mix0_0[x], mix0_1[x], mix0_2[x], mix0_3[x], mix0_4[x], mix0_5[x], mix0_6[x], mix0_7[x]])
        
        #------------------------------------------------------------------------------
        
        
        # ****  FIR  ****
        #fir_in_data = fir_in['fir']
        #fir_in_sync = fir_in['sync']
        #fir_in_dv = fir_in['dv'] 
        
        #fir_out_data = fir_out['fir']
        #fir_out_sync = fir_out['sync']
        #fir_out_dv = fir_out['dv'] 
        
        fir_out1_data = fir_out1['fir']
        fir_out1_sync = fir_out1['sync']
        fir_out1_dv = fir_out1['dv'] 
        fir_out1_conf = fir_out1['conf_tvalid'] 
        fir_out1_tlast = fir_out1['tlast'] 
        
        
        # FFT: 2
        fft_ch2 = fft2['fft_ch']
        fft_re2 = fft2['fft_re']
        fft_im2 = fft2['fft_im']
        fft_dv2 = fft2['fft_dv']
        fft_fs2 = fft2['fft_fs']
        fft_tl2 = fft2['fft_tl']
        fft_sync2 = fft2['fft_sync']
        fft_of2 = fft2['fft_of']
        fft_tready2 = fft2['fft_tready']
        fft_tlast_miss2 = fft2['tlast_miss']
        fft_tlast_unexp2 = fft2['tlast_unexp']
        fir_sync2 = fft2['fir_sync']
        fft_trig = fft2['trig']
        fft_trig_time = fft2['trig_time']
        
        print 'fir trig time'    
        print fft_trig[0:10]
        print fft_trig_time[0:10]
        print 'curr_time_fft' 
        print f.registers.nb_pfb_ss_time_trig_cap_curr_time_fft.read()
        print 'cap_time_fft' 
        print f.registers.nb_pfb_ss_time_trig_cap_time_fft.read()
        print 'time_sum_fft' 
        print f.registers.nb_pfb_ss_time_trig_cap_time_sum_fft.read()
        
        ## NB FFT: 0
        nb_r0 = nb_fft['r0']
        nb_i0 = nb_fft['i0']
        nb_r1 = nb_fft['r1']
        nb_i1 = nb_fft['i1']
        nb_r2 = nb_fft1['r2']
        nb_i2 = nb_fft1['i2']
        nb_r3 = nb_fft1['r3']
        nb_i3 = nb_fft1['i3']
        nb_sync = nb_fft['sync']
        nb_dv = nb_fft['dv']  
        nb_fft_sync_cnt = nb_fft['sync_cnt']
        nb_fft_new_spec = nb_fft['new_spec']
        
        nb_real = []
        nb_imag = []
            
        for x in range(0, len(nb_r0)):
            nb_real.extend(
                [nb_r0[x], nb_r1[x], nb_r2[x], nb_r3[x]])
            
        for x in range(0, len(nb_i0)):
            nb_imag.extend(
                [nb_i0[x], nb_i1[x], nb_i2[x], nb_i3[x]])
        nb_complx_sq = nb_real + np.multiply(nb_imag, 1j)
            
            
        # ****  input  ****
        input_sync = inputs['sync']
        input_init = inputs['init']
        input_idx = inputs['idx']
        input_en = inputs['en']
        input_load = inputs['load']
        input_phase = inputs['phase']
        input_dt_phase = inputs['dt_phase']
        input_delay = inputs['delay']
        
        # ****  delay calc  ****
        delay_calc_sel = delay_calc['sel']
        delay_calc_val = delay_calc['val']
        delay_calc_update = delay_calc['update']
        delay_calc_val_inc = delay_calc['val_inc']
        
        # ****  delay coeff  ****
        delay_coeff_en = delay_coeff['en_o']
        delay_coeff_coeff = delay_coeff['coeff']
        
        # ****  fd_fs  ****
        fd_fs_sync = fd_fs['sync']
        fd_fs_x = fd_fs['x']
        fd_fs_a0 = fd_fs['a0']
        fd_fs_a1 = fd_fs['a1']
        fd_fs_cos = fd_fs['cos']

        # ****  fd_fs1  ****
        fd_fs_cos1 = fd_fs1['cos']
        fd_fs_sin1 = fd_fs1['sin']
        b_real = fd_fs1['b_real']
        b_imag = fd_fs1['b_imag']
        out_real = fd_fs1['out_real']
        out_imag = fd_fs1['out_imag']
        
        # ****  QUANT  ****
        q0_r0 = quant0_ss['real0']
        q0_i0 = quant0_ss['imag0']
        q0_r1 = quant0_ss['real1']
        q0_i1 = quant0_ss['imag1']
        q0_r2 = quant0_ss['real2']
        q0_i2 = quant0_ss['imag2']
        q0_r3 = quant0_ss['real3']
        q0_i3 = quant0_ss['imag3']
        q0_trig = quant0_ss['trig']
        q0_trig_time = quant0_ss['trig_time']
        
        print 'Qaunt trig time'  
        print q0_trig[0:10]
        print q0_trig_time[0:10]        
        print 'curr_time_quant' 
        print f.registers.ss_time_trig1_cap_curr_time_quant.read()
        print 'cap_time_quant' 
        print f.registers.ss_time_trig1_cap_time_quant.read()
        print 'time_sum_quant' 
        print f.registers.ss_time_trig1_cap_time_sum_quant.read()
           
        q0_real = []
        q0_imag = []
            
        for x in range(0, len(q0_r0)):
            q0_real.extend(
                [q0_r0[x], q0_r1[x], q0_r2[x], q0_r3[x]])
            
        for x in range(0, len(q0_i0)):
            q0_imag.extend(
                [q0_i0[x], q0_i1[x], q0_i2[x], q0_i3[x]])
        q0_complx_sq = q0_real + np.multiply(q0_imag, 1j)
        
        #------------------------------------------------------------------------------
        #                           Figures
        #------------------------------------------------------------------------------
            
        #plt.figure(1)
        #plt.clf()
        #plt.subplot(411)
        #plt.plot(adc0_input)
        #plt.subplot(412)
        #plt.plot(adc0_0)
        #plt.subplot(413)
        #plt.plot(adc_dv)
        #plt.plot(adc_sync)
        #plt.subplot(414)
        #fft_adc = np.fft.fft(adc0_input[5:5+8192])
        #plt.semilogy(np.abs(fft_adc))
           
        #plt.figure(2)
        #plt.clf()
        #plt.subplot(411)
        #plt.plot(adc2_input)
        #plt.subplot(412)
        #plt.plot(adc2_0)
        #plt.subplot(413)
        #plt.plot(adc2_dv)
        #plt.plot(adc2_sync)
        #plt.subplot(414)
        #fft_adc = np.fft.fft(adc2_input[5:5+8192])
        #plt.semilogy(np.abs(fft_adc))    
        
        #plt.figure(3)
        #plt.clf()
        #plt.subplot(511)
        #plt.plot(osc_input)
        #plt.subplot(512)
        #plt.plot(osc_0)
        #plt.subplot(513)
        #plt.plot(ddc_dv_in)
        #plt.plot(ddc_sync)
        #plt.subplot(514)
        #plt.plot(pfbin_dv)
        #plt.plot(pfbin_sync)
        #plt.subplot(515)
        #fft_osc = np.fft.fft(osc_input[462:462+8192])
        #plt.semilogy(np.abs(fft_osc))
        
        #plt.figure(4)
        #plt.clf()
        #plt.subplot(411)
        #plt.plot(mix_p0_input)
        #plt.subplot(412)
        #plt.plot(mix_p0_0)
        #plt.subplot(413)
        #plt.plot(mix_p0_dv)
        #plt.plot(mix_p0_sync)
        #plt.subplot(414)
        #fft_mix_p0_input = np.fft.fft(mix_p0_input[0:0+8192])
        #plt.semilogy(np.abs(fft_mix_p0_input))
        
        #plt.figure(5)
        #plt.clf()
        #plt.subplot(411)
        #plt.plot(mix_osc_input)
        #plt.plot(mix_p0_input)
        #plt.subplot(412)
        #plt.plot(mix_osc_0)
        #plt.plot(mix_p0_0)
        #plt.subplot(413)
        #plt.plot(mix_osc_dv)
        #plt.plot(mix_p0_dv)
        #plt.plot(mix_osc_sync)
        #plt.plot(mix_p0_sync)
        #plt.subplot(414)
        #fft_mix_osc_input = np.fft.fft(mix_osc_input[0:0+8192])
        #plt.semilogy(np.abs(fft_mix_osc_input))
        
        #plt.figure(6)
        #plt.clf()
        #plt.subplot(311)
        #plt.plot(mix)
        #plt.subplot(312)
        #plt.plot(mix_dv)
        #plt.plot(mix_sync)
        #plt.subplot(313)
        #fft_mix = np.fft.fft(mix[0:0+2047])
        #plt.semilogy(np.abs(fft_mix))
        
        #plt.figure(7)
        #plt.clf()    
        #plt.subplot(511)
        #plt.plot(fir_in_data)
        #plt.subplot(512)
        #plt.plot(fir_in_sync)
        #plt.plot(fir_in_dv)
        #plt.subplot(513)
        #plt.plot(fir_out_data)
        #plt.subplot(514)
        #plt.plot(fir_out_sync)
        #plt.plot(fir_out_dv)
        #plt.subplot(515)
        #fft_fir_out_data = np.fft.fft(fir_out_data[0:0+2047])
        #plt.semilogy(np.abs(fft_fir_out_data))
        
        #plt.figure(8)
        #plt.clf()   
        #plt.subplot(411)
        #plt.plot(fir_out1_data)
        #plt.subplot(412)
        #plt.plot(fir_out1_sync)
        #plt.plot(fir_out1_dv)
        #plt.subplot(413)
        #plt.plot(fir_out1_conf)
        #plt.plot(fir_out1_tlast)
        #plt.subplot(414)
        #fft_fir_out1_data = np.fft.fft(fir_out1_data[0:0+2047])
        #plt.semilogy(np.abs(fft_fir_out1_data))
        
#        plt.figure(9)
#        plt.clf()
#        plt.subplot(611)
#        plt.semilogy(np.square(np.abs(fft_re2)))
#        plt.subplot(612)
#        plt.plot(fft_sync2)
#        plt.plot(fft_dv2)
#        plt.subplot(613)
#        plt.plot(fft_ch2)
#        plt.subplot(614)
#        plt.plot(fft_fs2)
#        plt.plot(fft_tl2)
#        plt.subplot(615)
#        plt.plot(fft_of2)
#        plt.plot(fft_tready2)
#        plt.subplot(616)
#        plt.plot(fft_tlast_miss2)
#        plt.plot(fft_tlast_unexp2)
        
            
#        plt.figure(10)
#        plt.clf()
#        plt.subplot(811)
#        plt.plot(input_sync)
#        plt.subplot(812)
#        plt.plot(input_init)
#        plt.subplot(813)
#        plt.plot(input_idx)
#        plt.subplot(814)
#        plt.plot(input_en)
#        plt.subplot(815)
#        plt.plot(input_load)
#        plt.subplot(816)
#        plt.plot(input_phase)
#        plt.subplot(817)
#        plt.plot(input_dt_phase)
#        plt.subplot(818)
#        plt.plot(input_delay)
#        
#        plt.figure(11)
#        plt.clf()    
#        plt.subplot(411)
#        plt.plot(delay_calc_sel)
#        plt.subplot(412)
#        plt.plot(delay_calc_val)
#        plt.subplot(413)
#        plt.plot(delay_calc_update)
#        plt.subplot(414)
#        plt.plot(delay_calc_val_inc)
#        
#        plt.figure(12)
#        plt.clf()    
#        plt.subplot(211)
#        plt.plot(delay_calc_sel)
#        plt.subplot(212)
#        plt.plot(delay_coeff_coeff)
#        
#        plt.figure(13)
#        plt.clf()    
#        plt.subplot(511)
#        plt.plot(fd_fs_sync)
#        plt.subplot(512)
#        plt.plot(fd_fs_x)
#        plt.subplot(513)
#        plt.plot(fd_fs_a0)
#        plt.subplot(514)
#        plt.plot(fd_fs_a1)
#        plt.subplot(515)
#        plt.plot(fd_fs_cos)
        
        
#        plt.figure(14)
#        plt.clf()    
#        plt.subplot(611)
#        plt.plot(fd_fs_cos1)
#        plt.subplot(612)
#        plt.plot(fd_fs_sin1)
#        plt.subplot(613)
#        plt.plot(b_real)
#        plt.subplot(614)
#        plt.plot(b_imag)
#        plt.subplot(615)
#        plt.plot(out_real)
#        plt.subplot(616)
#        plt.plot(out_imag)        
#       
#        
#        plt.figure(15)
#        plt.clf()    
#        plt.subplot(311)
#        plt.semilogy(np.square(np.abs(nb_complx_sq)))
#        plt.subplot(312)
#        plt.plot(np.abs(q0_r0))
#        #plt.plot(nb_fft_new_spec)
#        plt.subplot(313)
#        plt.plot(nb_dv)
#        plt.plot(nb_sync)
        #
        #plt.figure(15)
        #plt.clf()    
        #plt.subplot(211)
        #plt.semilogy(np.square(np.abs(q0_complx_sq)))
        #plt.subplot(212)
        #plt.plot(np.abs(q0_complx_sq))
        
        plt.show()    
            
