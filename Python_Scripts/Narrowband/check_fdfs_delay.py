import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

#==============================================================================
#   Classes and methods
#==============================================================================
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
    def adc_SS_data_compare (self, f0,f1,f2,f3):
        
        adc0 = f0.snapshots.snap_adc_ss.read(arm=False)['data']
        adc1 = f1.snapshots.snap_adc_ss.read(arm=False)['data']
        adc2 = f2.snapshots.snap_adc_ss.read(arm=False)['data']
        adc3 = f3.snapshots.snap_adc_ss.read(arm=False)['data']

        [adc0_in, adc0_0, adc0_sync, adc0_dv] = self.unpack_adc(adc0)
        [adc1_in, adc1_0, adc1_sync, adc1_dv] = self.unpack_adc(adc1)
        [adc2_in, adc2_0, adc2_sync, adc2_dv] = self.unpack_adc(adc2)
        [adc3_in, adc3_0, adc3_sync, adc3_dv] = self.unpack_adc(adc3)
        
        adc_sync = [adc0_sync, adc1_sync, adc2_sync, adc3_sync]
        adc_dv = [adc0_dv, adc1_dv, adc2_dv, adc3_dv]
                
        self.plot_adc_compare(adc0_in, adc0_0, adc1_in, adc1_0, adc2_in, adc2_0, adc3_in, adc3_0, adc_sync, adc_dv)
        
        
    def pfbin_SS_data_compare (self, f0,f1,f2,f3):
        pfbin0 = f0.snapshots.snap_pfbin_ss.read(arm=False)['data'] 
        pfbin1 = f1.snapshots.snap_pfbin_ss.read(arm=False)['data'] 
        pfbin2 = f2.snapshots.snap_pfbin_ss.read(arm=False)['data'] 
        pfbin3 = f3.snapshots.snap_pfbin_ss.read(arm=False)['data'] 
        
        [pfbin0_input, pfbin0_0, pfbin0_sync, pfbin0_dv] = self.unpack_pfbin(pfbin0)
        [pfbin1_input, pfbin1_0, pfbin1_sync, pfbin1_dv] = self.unpack_pfbin(pfbin1)
        [pfbin2_input, pfbin2_0, pfbin2_sync, pfbin2_dv] = self.unpack_pfbin(pfbin2)
        [pfbin3_input, pfbin3_0, pfbin3_sync, pfbin3_dv] = self.unpack_pfbin(pfbin3)
        
        pfb_sync = [pfbin0_sync, pfbin1_sync, pfbin2_sync, pfbin3_sync]
        pfb_dv = [pfbin0_dv, pfbin1_dv, pfbin2_dv, pfbin3_dv]  
        
        self.plot_pfbin_compare(pfbin0_input, pfbin0_0, pfbin1_input, pfbin1_0, pfbin2_input, pfbin2_0, pfbin3_input, pfbin3_0, pfb_sync, pfb_dv)    

    def mix_SS_data_compare (self, f0,f1,f2,f3):
        mix0 = f0.snapshots.DDC_snap_mix_ss.read(arm=False)['data'] 
        mix1 = f1.snapshots.DDC_snap_mix_ss.read(arm=False)['data'] 
        mix2 = f2.snapshots.DDC_snap_mix_ss.read(arm=False)['data'] 
        mix3 = f3.snapshots.DDC_snap_mix_ss.read(arm=False)['data'] 
        
        [mix0_out, mix0_0, mix0_sync, mix0_dv] = self.unpack_mix(mix0)
        [mix1_out, mix1_0, mix1_sync, mix1_dv] = self.unpack_mix(mix1)
        [mix2_out, mix2_0, mix2_sync, mix2_dv] = self.unpack_mix(mix2)
        [mix3_out, mix3_0, mix3_sync, mix3_dv] = self.unpack_mix(mix3)
        
        mix_sync = [mix0_sync, mix1_sync, mix2_sync, mix3_sync]
        mix_dv = [mix0_dv, mix1_dv, mix2_dv, mix3_dv]  
        
        self.plot_mix_compare(mix0_out, mix0_0, mix1_out, mix1_0, mix2_out, mix2_0, mix3_out, mix3_0, mix_sync, mix_dv)    
        
    def ddc_SS_data_compare (self, f0,f1,f2,f3):
        ddc0 = f0.snapshots.DDC_snap_ddc_ss.read(arm=False)['data'] 
        ddc1 = f1.snapshots.DDC_snap_ddc_ss.read(arm=False)['data'] 
        ddc2 = f2.snapshots.DDC_snap_ddc_ss.read(arm=False)['data'] 
        ddc3 = f3.snapshots.DDC_snap_ddc_ss.read(arm=False)['data'] 
        
        [ddc0_out, ddc0_sync, ddc0_dv] = self.unpack_ddc(ddc0)
        [ddc1_out, ddc1_sync, ddc1_dv] = self.unpack_ddc(ddc1)
        [ddc2_out, ddc2_sync, ddc2_dv] = self.unpack_ddc(ddc2)
        [ddc3_out, ddc3_sync, ddc3_dv] = self.unpack_ddc(ddc3)
        
        ddc_sync = [ddc0_sync, ddc1_sync, ddc2_sync, ddc3_sync]
        ddc_dv = [ddc0_dv, ddc1_dv, ddc2_dv, ddc3_dv]  
        
        self.plot_ddc_compare(ddc0_out, ddc1_out, ddc2_out, ddc3_out, ddc_sync, ddc_dv)    

    def fir_SS_data_compare (self, f0,f1,f2,f3):
        fir0 = f0.snapshots.nb_pfb_ss_fir_out_ss.read(arm=False)['data'] 
        fir1 = f1.snapshots.nb_pfb_ss_fir_out_ss.read(arm=False)['data'] 
        fir2 = f2.snapshots.nb_pfb_ss_fir_out_ss.read(arm=False)['data'] 
        fir3 = f3.snapshots.nb_pfb_ss_fir_out_ss.read(arm=False)['data'] 
        
        [fir0_out, fir0_sync, fir0_dv, fir0_tlast] = self.unpack_fir(fir0)
        [fir1_out, fir1_sync, fir1_dv, fir1_tlast] = self.unpack_fir(fir1)
        [fir2_out, fir2_sync, fir2_dv, fir2_tlast] = self.unpack_fir(fir2)
        [fir3_out, fir3_sync, fir3_dv, fir3_tlast] = self.unpack_fir(fir3)
        
        fir_sync = [fir0_sync, fir1_sync, fir2_sync, fir3_sync]
        fir_dv = [fir0_dv, fir1_dv, fir2_dv, fir3_dv]  
        fir_tlast = [fir0_tlast, fir1_tlast, fir2_tlast, fir3_tlast]
        
        self.plot_fir_compare(fir0_out, fir1_out, fir2_out, fir3_out, fir_sync, fir_dv, fir_tlast)             
        
    def fft_SS_data_compare (self, f0,f1,f2,f3):
        fft0 = f0.snapshots.nb_pfb_ss_fft_ss.read(arm=False)['data'] 
        fft1 = f1.snapshots.nb_pfb_ss_fft_ss.read(arm=False)['data'] 
        fft2 = f2.snapshots.nb_pfb_ss_fft_ss.read(arm=False)['data'] 
        fft3 = f3.snapshots.nb_pfb_ss_fft_ss.read(arm=False)['data'] 
        
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


    def nb_sync_SS_data_compare (self, f0,f1,f2,f3):
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
        
    def quant_SS_data_compare (self, f0,f1,f2,f3):
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
        print 'curr_time_adc_msw:', f.registers.ss_time_trig_adc_cap_curr_time_adc_msw.read()
        print 'curr_time_adc_lsw:', f.registers.ss_time_trig_adc_cap_curr_time_adc_lsw.read()
        print 'cap_time_adc_msw:', f.registers.ss_time_trig_adc_cap_time_adc_msw.read()
        print 'cap_time_adc_lsw:', f.registers.ss_time_trig_adc_cap_time_adc_lsw.read()
        print 'trig_time_adc:', f.registers.ss_time_trig_adc_cap_trig_adc.read()
        
        adc_input = []
            
        for x in range(0, len(adc_0)):
            adc_input.extend(
                    [adc_0[x], adc_1[x], adc_2[x], adc_3[x], adc_4[x], adc_5[x], adc_6[x], adc_7[x]])
        
        return (adc_input, adc_0, adc_sync, adc_dv)    

    def unpack_pfbin(self, pfbin):
        # pfbin
        pfbin_0 = pfbin['p0_d0']
        pfbin_1 = pfbin['p0_d1']
        pfbin_2 = pfbin['p0_d2']
        pfbin_3 = pfbin['p0_d3']
        pfbin_4 = pfbin['p0_d4']
        pfbin_5 = pfbin['p0_d5']
        pfbin_6 = pfbin['p0_d6']
        pfbin_7 = pfbin['p0_d7']
        pfbin_sync = pfbin['sync']
        pfbin_dv = pfbin['dv']  
        pfbin_trig = pfbin['trig']
        pfbin_trig_time = pfbin['trig_time']

        print 'PFB trig time'  
        print pfbin_trig[0:10]
        print pfbin_trig_time[0:10]
        print 'curr_time_pfb_msw:', f.registers.ss_time_trig_pfbin_cap_curr_time_pfb_msw.read()
        print 'curr_time_pfb_lsw:', f.registers.ss_time_trig_pfbin_cap_curr_time_pfb_lsw.read()
        print 'cap_time_pfb_msw:', f.registers.ss_time_trig_pfbin_cap_time_pfb_msw.read()
        print 'cap_time_pfb_lsw:', f.registers.ss_time_trig_pfbin_cap_time_pfb_lsw.read()
        print 'trig_time_pfb:', f.registers.ss_time_trig_pfbin_cap_trig_pfb.read()
        
        pfbin_input = []
            
        for x in range(0, len(pfbin_0)):
            pfbin_input.extend(
                    [pfbin_0[x], pfbin_1[x], pfbin_2[x], pfbin_3[x], pfbin_4[x], pfbin_5[x], pfbin_6[x], pfbin_7[x]])
        
        return (pfbin_input, pfbin_0, pfbin_sync, pfbin_dv)  


    def unpack_mix(self, mix):
        # pfbin
        mix_0 = mix['p0_d0']
        mix_1 = mix['p0_d1']
        mix_2 = mix['p0_d2']
        mix_3 = mix['p0_d3']
        mix_4 = mix['p0_d4']
        mix_5 = mix['p0_d5']
        mix_6 = mix['p0_d6']
        mix_7 = mix['p0_d7']
        mix_sync = mix['sync']
        mix_dv = mix['dv']  
        mix_trig = mix['trig']
        mix_trig_time = mix['trig_time']

        print 'Mix trig time'  
        print mix_trig[0:10]
        print mix_trig_time[0:10]
        print 'curr_time_mix_msw:', f.registers.DDC_ss_time_trig_cap_curr_time_mix_msw.read()
        print 'curr_time_mix_lsw:', f.registers.DDC_ss_time_trig_cap_curr_time_mix_lsw.read()
        print 'cap_time_mix_msw:', f.registers.DDC_ss_time_trig_cap_time_mix_msw.read()
        print 'cap_time_mix_lsw:', f.registers.DDC_ss_time_trig_cap_time_mix_lsw.read()
        print 'trig_time_mix:', f.registers.DDC_ss_time_trig_cap_trig_mix.read()
        
        mix_out = []
            
        for x in range(0, len(mix_0)):
            mix_out.extend(
                    [mix_0[x], mix_1[x], mix_2[x], mix_3[x], mix_4[x], mix_5[x], mix_6[x], mix_7[x]])
        
        return (mix_out, mix_0, mix_sync, mix_dv)  

    def unpack_ddc(self, ddc):
        # pfbin
        ddc_out = ddc['p0']
        ddc_sync = ddc['sync']
        ddc_dv = ddc['dv']  
        ddc_trig = ddc['trig']
        ddc_trig_time = ddc['trig_time']

        print 'DDC trig time'  
        print ddc_trig[0:10]
        print ddc_trig_time[0:10]
        print 'curr_time_ddc_msw:', f.registers.DDC_ss_time_trig1_cap_curr_time_ddc_msw.read()
        print 'curr_time_ddc_lsw:', f.registers.DDC_ss_time_trig1_cap_curr_time_ddc_lsw.read()
        print 'cap_time_ddc_msw:', f.registers.DDC_ss_time_trig1_cap_time_ddc_msw.read()
        print 'cap_time_ddc_lsw:', f.registers.DDC_ss_time_trig1_cap_time_ddc_lsw.read()
        print 'trig_time_ddc:', f.registers.DDC_ss_time_trig1_cap_trig_ddc.read()
        
       
        return (ddc_out, ddc_sync, ddc_dv)  


    def unpack_fir(self, fir):
        # pfbin
        fir_out = fir['fir']
        fir_sync = fir['sync']
        fir_tlast = fir['tlast']
        fir_dv = fir['dv']  
        fir_trig = fir['trig']
        fir_trig_time = fir['trig_time']

        print 'FIR trig time'  
        print fir_trig[0:10]
        print fir_trig_time[0:10]
        print 'curr_time_fir_msw:', f.registers.nb_pfb_ss_time_trig_fir_cap_curr_time_fir_msw.read()
        print 'curr_time_fir_lsw:', f.registers.nb_pfb_ss_time_trig_fir_cap_curr_time_fir_lsw.read()
        print 'cap_time_fir_msw:', f.registers.nb_pfb_ss_time_trig_fir_cap_time_fir_msw.read()
        print 'cap_time_fir_lsw:', f.registers.nb_pfb_ss_time_trig_fir_cap_time_fir_lsw.read()
        print 'trig_time_fir:', f.registers.nb_pfb_ss_time_trig_fir_cap_trig_fir.read()
        
       
        return (fir_out, fir_sync, fir_dv, fir_tlast)  

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
        
        print 'fft trig time'    
        print fft_trig[0:10]
        print fft_trig_time[0:10]
        
        print 'curr_time_fft_msw:', f.registers.nb_pfb_ss_time_trig_fft_cap_curr_time_fft_msw.read()
        print 'curr_time_fft_lsw:', f.registers.nb_pfb_ss_time_trig_fft_cap_curr_time_fft_lsw.read()

        print 'cap_time_fft_msw:',  f.registers.nb_pfb_ss_time_trig_fft_cap_time_fft_msw.read()
        print 'cap_time_fft_lsw:', f.registers.nb_pfb_ss_time_trig_fft_cap_time_fft_lsw.read()
        
        print 'trig_time_fft:', f.registers.nb_pfb_ss_time_trig_fft_cap_trig_fft.read()

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
        print 'curr_time_syncgen_msw:', f.registers.nb_pfb_ss_time_trig_syncgen_cap_curr_time_syncgen_msw.read()
        print 'curr_time_syncgen_lsw:', f.registers.nb_pfb_ss_time_trig_syncgen_cap_curr_time_syncgen_lsw.read()
        
        print 'cap_time_syncgen_msw:', f.registers.nb_pfb_ss_time_trig_syncgen_cap_time_syncgen_msw.read()
        print 'cap_time_syncgen_lsw:', f.registers.nb_pfb_ss_time_trig_syncgen_cap_time_syncgen_lsw.read()
        
        print 'time_sum_syncgen:', f.registers.nb_pfb_ss_time_trig_syncgen_cap_trig_syncgen.read()
       
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
        print 'curr_time_quant_msw:', f.registers.ss_time_trig_quant_cap_curr_time_quant_msw.read()
        print 'curr_time_quant_lsw:', f.registers.ss_time_trig_quant_cap_curr_time_quant_lsw.read()
        
        print 'cap_time_quant_msw:', f.registers.ss_time_trig_quant_cap_time_quant_msw.read()
        print 'cap_time_quant_lsw:', f.registers.ss_time_trig_quant_cap_time_quant_lsw.read()
        
        print 'time_sum_quant:', f.registers.ss_time_trig_quant_cap_trig_quant.read()
        
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
        
    def plot_pfbin_compare(self, pfbin0_input, pfbin0_0, pfbin1_input, pfbin1_0, pfbin2_input, pfbin2_0, pfbin3_input, pfbin3_0, pfb_sync, pfb_dv):
        
        plt.figure(3)
        plt.clf()
        plt.subplot(411)
        plt.plot(pfbin0_input)
        plt.plot(pfbin1_input)
        plt.subplot(412)
        plt.plot(pfbin2_input)
        plt.plot(pfbin3_input)
        
        plt.subplot(413)
        plt.plot(pfbin0_0)
        plt.plot(pfbin1_0)
        plt.subplot(414)
        plt.plot(pfbin2_0)
        plt.plot(pfbin3_0)
        
        plt.figure(4)
        plt.clf()
        plt.subplot(411)
        plt.plot(pfb_sync[0])
        plt.plot(pfb_sync[1])
        plt.subplot(412)
        plt.plot(pfb_sync[2])
        plt.plot(pfb_sync[3])
        
        plt.subplot(413)
        plt.plot(pfb_dv[0])
        plt.plot(pfb_dv[1])
        plt.subplot(414)
        plt.plot(pfb_dv[2])
        plt.plot(pfb_dv[3])        
 
    def plot_mix_compare(self, mix0_out, mix0_0, mix1_out, mix1_0, mix2_out, mix2_0, mix3_out, mix3_0, mix_sync, mix_dv):
        
        plt.figure(5)
        plt.clf()
        plt.subplot(411)
        plt.plot(mix0_out)
        plt.plot(mix1_out)
        plt.subplot(412)
        plt.plot(mix2_out)
        plt.plot(mix3_out)
        
        plt.subplot(413)
        plt.plot(mix0_0)
        plt.plot(mix1_0)
        plt.subplot(414)
        plt.plot(mix2_0)
        plt.plot(mix3_0)
        
        plt.figure(6)
        plt.clf()
        plt.subplot(411)
        plt.plot(mix_sync[0])
        plt.plot(mix_sync[1])
        plt.subplot(412)
        plt.plot(mix_sync[2])
        plt.plot(mix_sync[3])
        
        plt.subplot(413)
        plt.plot(mix_dv[0])
        plt.plot(mix_dv[1])
        plt.subplot(414)
        plt.plot(mix_dv[2])
        plt.plot(mix_dv[3])       
        
        
    def plot_ddc_compare(self, ddc0_out, ddc1_out, ddc2_out, ddc3_out, ddc_sync, ddc_dv):
        
        plt.figure(7)
        plt.clf()
        plt.subplot(311)
        plt.plot(ddc0_out)
        plt.plot(ddc1_out)
        
        plt.subplot(312)
        plt.plot(ddc2_out)
        plt.plot(ddc3_out)
        
        plt.subplot(313)
        plt.plot(ddc_sync)
        plt.plot(ddc_dv)


        
    def plot_fir_compare(self, fir0_out, fir1_out, fir2_out, fir3_out, fir_sync, fir_dv, fir_tlast):
        
        plt.figure(8)
        plt.clf()
        plt.subplot(511)
        plt.plot(fir0_out)
        plt.plot(fir1_out)
        plt.subplot(512)
        plt.plot(fir2_out)
        plt.plot(fir3_out)
               
        plt.subplot(513)
        plt.plot(fir_sync[0])
        plt.plot(fir_sync[1])
        plt.plot(fir_sync[0])
        plt.plot(fir_sync[1])

        plt.subplot(514)
        plt.plot(fir_dv[2])
        plt.plot(fir_dv[3])     
        plt.plot(fir_dv[0])
        plt.plot(fir_dv[1])
        
        plt.subplot(515)
        plt.plot(fir_tlast[2])
        plt.plot(fir_tlast[3])     
        plt.plot(fir_tlast[0])
        plt.plot(fir_tlast[1])
        
        
    def plot_fft_compare(self, real, imag, chan, fft_sync, fft_dv, fir_sync):
        
        complx0 = real[0] + np.multiply(imag[0], 1j)
        complx1 = real[1] + np.multiply(imag[1], 1j)
        complx2 = real[2] + np.multiply(imag[2], 1j)
        complx3 = real[3] + np.multiply(imag[3], 1j)
        
        plt.figure(9)
        plt.clf()
        plt.subplot(511)
        plt.plot(fft_sync[0])
        plt.plot(fft_sync[1])
        plt.plot(fft_sync[2])
        plt.plot(fft_sync[3])
        plt.subplot(512)
        plt.plot(fft_dv[0])
        plt.plot(fft_dv[1])
        plt.plot(fft_dv[2])
        plt.plot(fft_dv[3])
        plt.subplot(513)
        plt.plot(fir_sync[0])
        plt.plot(fir_sync[1])
        plt.plot(fir_sync[2])
        plt.plot(fir_sync[3])
        plt.subplot(514)
        plt.plot(chan[0])
        plt.plot(chan[1])
        plt.plot(chan[2])
        plt.plot(chan[3])
        plt.subplot(515)
        plt.plot(np.square(np.abs(complx0)))
        plt.plot(np.square(np.abs(complx1)))
        plt.plot(np.square(np.abs(complx2)))
        plt.plot(np.square(np.abs(complx3)))


    def plot_nb_sync_compare(self, nb_sync_re, nb_sync_im, nb_sync_sync, nb_sync_dv, nb_sync_ch, nb_sync_cnt):
        
        complx0 = nb_sync_re[0] + np.multiply(nb_sync_im[0], 1j)
        complx1 = nb_sync_re[1] + np.multiply(nb_sync_im[1], 1j)
        complx2 = nb_sync_re[2] + np.multiply(nb_sync_im[2], 1j)
        complx3 = nb_sync_re[3] + np.multiply(nb_sync_im[3], 1j)
        
        plt.figure(10)
        plt.clf()
        plt.subplot(511)
        plt.plot(np.square(np.abs(complx0)))
        plt.plot(np.square(np.abs(complx1)))
        plt.plot(np.square(np.abs(complx2)))
        plt.plot(np.square(np.abs(complx3)))
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
        
        complx0 = real[0] + np.multiply(imag[0], 1j)
        complx1 = real[1] + np.multiply(imag[1], 1j)
        complx2 = real[2] + np.multiply(imag[2], 1j)
        complx3 = real[3] + np.multiply(imag[3], 1j)
        
        plt.figure(11)
        plt.clf()
        plt.plot(np.square(np.abs(complx0)))
        plt.plot(np.square(np.abs(complx1)))
        plt.plot(np.square(np.abs(complx2)))
        plt.plot(np.square(np.abs(complx3)))


