import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

hosts = ['skarab020303-01','skarab020308-01','skarab02030A-01','skarab02030E-01']
highest_time_msw = 0
highest_time_lsw = 0

filename = '/home/avanderbyl/fpgs/s_c_nbe_m1k_2019-05-28_1411.fpg'

class skarab_debug:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'

    def get_fft_offset(self, f):

        
        print 'FDFS offset values for', f.host
        print f.registers.dds_fft_bin.read()
        print f.registers.dds_fft_phase_offset.read()

class all_skarab_debug: 
    def get_adc_SS_data_compare (self, f0,f1,f2,f3):
        
        adc0 = f0.snapshots.snap_adc2_ss.read(arm=False)['data']
        adc1 = f1.snapshots.snap_adc2_ss.read(arm=False)['data']
        adc2 = f2.snapshots.snap_adc2_ss.read(arm=False)['data']
        adc3 = f3.snapshots.snap_adc2_ss.read(arm=False)['data']

        print 'Host:', f0.host               
        [adc0_in, adc0_0, adc0_sync, adc0_dv] = self.unpack_adc(adc0)
        print 'Host:', f1.host     
        [adc1_in, adc1_0, adc1_sync, adc1_dv] = self.unpack_adc(adc1)
        print 'Host:', f2.host     
        [adc2_in, adc2_0, adc2_sync, adc2_dv] = self.unpack_adc(adc2)
        print 'Host:', f3.host     
        [adc3_in, adc3_0, adc3_sync, adc3_dv] = self.unpack_adc(adc3)
        
        adc_sync = [adc0_sync, adc1_sync, adc2_sync, adc3_sync]
        adc_dv = [adc0_dv, adc1_dv, adc2_dv, adc3_dv]
                
        self.plot_adc_compare(adc0_in, adc0_0, adc1_in, adc1_0, adc2_in, adc2_0, adc3_in, adc3_0, adc_sync, adc_dv)
        
        
    def get_fft_SS_data_compare (self, f0,f1,f2,f3):
        fft0 = f0.snapshots.nb_pfb_ss_fft2_ss.read(arm=False)['data'] 
        fft1 = f0.snapshots.nb_pfb_ss_fft2_ss.read(arm=False)['data'] 
        fft2 = f0.snapshots.nb_pfb_ss_fft2_ss.read(arm=False)['data'] 
        fft3 = f0.snapshots.nb_pfb_ss_fft2_ss.read(arm=False)['data'] 
        
        [re0, im0, ch0, fft0_sync, fft0_dv, fir0_sync] = self.unpack_fft(fft0)
        [re1, im1, ch1, fft1_sync, fft1_dv, fir1_sync] = self.unpack_fft(fft1)
        [re2, im2, ch2, fft2_sync, fft2_dv, fir2_sync] = self.unpack_fft(fft2)
        [re3, im3, ch3, fft3_sync, fft3_dv, fir3_sync] = self.unpack_fft(fft3)
        
        real = [re0, re1, re2, re3]
        imag = [im0, im1, im2, im3]
        chan = [ch0, ch1, ch2, ch3]
        fft_sync = [fft0_sync, fft1_sync, fft2_sync, fft3_sync]
        fft_dv = [fft0_dv, fft1_dv, fft2_dv, fft3_dv]
        fir_sync = [fir0_sync, fir1_sync, fir2_sync, fir3_sync]     
        
        self.plot_fft_compare(real, imag, chan, fft_sync, fft_dv, fir_sync)


    def get_nb_sync_SS_data_compare (self, f0,f1,f2,f3):
        nb0_sync = f0.snapshots.nb_pfb_ss_nb_sync_ss.read(arm=False)['data']
        nb1_sync = f1.snapshots.nb_pfb_ss_nb_sync_ss.read(arm=False)['data']
        nb2_sync = f2.snapshots.nb_pfb_ss_nb_sync_ss.read(arm=False)['data']
        nb3_sync = f3.snapshots.nb_pfb_ss_nb_sync_ss.read(arm=False)['data']
        
        [nb0_re, nb0_im, nb0_sync_sync, nb0_sync_dv, nb0_sync_ch, nb0_sync_cnt] = self.unpack_nb_sync(nb0_sync)
        [nb1_re, nb1_im, nb1_sync_sync, nb1_sync_dv, nb1_sync_ch, nb1_sync_cnt] = self.unpack_nb_sync(nb1_sync)
        [nb2_re, nb2_im, nb2_sync_sync, nb2_sync_dv, nb2_sync_ch, nb2_sync_cnt] = self.unpack_nb_sync(nb2_sync)
        [nb3_re, nb3_im, nb3_sync_sync, nb3_sync_dv, nb3_sync_ch, nb3_sync_cnt] = self.unpack_nb_sync(nb3_sync)

        nb_sync_re = [nb0_re, nb1_re, nb2_re, nb3_re]
        nb_sync_im = [nb0_im, nb1_im, nb2_im, nb3_im]
        
        nb_sync_sync = [nb0_sync_sync, nb1_sync_sync, nb2_sync_sync, nb3_sync_sync]
        nb_sync_dv = [nb0_sync_dv, nb1_sync_dv, nb2_sync_dv, nb3_sync_dv]
        nb_sync_ch = [nb0_sync_ch, nb1_sync_ch, nb2_sync_ch, nb3_sync_ch]
        nb_sync_cnt = [nb0_sync_cnt, nb1_sync_cnt, nb2_sync_cnt, nb3_sync_cnt]
                        
        self.plot_nb_sync_compare(nb_sync_re, nb_sync_im, nb_sync_sync, nb_sync_dv, nb_sync_ch, nb_sync_cnt)
        
    def get_quant_SS_data_compare (self, f0,f1,f2,f3):
        q0 = f0.snapshots.snap_quant0_ss.read(arm=False)['data']
        q1 = f1.snapshots.snap_quant0_ss.read(arm=False)['data']
        q2 = f2.snapshots.snap_quant0_ss.read(arm=False)['data']
        q3 = f3.snapshots.snap_quant0_ss.read(arm=False)['data']
        
        [q_re0, q_im0] = self.unpack_quant(q0)
        [q_re1, q_im1] = self.unpack_quant(q1)
        [q_re2, q_im2] = self.unpack_quant(q2)
        [q_re3, q_im3] = self.unpack_quant(q3)
        
        real = [q_re0, q_re1, q_re2, q_re3]
        imag = [q_im0, q_im1, q_im2, q_im3]
        
        self.plot_quant_compare(real, imag)

    def unpack_adc(self, adc):
        # ADC
        adc_0 = adc['p0_d0']
        adc_1 = adc['p0_d1']
        adc_2 = adc['p0_d2']
        adc_3 = adc['p0_d3']
        adc_4 = adc['p0_d4']
        adc_5 = adc['p0_d5']
        adc_6 = adc['p0_d6']
        adc_7 = adc['p0_d7']
        adc_sync = adc['sync']
        adc_dv = adc['dv']  
        adc_trig = adc['trig']
        adc_trig_time = adc['trig_time']

        print 'ADC trig time'  
        print adc_trig[0:10]
        print adc_trig_time[0:10]
        print 'curr_time_adc_msw:', f.registers.ss_time_trig_cap_curr_time_adc_msw.read()
        print 'curr_time_adc_lsw:', f.registers.ss_time_trig_cap_curr_time_adc_lsw.read()
        print 'cap_time_adc_msw:', f.registers.ss_time_trig_cap_time_adc_msw.read()
        print 'cap_time_adc_lsw:', f.registers.ss_time_trig_cap_time_adc_lsw.read()
        print 'time_sum_adc:', f.registers.ss_time_trig_cap_trig_adc.read()
        
        adc_input = []
            
        for x in range(0, len(adc_0)):
            adc_input.extend(
                    [adc_0[x], adc_1[x], adc_2[x], adc_3[x], adc_4[x], adc_5[x], adc_6[x], adc_7[x]])
        
        return (adc_input, adc_0, adc_sync, adc_dv)    

    def unpack_fft(self, fft):

        fft_ch = fft['fft_ch']
        fft_re = fft['fft_re']
        fft_im = fft['fft_im']
        fft_dv = fft['fft_dv']
        fft_fs = fft['fft_fs']
        fft_tl = fft['fft_tl']
        fft_sync = fft['fft_sync']
        fft_of = fft['fft_of']
        fft_tready = fft['fft_tready']
        fft_tlast_miss = fft['tlast_miss']
        fft_tlast_unexp = fft['tlast_unexp']
        fir_sync = fft['fir_sync']
        fft_trig = fft['trig']
        fft_trig_time = fft['trig_time']
        
        print 'fir trig time'    
        print fft_trig[0:10]
        print fft_trig_time[0:10]
        
        print 'curr_time_fft_msw:', f.registers.nb_pfb_ss_time_trig_cap_curr_time_fft_msw.read()
        print 'curr_time_fft_lsw:', f.registers.nb_pfb_ss_time_trig_cap_curr_time_fft_lsw.read()

        print 'cap_time_fft_msw:',  f.registers.nb_pfb_ss_time_trig_cap_time_fft_msw.read()
        print 'cap_time_fft_lsw:', f.registers.nb_pfb_ss_time_trig_cap_time_fft_lsw.read()
        
        print 'time_sum_fft:', f.registers.nb_pfb_ss_time_trig_cap_trig_fft.read()
        
        
        return (fft_re, fft_im, fft_ch, fft_sync, fft_dv, fir_sync)
        
    def unpack_nb_sync(self, nb_sync):
        # ****  QUANT  ****
        nb_sync_re = nb_sync['re']
        nb_sync_im = nb_sync['im']
        nb_sync_sync = nb_sync['sync']
        nb_sync_dv = nb_sync['dv']
        nb_sync_ch = nb_sync['ch']
        nb_sync_cnt = nb_sync['sync_cnt']
        nb_sync_trig = nb_sync['trig']
        nb_sync_trig_time = nb_sync['trig_time']
        
        print 'NB Sync trig time'  
        print nb_sync_trig[0:10]
        print nb_sync_trig_time[0:10]        
        print 'curr_time_syncgen_msw:', f.registers.nb_pfb_ss_time_trig1_cap_curr_time_syncgen_msw.read()
        print 'curr_time_syncgen_lsw:', f.registers.nb_pfb_ss_time_trig1_cap_curr_time_syncgen_lsw.read()
        
        print 'cap_time_syncgen_msw:', f.registers.nb_pfb_ss_time_trig1_cap_time_syncgen_msw.read()
        print 'cap_time_syncgen_lsw:', f.registers.nb_pfb_ss_time_trig1_cap_time_syncgen_lsw.read()
        
        print 'time_sum_syncgen:', f.registers.nb_pfb_ss_time_trig1_cap_trig_syncgen.read()
       
        return (nb_sync_re, nb_sync_im, nb_sync_sync, nb_sync_dv, nb_sync_ch, nb_sync_cnt)    
    
    def unpack_quant(self, quant):
        # ****  QUANT  ****
        q_r0 = quant['real0']
        q_i0 = quant['imag0']
        q_r1 = quant['real1']
        q_i1 = quant['imag1']
        q_r2 = quant['real2']
        q_i2 = quant['imag2']
        q_r3 = quant['real3']
        q_i3 = quant['imag3']
        q_trig = quant['trig']
        q_trig_time = quant['trig_time']
        
        print 'Qaunt trig time'  
        print q_trig[0:10]
        print q_trig_time[0:10]        
        print 'curr_time_quant_msw:', f.registers.ss_time_trig1_cap_curr_time_quant_msw.read()
        print 'curr_time_quant_lsw:', f.registers.ss_time_trig1_cap_curr_time_quant_lsw.read()
        
        print 'cap_time_quant_msw:', f.registers.ss_time_trig1_cap_time_quant_msw.read()
        print 'cap_time_quant_lsw:', f.registers.ss_time_trig1_cap_time_quant_lsw.read()
        
        print 'time_sum_quant:', f.registers.ss_time_trig1_cap_trig_quant.read()
        
        q0_real = []
        q0_imag = []
            
        for x in range(0, len(q_r0)):
            q0_real.extend(
                [q_r0[x], q_r1[x], q_r2[x], q_r3[x]])
            
        for x in range(0, len(q_i0)):
            q0_imag.extend(
                [q_i0[x], q_i1[x], q_i2[x], q_i3[x]])

        return (q0_real, q0_imag)    

    def plot_adc_compare(self, adc0_in, adc0_0, adc1_in, adc1_0, adc2_in, adc2_0, adc3_in, adc3_0, adc_sync, adc_dv):
        
        plt.figure(1)
        plt.clf()
        plt.subplot(411)
        plt.plot(adc0_in)
        plt.plot(adc1_in)
        plt.subplot(412)
        plt.plot(adc2_in)
        plt.plot(adc3_in)
        
        plt.subplot(413)
        plt.plot(adc0_0)
        plt.plot(adc1_0)
        plt.subplot(414)
        plt.plot(adc2_0)
        plt.plot(adc3_0)
        
        plt.figure(2)
        plt.clf()
        plt.subplot(411)
        plt.plot(adc_sync[0])
        plt.plot(adc_sync[1])
        plt.subplot(412)
        plt.plot(adc_sync[2])
        plt.plot(adc_sync[3])
        
        plt.subplot(413)
        plt.plot(adc_dv[0])
        plt.plot(adc_dv[1])
        plt.subplot(414)
        plt.plot(adc_dv[2])
        plt.plot(adc_dv[3])
        
        
    def plot_fft_compare(self, real, imag, chan, fft_sync, fft_dv, fir_sync):
        
        plt.figure(3)
        plt.clf()
        plt.subplot(611)
        plt.plot(fft_sync[0])
        plt.plot(fft_sync[1])
        plt.plot(fft_sync[2])
        plt.plot(fft_sync[3])
        plt.subplot(612)
        plt.plot(fft_dv[0])
        plt.plot(fft_dv[1])
        plt.plot(fft_dv[2])
        plt.plot(fft_dv[3])
        plt.subplot(613)
        plt.plot(fir_sync[0])
        plt.plot(fir_sync[1])
        plt.plot(fir_sync[2])
        plt.plot(fir_sync[3])
        plt.subplot(614)
        plt.plot(chan[0])
        plt.plot(chan[1])
        plt.plot(chan[2])
        plt.plot(chan[3])
        plt.subplot(615)
        plt.plot(real[0])
        plt.plot(real[1])
        plt.plot(real[2])
        plt.plot(real[3])
        plt.subplot(616)
        plt.plot(imag[0])
        plt.plot(imag[1])
        plt.plot(imag[2])
        plt.plot(imag[3])


    def plot_nb_sync_compare(self, nb_sync_re, nb_sync_im, nb_sync_sync, nb_sync_dv, nb_sync_ch, nb_sync_cnt):
        
        plt.figure(5)
        plt.clf()
        plt.subplot(511)
        plt.plot(nb_sync_re[0])
        plt.plot(nb_sync_re[1])
        plt.plot(nb_sync_re[2])
        plt.plot(nb_sync_re[3])
        plt.subplot(512)
        plt.plot(nb_sync_sync[0])
        plt.plot(nb_sync_sync[1])
        plt.plot(nb_sync_sync[2])
        plt.plot(nb_sync_sync[3])
        plt.subplot(513)
        plt.plot(nb_sync_dv[0])
        plt.plot(nb_sync_dv[1])        
        plt.plot(nb_sync_dv[2])        
        plt.plot(nb_sync_dv[3])    
        plt.subplot(514)
        plt.plot(nb_sync_ch[0])
        plt.plot(nb_sync_ch[1])        
        plt.plot(nb_sync_ch[2])        
        plt.plot(nb_sync_ch[3])    
        plt.subplot(515)
        plt.plot(nb_sync_cnt[0])
        plt.plot(nb_sync_cnt[1])        
        plt.plot(nb_sync_cnt[2])        
        plt.plot(nb_sync_cnt[3])    
        
        
    def plot_quant_compare(self, real, imag):
        
        plt.figure(6)
        plt.clf()
        plt.subplot(211)
        plt.plot(real[0])
        plt.plot(real[1])
        plt.plot(real[2])
        plt.plot(real[3])
        plt.subplot(212)
        plt.plot(imag[0])
        plt.plot(imag[1])        
        plt.plot(imag[2])        
        plt.plot(imag[3])