#==============================================================================
# End of classes and methods
#==============================================================================
        



hosts = ['skarab020303-01','skarab020308-01','skarab02030A-01','skarab02030E-01']
highest_time_msw = 0
highest_time_lsw = 0

filename = '/home/avanderbyl/fpgs/s_c_nbe_m1k_2019-05-30_2132.fpg'

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
        print ' ' 
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
        print ' ' 
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


    print ' ' 
    print 'Arming Snapshots'      
    print '================'  

    f.snapshots.snap_adc_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.snap_pfbin_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.DDC_snap_mix_ss.arm(man_trig=False, man_valid=False)    
    f.snapshots.DDC_snap_ddc_ss.arm(man_trig=False, man_valid=False)   
    f.snapshots.nb_pfb_ss_fir_out_ss.arm(man_trig=False, man_valid=False)     
    f.snapshots.nb_pfb_ss_fft_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.nb_pfb_ss_nb_sync_ss.arm(man_trig=False, man_valid=False)    
    f.snapshots.nb_pfb_ss_nb_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.nb_pfb_ss_nb1_ss.arm(man_trig=False, man_valid=False)
    
    
    f.snapshots.snap_quant0_ss.arm(man_trig=False, man_valid=False)
    
    f.snapshots.phase_compensation0_delay_gen_ss_inputs_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.phase_compensation0_delay_gen_delay_gen_delay_calc_calc_ss.arm(man_trig=True, man_valid=True)
    f.snapshots.phase_compensation0_delay_gen_delay_gen_delay_calc_calc1_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.phase_compensation0_fd_fs_ss_fd_fs_ss.arm(man_trig=False, man_valid=False)
    f.snapshots.phase_compensation0_fd_fs_ss_fd_fs1_ss.arm(man_trig=False, man_valid=False)
    
    print ' ' 
    print 'Arming Done' 
    print '==========='
    
#    print ' ' 
#    print 'Grab all local times'
#    print '===================='
#    print 'Capture Time'
#    # Tigger to capture 
#    f.registers.control.write(local_time_capture='pulse')
#
#    print 'Source: Spead Timestamp'
#    f.registers.control.write(local_time_source=0)
#    print f.registers.local_time_msw.read()
#    print f.registers.local_time_lsw.read()
#
#    print 'Source: time80_48 Timestamp'
#    f.registers.control.write(local_time_source=1)
#    print f.registers.local_time_msw.read()
#    print f.registers.local_time_lsw.read()
#
#    print 'Source: PFB Time Timestamp'
#    f.registers.control.write(local_time_source=2)
#    print f.registers.local_time_msw.read()
#    print f.registers.local_time_lsw.read()
#
#    print 'Source: Pack Sync Timestamp'
#    f.registers.control.write(local_time_source=3)
#    print f.registers.local_time_msw.read()
#    print f.registers.local_time_lsw.read()
#
    print ' ' 
    print 'Setting up ss time trig for SS'
    print '=============================='
    print ' ' 
    # Tigger to capture 
    f.registers.control.write(local_time_capture='pulse')

    # Set time soure to time80_48
    f.registers.control.write(local_time_source=1)

    # Read back current time 
    curr_time_msw = f.registers.local_time_msw.read()
    curr_time_lsw = f.registers.local_time_lsw.read()
    
    print 'curr_time_msw:', curr_time_msw
    print 'curr_time_lsw:', curr_time_lsw
    print ' ' 
    
    #Determine which board has the h
    if highest_time_msw < curr_time_msw: 
        highest_time_msw = curr_time_msw
        
    if highest_time_lsw < curr_time_lsw: 
        highest_time_lsw = curr_time_lsw


    f.registers.tl_cd0_control0.write(arm='pulse')    
    f.registers.tl_cd0_control0.write(load_immediate='pulse')    
    f.registers.control.write(cnt_rst='pulse')
    f.registers.control.write(sys_rst='pulse')