#==============================================================================
        


for x in hosts:
    print '--------------------------------------------------------------------'
    print x

    f = casperfpga.CasperFpga(x)
    f.get_system_information(filename)
    
    # Select CD Bypass
    #-----------------
    f.registers.control.write(cd_bypass=0)
    
    # Check if HMC is ok
    print f.registers.cd_hmc_hmc_delay_status0.read()
    print f.registers.cd_hmc_hmc_delay_status1.read()
    print f.registers.cd_hmc_hmc_delay_status2.read()
    print f.registers.cd_hmc_hmc_delay_status3.read()
    print f.registers.cd_hmc_hmc_delay_status4.read()
    print f.registers.cd_hmc_hmc_delay_status5.read()
    
   
    # Setup mixer oscillator
    #-----------------------
    mix_freq = ((153500000)*np.power(2,22))/1712e6
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
	

    if x == 'skarab020303-01':  
        print "Setting Delays"
        print x
        f.registers.delay_whole0.write(initial=0)
        f.registers.delay_frac0.write(initial=0.0)
        f.registers.delta_delay_whole0.write(initial=0.0)
        f.registers.delta_delay_frac0.write(initial=0.0)
        f.registers.phase0.write(initial=0.0)
        f.registers.phase0.write(delta=0.0)
        