#==============================================================================
print '************************************'
print 'Write the trigger time to all boards'
print '************************************'


for x in hosts:
    print x
   
    f = casperfpga.CasperFpga(x)
    f.get_system_information(filename)
    # Now add time to just captured time. This needs to be far enough ahead that 
    # no FEng will there yet.
    trig_time_msw = highest_time_msw['data']['timestamp_msw']+ 7
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

    print 'Arming time trigger'
    f.registers.arm_ss_ts_rst.write(rst='pulse')
    f.registers.ts_ss_lock.write(en=0)
    f.registers.arm_ts_ss_lock.write(en='pulse')
    
    if f.registers.ts_ss_lock.read()['data']['en'] == 1:
        print 'Trigger source: Time trigger'
    else:
        print 'Trigger source: Sync'
            
    
    print 'curr_time_msw:', f.registers.local_time_msw.read()
    print 'curr_time_lsw:', f.registers.local_time_lsw.read()

print '***********************************************************************'
print ' ' 

f0 = casperfpga.CasperFpga(hosts[0])
f0.get_system_information(filename)

f1 = casperfpga.CasperFpga(hosts[1])
f1.get_system_information(filename)

f2 = casperfpga.CasperFpga(hosts[2])
f2.get_system_information(filename)

f3 = casperfpga.CasperFpga(hosts[3])
f3.get_system_information(filename)

# Read FFT offset calculations for each Skarab
print ' ' 
print 'Check FDFS values' 
print '-----------------' 
print ' ' 
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
#compare_all.adc_SS_data_compare(f0,f1,f2,f3)
#compare_all.pfbin_SS_data_compare(f0,f1,f2,f3)
compare_all.mix_SS_data_compare(f0,f1,f2,f3)
compare_all.ddc_SS_data_compare(f0,f1,f2,f3)
#compare_all.fir_SS_data_compare(f0,f1,f2,f3)
#compare_all.fft_SS_data_compare(f0,f1,f2,f3)
#compare_all.nb_sync_SS_data_compare(f0,f1,f2,f3)
#compare_all.quant_SS_data_compare(f0,f1,f2,f3)

# Get Sync Counts
print ' ' 
print 'Grab Sync Counts'
print '-----------------' 
print 'cd_status0:', f0.registers.cd_status.read()
print 'cd_status1:', f1.registers.cd_status.read()
print 'cd_status2:', f2.registers.cd_status.read()
print 'cd_status3:', f3.registers.cd_status.read()
print '***'
print ''

print 'mix_sync_cnt0:', f0.registers.DDC_mix_sync_cnt.read()
print 'mix_sync_cnt1:', f1.registers.DDC_mix_sync_cnt.read()
print 'mix_sync_cnt2:', f2.registers.DDC_mix_sync_cnt.read()
print 'mix_sync_cnt3:', f3.registers.DDC_mix_sync_cnt.read()
print '***'
print ''