#        print f.registers.delay_whole0.read()
#        print f.registers.delay_frac0.read()
#        print f.registers.delta_delay_whole0.read()
#        print f.registers.delta_delay_frac0.read()
#        print f.registers.phase0.read()
#        print f.registers.phase0.read()        
    else:
        print "Setting Delays"
        print x
        f.registers.delay_whole0.write(initial=0)
        f.registers.delay_frac0.write(initial=0.0)
        f.registers.delta_delay_whole0.write(initial=0.0)
        f.registers.delta_delay_frac0.write(initial=0.0)
        f.registers.phase0.write(initial=0.0)
        f.registers.phase0.write(delta=0.0)
        
#        print f.registers.delay_whole0.read()
#        print f.registers.delay_frac0.read()
#        print f.registers.delta_delay_whole0.read()
#        print f.registers.delta_delay_frac0.read()
#        print f.registers.phase0.read()
#        print f.registers.phase0.read()   


    print 'Arming Snapshots'    

    f.snapshots.snap_adc2_ss.arm(man_trig=False, man_valid=False)
    
    f.snapshots.nb_pfb_ss_fft2_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.nb_pfb_ss_nb_sync_ss.arm(man_trig=False, man_valid=False)
    
    f.snapshots.snap_quant0_ss.arm(man_trig=False, man_valid=False)
    
    f.snapshots.phase_compensation0_delay_gen_ss_inputs_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.phase_compensation0_delay_gen_delay_gen_delay_calc_calc_ss.arm(man_trig=True, man_valid=True)
    f.snapshots.phase_compensation0_delay_gen_delay_gen_delay_calc_calc1_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.phase_compensation0_fd_fs_ss_fd_fs_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.phase_compensation0_fd_fs_ss_fd_fs1_ss.arm(man_trig=False, man_valid=False)

    print 'Grab all local times'
    print '===================='
    print 'Capture Time'
    # Tigger to capture 
    f.registers.control.write(local_time_capture='pulse')

    print 'Source: Spead Timestamp'
    f.registers.control.write(local_time_source=0)
    print f.registers.local_time_msw.read()
    print f.registers.local_time_lsw.read()

    print 'Source: time80_48 Timestamp'
    f.registers.control.write(local_time_source=1)
    print f.registers.local_time_msw.read()
    print f.registers.local_time_lsw.read()

    print 'Source: PFB Time Timestamp'
    f.registers.control.write(local_time_source=2)
    print f.registers.local_time_msw.read()
    print f.registers.local_time_lsw.read()

    print 'Source: Pack Sync Timestamp'
    f.registers.control.write(local_time_source=3)
    print f.registers.local_time_msw.read()
    print f.registers.local_time_lsw.read()

    print 'Setting up ss time trig for SS'
    print '=============================='
    # Tigger to capture 
    f.registers.control.write(local_time_capture='pulse')

    # Set time soure to time80_48
    f.registers.control.write(local_time_source=1)

    # Read back time (msw)
    curr_time_msw = f.registers.local_time_msw.read()
    curr_time_lsw = f.registers.local_time_lsw.read()
    
    
    print 'curr_time_msw:', curr_time_msw
    print 'curr_time_lsw:', curr_time_lsw
    
    #Determine which board has the h
    if highest_time_msw < curr_time_msw: 
        highest_time_msw = curr_time_msw
        
    if highest_time_lsw < curr_time_lsw: 
        highest_time_lsw = curr_time_lsw

    print 'Arming Done' 
    f.registers.tl_cd0_control0.write(arm='pulse')    
    f.registers.tl_cd0_control0.write(load_immediate='pulse')    
    f.registers.control.write(cnt_rst='pulse')
    f.registers.control.write(sys_rst='pulse')

#==============================================================================
print '***********************************************************************'
print 'Write the trigger time to all boards'

for x in hosts:
    print x
   
    f = casperfpga.CasperFpga(x)
    f.get_system_information(filename)
    # Now add time to just captured time. This needs to be far enough ahead that 
    # no FEng will there yet.
    trig_time_msw = highest_time_msw['data']['timestamp_msw']+ 5
    trig_time_lsw = highest_time_lsw['data']['timestamp_lsw']+ 2**9

    # Now write trigger time
    print 'Writing Trig time'
    f.registers.ss_trig_time_in_msw.write(time=trig_time_msw)
    f.registers.ss_trig_time_in_lsw.write(time=trig_time_lsw)
    
    print 'Trig time msw:', trig_time_msw
    print 'Trig time lsw:', trig_time_lsw    

    print 'Read back written data'
    print 'ss_trig_time_in_msw:', f.registers.ss_trig_time_in_msw.read()
    print 'ss_trig_time_in_lsw:', f.registers.ss_trig_time_in_lsw.read()

   
    f.registers.arm_ss_ts_rst.write(rst='pulse')
    f.registers.ts_ss_lock.write(en=1)
    f.registers.arm_ts_ss_lock.write(en='pulse')
    
    print 'curr_time_msw:', f.registers.local_time_msw.read()
    print 'curr_time_lsw:', f.registers.local_time_lsw.read()