print 'mix_sync_cnt0:', f0.registers.DDC_ddc_sync_cnt.read()
print 'mix_sync_cnt1:', f1.registers.DDC_ddc_sync_cnt.read()
print 'mix_sync_cnt2:', f2.registers.DDC_ddc_sync_cnt.read()
print 'mix_sync_cnt3:', f3.registers.DDC_ddc_sync_cnt.read()
print '***'
print ''

print 'ddc_status0:', f0.registers.ddc_status.read()
print 'ddc_status1:', f1.registers.ddc_status.read()
print 'ddc_status2:', f2.registers.ddc_status.read()
print 'ddc_status3:', f3.registers.ddc_status.read()
print '***'
print ''

print 'fir_sync_cnt0:', f0.registers.nb_pfb_fir_sync_cnt.read()
print 'fir_sync_cnt1:', f1.registers.nb_pfb_fir_sync_cnt.read()
print 'fir_sync_cnt2:', f2.registers.nb_pfb_fir_sync_cnt.read()
print 'fir_sync_cnt3:', f3.registers.nb_pfb_fir_sync_cnt.read()
print '***'
print ''

print 'fft_sync_cnt0:', f0.registers.nb_pfb_fft_sync_cnt.read()
print 'fft_sync_cnt1:', f1.registers.nb_pfb_fft_sync_cnt.read()
print 'fft_sync_cnt2:', f2.registers.nb_pfb_fft_sync_cnt.read()
print 'fft_sync_cnt3:', f3.registers.nb_pfb_fft_sync_cnt.read()
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

plt.show()