print '***********************************************************************'

f0 = casperfpga.CasperFpga(hosts[0])
f0.get_system_information(filename)

f1 = casperfpga.CasperFpga(hosts[1])
f1.get_system_information(filename)

f2 = casperfpga.CasperFpga(hosts[2])
f2.get_system_information(filename)

f3 = casperfpga.CasperFpga(hosts[3])
f3.get_system_information(filename)

# Read FFT offset calculations for each Skarab
s0 = skarab_debug()
s0.get_fft_offset(f0)
s1 = skarab_debug()
s1.get_fft_offset(f1)
s2 = skarab_debug()
s2.get_fft_offset(f2)
s3 = skarab_debug()
s3.get_fft_offset(f3)

compare_all = all_skarab_debug()

# Grab SS Data for all skarabs
compare_all.get_adc_SS_data_compare(f0,f1,f2,f3)
compare_all.get_fft_SS_data_compare(f0,f1,f2,f3)
compare_all.get_nb_sync_SS_data_compare(f0,f1,f2,f3)
compare_all.get_quant_SS_data_compare(f0,f1,f2,f3)

# Get Sync Counts
print 'cd_status0:', f0.registers.cd_status.read()
print 'cd_status1:', f1.registers.cd_status.read()
print 'cd_status2:', f2.registers.cd_status.read()
print 'cd_status3:', f3.registers.cd_status.read()
print '***'
print ''

print 'ddc_status0:', f0.registers.ddc_status.read()
print 'ddc_status1:', f1.registers.ddc_status.read()
print 'ddc_status2:', f2.registers.ddc_status.read()
print 'ddc_status3:', f3.registers.ddc_status.read()
print '***'
print ''

print 'nb_status0:', f0.registers.nb_status.read()
print 'nb_status1:', f1.registers.nb_status.read()
print 'nb_status2:', f2.registers.nb_status.read()
print 'nb_status3:', f3.registers.nb_status.read()
print '***'
print ''

print 'fdfs_sync_cnt0:', f0.registers.fdfs_sync_cnt.read()
print 'fdfs_sync_cnt1:', f1.registers.fdfs_sync_cnt.read()
print 'fdfs_sync_cnt2', f2.registers.fdfs_sync_cnt.read()
print 'fdfs_sync_cnt3:', f3.registers.fdfs_sync_cnt.read()
print '***'
print ''

print 'quant_sync_cnt0:', f0.registers.quant_sync_cnt.read()
print 'quant_sync_cnt1:', f1.registers.quant_sync_cnt.read()
print 'quant_sync_cnt2:', f2.registers.quant_sync_cnt.read()
print 'quant_sync_cnt3:', f3.registers.quant_sync_cnt.read()

#s0.unpack_and_plot_adc(adc0)
plt.show()

#for x in hosts:
#    print '*******************************************************************'
#    print x
#    
#    f = casperfpga.CasperFpga(x)
#    f.get_system_information('/home/avanderbyl/fpgs/s_c_nbe_m1k_2019-05-24_1545.fpg')
#    
##    print 'FDFS offset values'
##    print f.registers.dds_fft_bin.read()
##    print f.registers.dds_fft_phase_offset.read()
#                
#    # Grab ADC data and Quant data as a sanity check    
#    #-----------------------------------------------
#    adc2 = f.snapshots.snap_adc2_ss.read(arm=False)['data']
#       
#    fft2 = f.snapshots.nb_pfb_ss_fft2_ss.read(arm=False)['data']
#        
#    quant0_ss = f.snapshots.snap_quant0_ss.read(arm=False)['data']
#    
#    inputs = f.snapshots.phase_compensation0_delay_gen_ss_inputs_ss.read(arm=False)['data']
#    delay_calc = f.snapshots.phase_compensation0_delay_gen_delay_gen_delay_calc_calc_ss.read(arm=False)['data']
#    delay_coeff = f.snapshots.phase_compensation0_delay_gen_delay_gen_delay_calc_calc1_ss.read(arm=False)['data']
#    fd_fs = f.snapshots.phase_compensation0_fd_fs_ss_fd_fs_ss.read(arm=False)['data']
#    fd_fs1 = f.snapshots.phase_compensation0_fd_fs_ss_fd_fs1_ss.read(arm=False)['data']
#    
#
#    # ADC
#    adc2_0 = adc2['p0_d0']
#    adc2_1 = adc2['p0_d1']
#    adc2_2 = adc2['p0_d2']
#    adc2_3 = adc2['p0_d3']
#    adc2_4 = adc2['p0_d4']
#    adc2_5 = adc2['p0_d5']
#    adc2_6 = adc2['p0_d6']
#    adc2_7 = adc2['p0_d7']
#    adc2_sync = adc2['sync']
#    adc2_dv = adc2['dv']  
#    adc2_trig = adc2['trig']
#    adc2_trig_time = adc2['trig_time']
#
#    print 'ADC trig time'  
#    print adc2_trig[0:10]
#    print adc2_trig_time[0:10]
#    print 'curr_time_adc' 
#    print f.registers.ss_time_trig_cap_curr_time_adc.read()
#    print 'cap_time_adc' 
#    print f.registers.ss_time_trig_cap_time_adc.read()
#    print 'cap_trig_adc' 
#    print f.registers.ss_time_trig_cap_trig_adc.read()
#     
#    #------------------------------------------------------------------------------
#    adc2_input = []
#            
#    for x in range(0, len(adc2_0)):
#        adc2_input.extend(
#            [adc2_0[x], adc2_1[x], adc2_2[x], adc2_3[x], adc2_4[x], adc2_5[x], adc2_6[x], adc2_7[x]])
#        
#    #------------------------------------------------------------------------------
#        
#    # FFT: 2
#    fft_ch2 = fft2['fft_ch']
#    fft_re2 = fft2['fft_re']
#    fft_im2 = fft2['fft_im']
#    fft_dv2 = fft2['fft_dv']
#    fft_fs2 = fft2['fft_fs']
#    fft_tl2 = fft2['fft_tl']
#    fft_sync2 = fft2['fft_sync']
#    fft_of2 = fft2['fft_of']
#    fft_tready2 = fft2['fft_tready']
#    fft_tlast_miss2 = fft2['tlast_miss']
#    fft_tlast_unexp2 = fft2['tlast_unexp']
#    fir_sync2 = fft2['fir_sync']
#    fft_trig = fft2['trig']
#    fft_trig_time = fft2['trig_time']
#        
#    #------------------------------------------------------------------------------
#
#    # ****  QUANT  ****
#    q0_r0 = quant0_ss['real0']
#    q0_i0 = quant0_ss['imag0']
#    q0_r1 = quant0_ss['real1']
#    q0_i1 = quant0_ss['imag1']
#    q0_r2 = quant0_ss['real2']
#    q0_i2 = quant0_ss['imag2']
#    q0_r3 = quant0_ss['real3']
#    q0_i3 = quant0_ss['imag3']
#    q0_trig = quant0_ss['trig']
#    q0_trig_time = quant0_ss['trig_time']
#        
#           
#    q0_real = []
#    q0_imag = []
#            
#    for x in range(0, len(q0_r0)):
#        q0_real.extend(
#            [q0_r0[x], q0_r1[x], q0_r2[x], q0_r3[x]])
#        
#    for x in range(0, len(q0_i0)):
#        q0_imag.extend(
#            [q0_i0[x], q0_i1[x], q0_i2[x], q0_i3[x]])
#    q0_complx_sq = q0_real + np.multiply(q0_imag, 1j)
#        
#    #------------------------------------------------------------------------------
#
#    # ****  fd_fs  ****
#    fd_fs_sync = fd_fs['sync']
#    fd_fs_x = fd_fs['x']
#    fd_fs_a0 = fd_fs['a0']
#    fd_fs_a1 = fd_fs['a1']
#    fd_fs_cos = fd_fs['cos']
#
#    # ****  fd_fs1  ****
#    fd_fs_cos1 = fd_fs1['cos']
#    fd_fs_sin1 = fd_fs1['sin']
#    b_real = fd_fs1['b_real']
#    b_imag = fd_fs1['b_imag']
#    out_real = fd_fs1['out_real']
#    out_imag = fd_fs1['out_imag']

#    plt.figure(13)
#    plt.clf()    
#    plt.subplot(511)
#    plt.plot(fd_fs_sync)
#    plt.subplot(512)
#    plt.plot(fd_fs_x)
#    plt.subplot(513)
#    plt.plot(fd_fs_a0)
#    plt.subplot(514)
#    plt.plot(fd_fs_a1)
#    plt.subplot(515)
#    plt.plot(fd_fs_cos)
#        
#        
#    plt.figure(14)
#    plt.clf()    
#    plt.subplot(611)
#    plt.plot(fd_fs_cos1)
#    plt.subplot(612)
#    plt.plot(fd_fs_sin1)
#    plt.subplot(613)
#    plt.plot(b_real)
#    plt.subplot(614)
#    plt.plot(b_imag)
#    plt.subplot(615)
#    plt.plot(out_real)
#    plt.subplot(616)
#    plt.plot(out_imag)  
#    
#    plt.show() 