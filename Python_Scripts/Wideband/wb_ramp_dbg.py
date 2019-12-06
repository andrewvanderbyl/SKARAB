import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

time.sleep(0.2)
sample_len = 16384

tl_cd0_bp = False
hmc_bp = False
cd_bypass = False

ramp_tvg_en = True;
snapshot_trig_src = True;
snapshot_single_trig = True;

tvg_state = False
tvg_offset = 0
tvg_amp = 1

# For file generation
build_ver =  '2018_'
adc_filename = 'adc_'
cd_filename = 'cd_' 
coeff_filename = 'coeff_'
fir_int_filename = 'fir_int_'
fir_filename = 'fir_'   
fftbp_core_s3_filename = 'fftbp_core_s3_'
fftbp_core_filename = 'fftbp_core_'
fftbp_unscr_ro_filename = 'fftbp_unscr_ro_'
fftbp_unscr_logic_filename = 'fftbp_unscr_logic_'
fftbp_unscr_hilin_filename = 'fftbp_unscr_hilin_'
fftbp_unscr_hilint_filename = 'fftbp_unscr_hilint_'
fftbp_unscr_hilint_conv_filename = 'fftbp_unscr_hilint_conv_'
fftbp_unscr_hil_upper_filename = 'fftbp_unscr_hil_upper'
fftbp_unscr_hil_lower_filename = 'fftbp_unscr_hil_lower'
fftbp_unscr_hil_buf_filename = 'fftbp_unscr_hil_buf_'
fftbp_unscr_hil_filename = 'fftbp_unscr_hil_'
fftbp_filename = 'fftbp_'
fftdir_filename = 'fftdir_'
fft_filename = 'fft_'

adc0_f0 = []
adc0_f1 = []
adc0_f2 = []
adc0_f3 = []

cd_f0 = []
cd_f1 = []
cd_f2 = []
cd_f3 = []

coeff_f0 = []
coeff_f1 = []
coeff_f2 = []
coeff_f3 = []

fir_int_f0 = []
fir_int_f1 = []
fir_int_f2 = []
fir_int_f3 = []

fir_f0 = []
fir_f1 = []
fir_f2 = []
fir_f3 = []

fftbp_core_cmplx_f0 = []
fftbp_core_cmplx_f1 = []
fftbp_core_cmplx_f2 = []
fftbp_core_cmplx_f3 = []

fftbp_core_s3_cmplx_f0 = []
fftbp_core_s3_cmplx_f1 = []
fftbp_core_s3_cmplx_f2 = []
fftbp_core_s3_cmplx_f3 = []

fftbp_cmplx_f0 = []
fftbp_cmplx_f1 = []
fftbp_cmplx_f2 = []
fftbp_cmplx_f3 = []

fftdir_cmplx_f0 = []
fftdir_cmplx_f1 = []
fftdir_cmplx_f2 = []
fftdir_cmplx_f3 = []

fft_complx_f0 = []
fft_complx_f1 = []
fft_complx_f2 = []
fft_complx_f3 = []



#==============================================================================
#   Classes and methods
#==============================================================================
class skarab: 
        
    def program_fpga(self, f):
        print 'Program FPGA' 
        f.upload_to_ram_and_program(filename)
        f.get_system_information(filename)   
        
    def board_ss_diff(self, ss1, ss2):

        diff = False
        
        print 'SS1 length is ', len(ss1)
        print 'SS2 length is ', len(ss2)
        
        for x in range(len(ss1)):
            if (ss1[x]-ss2[x] != 0):
                print x
                diff = True

        if (diff):
            print 'SS Diff NOT zero'
            print ' '
        else:
            print 'SS are Identical'          
            print ' '

    def adc_diff(self):
        print ' ' 
        print 'Grabbing ADC In'  
        
        # -- FHost 0
        fhost_num = 0
        adc0_snap = f0.snapshots.snap_adc0_ss.read(arm=False)['data'] 
        
        adc0_d0 = adc0_snap['p0_d0']
        adc0_d1 = adc0_snap['p0_d1']
        adc0_d2 = adc0_snap['p0_d2']
        adc0_d3 = adc0_snap['p0_d3']
        adc0_d4 = adc0_snap['p0_d4']
        adc0_d5 = adc0_snap['p0_d5']
        adc0_d6 = adc0_snap['p0_d6']
        adc0_d7 = adc0_snap['p0_d7']
                   
        adc0_f0 = []
                                       
        for x in range(0, len(adc0_d0)):
            adc0_f0.extend(
                [adc0_d0[x], adc0_d1[x], adc0_d2[x], adc0_d3[x], adc0_d4[x], adc0_d5[x], adc0_d6[x], adc0_d7[x]])
        
        print len(adc0_f0)
        
        filename = adc_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in adc0_f0:
                filehandle.write('%s\n' % listitem)
        
            
        # -- FHost 1
        fhost_num = 1
        adc0_snap = f1.snapshots.snap_adc0_ss.read(arm=False)['data'] 
        
        adc0_d0 = adc0_snap['p0_d0']
        adc0_d1 = adc0_snap['p0_d1']
        adc0_d2 = adc0_snap['p0_d2']
        adc0_d3 = adc0_snap['p0_d3']
        adc0_d4 = adc0_snap['p0_d4']
        adc0_d5 = adc0_snap['p0_d5']
        adc0_d6 = adc0_snap['p0_d6']
        adc0_d7 = adc0_snap['p0_d7']
                   
        adc0_f1 = []
                                       
        for x in range(0, len(adc0_d0)):
            adc0_f1.extend(
                [adc0_d0[x], adc0_d1[x], adc0_d2[x], adc0_d3[x], adc0_d4[x], adc0_d5[x], adc0_d6[x], adc0_d7[x]])
        
        print len(adc0_f1)
        
        filename = adc_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in adc0_f1:
                filehandle.write('%s\n' % listitem)
            
            
        # -- FHost 2
        fhost_num = 2
        adc0_snap = f2.snapshots.snap_adc0_ss.read(arm=False)['data'] 
        
        adc0_d0 = adc0_snap['p0_d0']
        adc0_d1 = adc0_snap['p0_d1']
        adc0_d2 = adc0_snap['p0_d2']
        adc0_d3 = adc0_snap['p0_d3']
        adc0_d4 = adc0_snap['p0_d4']
        adc0_d5 = adc0_snap['p0_d5']
        adc0_d6 = adc0_snap['p0_d6']
        adc0_d7 = adc0_snap['p0_d7']
                   
        adc0_f2 = []
                                       
        for x in range(0, len(adc0_d0)):
            adc0_f2.extend(
                [adc0_d0[x], adc0_d1[x], adc0_d2[x], adc0_d3[x], adc0_d4[x], adc0_d5[x], adc0_d6[x], adc0_d7[x]])
        
        print len(adc0_f2)
        
        filename = adc_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in adc0_f2:
                filehandle.write('%s\n' % listitem)    
            
            
        # -- FHost 3
        fhost_num = 3
        adc0_snap = f3.snapshots.snap_adc0_ss.read(arm=False)['data'] 
        
        adc0_d0 = adc0_snap['p0_d0']
        adc0_d1 = adc0_snap['p0_d1']
        adc0_d2 = adc0_snap['p0_d2']
        adc0_d3 = adc0_snap['p0_d3']
        adc0_d4 = adc0_snap['p0_d4']
        adc0_d5 = adc0_snap['p0_d5']
        adc0_d6 = adc0_snap['p0_d6']
        adc0_d7 = adc0_snap['p0_d7']
                   
        adc0_f3 = []
                                       
        for x in range(0, len(adc0_d0)):
            adc0_f3.extend(
                [adc0_d0[x], adc0_d1[x], adc0_d2[x], adc0_d3[x], adc0_d4[x], adc0_d5[x], adc0_d6[x], adc0_d7[x]])
        
        print len(adc0_f3)
        
        filename = adc_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in adc0_f3:
                filehandle.write('%s\n' % listitem)   
        
        # ADC Diff
        print '------------- *** ADC Diff ***  -------------'
        print 'ADC Diff 0-1'
        d.board_ss_diff(adc0_f0,adc0_f1)
        print 'ADC Diff 0-2'
        d.board_ss_diff(adc0_f0,adc0_f2)
        print 'ADC Diff 0-3'
        d.board_ss_diff(adc0_f0,adc0_f3)
        print 'ADC Diff 1-2'
        d.board_ss_diff(adc0_f1,adc0_f2)
        print 'ADC Diff 1-3'
        d.board_ss_diff(adc0_f1,adc0_f3)
        print 'ADC Diff 2-3'
        d.board_ss_diff(adc0_f2,adc0_f3)

# ---------------------------------------------------------------------------------------------------------------------------------        
        
    def cd_diff(self):
        print ' ' 
        print 'Grabbing CD SS'    
        
        # -- FHost 0
        fhost_num = 0  
        #cd_snap = f0.snapshots.snap_cd_out_ss.read['data']
        cd_snap = f0.snapshots.snap_cd_out_ss.read(arm=False)['data']
        
        d0 = cd_snap['d0']
        d1 = cd_snap['d1']
        d2 = cd_snap['d2']
        d3 = cd_snap['d3']
        d4 = cd_snap['d4']
        d5 = cd_snap['d5']
        d6 = cd_snap['d6']
        d7 = cd_snap['d7']
        cd_sync = cd_snap['sync']
        cd_dv = cd_snap['dv']
                   
        cd_f0 = []
                                       
        for x in range(0, len(d0)):
            cd_f0.extend(
                [d0[x], d1[x], d2[x], d3[x], d4[x], d5[x], d6[x], d7[x]])    
        
        print len(cd_f0)
        
        filename = cd_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in cd_f0:
                filehandle.write('%s\n' % listitem)   
        
        
        
        #with open('f0_cd0.txt', 'w') as filehandle:
        #    for listitem in d0:
        #        filehandle.write('%s\n' % listitem)   
        #
        #with open('f0_cd_sync.txt', 'w') as filehandle:
        #    for listitem in cd_sync:
        #        filehandle.write('%s\n' % listitem)   
        #
        #with open('f0_cd_dv.txt', 'w') as filehandle:
        #    for listitem in cd_dv:
        #        filehandle.write('%s\n' % listitem)   
        
        
        
        #cd_data = cd_out[1:sample_len]
        #fft_cd_out = np.fft.fft(cd_data)
        
        # -- FHost 1
        fhost_num = 1  
        cd_snap = f1.snapshots.snap_cd_out_ss.read(arm=False)['data']
        
        d0 = cd_snap['d0']
        d1 = cd_snap['d1']
        d2 = cd_snap['d2']
        d3 = cd_snap['d3']
        d4 = cd_snap['d4']
        d5 = cd_snap['d5']
        d6 = cd_snap['d6']
        d7 = cd_snap['d7']
                   
        cd_f1 = []
                                       
        for x in range(0, len(d0)):
            cd_f1.extend(
                [d0[x], d1[x], d2[x], d3[x], d4[x], d5[x], d6[x], d7[x]])    
        
        print len(cd_f1)
        
        filename = cd_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in cd_f1:
                filehandle.write('%s\n' % listitem)   
        
        
        # -- FHost 2
        fhost_num = 2  
        cd_snap = f2.snapshots.snap_cd_out_ss.read(arm=False)['data']
        
        d0 = cd_snap['d0']
        d1 = cd_snap['d1']
        d2 = cd_snap['d2']
        d3 = cd_snap['d3']
        d4 = cd_snap['d4']
        d5 = cd_snap['d5']
        d6 = cd_snap['d6']
        d7 = cd_snap['d7']
                   
        cd_f2 = []
                                       
        for x in range(0, len(d0)):
            cd_f2.extend(
                [d0[x], d1[x], d2[x], d3[x], d4[x], d5[x], d6[x], d7[x]])    
        
        print len(cd_f2)
        
        filename = cd_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in cd_f2:
                filehandle.write('%s\n' % listitem)   
        
        
        # -- FHost 3
        fhost_num = 3  
        cd_snap = f3.snapshots.snap_cd_out_ss.read(arm=False)['data']
        
        d0 = cd_snap['d0']
        d1 = cd_snap['d1']
        d2 = cd_snap['d2']
        d3 = cd_snap['d3']
        d4 = cd_snap['d4']
        d5 = cd_snap['d5']
        d6 = cd_snap['d6']
        d7 = cd_snap['d7']
                   
        cd_f3 = []
                                       
        for x in range(0, len(d0)):
            cd_f3.extend(
                [d0[x], d1[x], d2[x], d3[x], d4[x], d5[x], d6[x], d7[x]])    
        
        print len(cd_f3)
        
        filename = cd_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in cd_f3:
                filehandle.write('%s\n' % listitem)  
                
        print '------------- *** CD Diff ***  -------------'
        print 'CD Diff 0-1'
        d.board_ss_diff(cd_f0,cd_f1)
        print 'CD Diff 0-2'
        d.board_ss_diff(cd_f0,cd_f2)
        print 'CD Diff 0-3'
        d.board_ss_diff(cd_f0,cd_f3)
        print 'CD Diff 1-2'
        d.board_ss_diff(cd_f1,cd_f2)
        print 'CD Diff 1-3'
        d.board_ss_diff(cd_f1,cd_f3)
        print 'CD Diff 2-3'
        d.board_ss_diff(cd_f2,cd_f3)

# ---------------------------------------------------------------------------------------------------------------------------------        
 

    def fir_coeff_diff(self):       
        print ' ' 
        print 'Grabbing Coeff SS'  
        
         # -- FHost 0
        fhost_num = 0  
        coeff_snap = f0.snapshots.pfb_pfb_fir_generic_snap_coeff_ss.read(arm=False)['data'] 
        coeff_snap1 = f0.snapshots.pfb_pfb_fir_generic_snap_coeff1_ss.read(arm=False)['data'] 
        
        C0 = coeff_snap['c0']  
        C1 = coeff_snap['c1']
        C2 = coeff_snap['c2']
        C3 = coeff_snap['c3']
        C4 = coeff_snap['c4']
        C5 = coeff_snap['c5']
        C6 = coeff_snap['c6']
        
        C7 = coeff_snap1['c7']
        C8 = coeff_snap1['c8']
        C9 = coeff_snap1['c9']
        C10 = coeff_snap1['c10']
        C11 = coeff_snap1['c11']
        C12 = coeff_snap1['c12']
        C13 = coeff_snap1['c13']
                   
        coeff_f0 = []
                                       
        for x in range(0, len(C0)):
            coeff_f0.extend(
                [C0[x], C1[x], C2[x], C3[x], C4[x], C5[x], C6[x], C7[x], C8[x], C9[x], C10[x], C11[x], C12[x], C13[x]])    
        
        print len(coeff_f0)
        
        filename = coeff_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in coeff_f0:
                filehandle.write('%s\n' % listitem)        
                
                
         # -- FHost 1
        fhost_num = 1  
        coeff_snap = f1.snapshots.pfb_pfb_fir_generic_snap_coeff_ss.read(arm=False)['data'] 
        coeff_snap1 = f1.snapshots.pfb_pfb_fir_generic_snap_coeff1_ss.read(arm=False)['data'] 
        
        C0 = coeff_snap['c0']  
        C1 = coeff_snap['c1']
        C2 = coeff_snap['c2']
        C3 = coeff_snap['c3']
        C4 = coeff_snap['c4']
        C5 = coeff_snap['c5']
        C6 = coeff_snap['c6']
        
        C7 = coeff_snap1['c7']
        C8 = coeff_snap1['c8']
        C9 = coeff_snap1['c9']
        C10 = coeff_snap1['c10']
        C11 = coeff_snap1['c11']
        C12 = coeff_snap1['c12']
        C13 = coeff_snap1['c13']
                   
        coeff_f1 = []
                                       
        for x in range(0, len(C0)):
            coeff_f1.extend(
                [C0[x], C1[x], C2[x], C3[x], C4[x], C5[x], C6[x], C7[x], C8[x], C9[x], C10[x], C11[x], C12[x], C13[x]])    
        
        print len(coeff_f1)
        
        filename = coeff_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in coeff_f1:
                filehandle.write('%s\n' % listitem)           
        
        
         # -- FHost 2
        fhost_num = 2  
        coeff_snap = f2.snapshots.pfb_pfb_fir_generic_snap_coeff_ss.read(arm=False)['data'] 
        coeff_snap1 = f2.snapshots.pfb_pfb_fir_generic_snap_coeff1_ss.read(arm=False)['data'] 
        
        C0 = coeff_snap['c0']  
        C1 = coeff_snap['c1']
        C2 = coeff_snap['c2']
        C3 = coeff_snap['c3']
        C4 = coeff_snap['c4']
        C5 = coeff_snap['c5']
        C6 = coeff_snap['c6']
        
        C7 = coeff_snap1['c7']
        C8 = coeff_snap1['c8']
        C9 = coeff_snap1['c9']
        C10 = coeff_snap1['c10']
        C11 = coeff_snap1['c11']
        C12 = coeff_snap1['c12']
        C13 = coeff_snap1['c13']
                   
        coeff_f2 = []
                                       
        for x in range(0, len(C0)):
            coeff_f2.extend(
                [C0[x], C1[x], C2[x], C3[x], C4[x], C5[x], C6[x], C7[x], C8[x], C9[x], C10[x], C11[x], C12[x], C13[x]])    
        
        print len(coeff_f2)
        
        filename = coeff_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in coeff_f2:
                filehandle.write('%s\n' % listitem)          
                
        
         # -- FHost 3
        fhost_num = 3
        coeff_snap = f3.snapshots.pfb_pfb_fir_generic_snap_coeff_ss.read(arm=False)['data'] 
        coeff_snap1 = f3.snapshots.pfb_pfb_fir_generic_snap_coeff1_ss.read(arm=False)['data'] 
        
        C0 = coeff_snap['c0']  
        C1 = coeff_snap['c1']
        C2 = coeff_snap['c2']
        C3 = coeff_snap['c3']
        C4 = coeff_snap['c4']
        C5 = coeff_snap['c5']
        C6 = coeff_snap['c6']
        
        C7 = coeff_snap1['c7']
        C8 = coeff_snap1['c8']
        C9 = coeff_snap1['c9']
        C10 = coeff_snap1['c10']
        C11 = coeff_snap1['c11']
        C12 = coeff_snap1['c12']
        C13 = coeff_snap1['c13']
                   
        coeff_f3 = []
                                       
        for x in range(0, len(C0)):
            coeff_f3.extend(
                [C0[x], C1[x], C2[x], C3[x], C4[x], C5[x], C6[x], C7[x], C8[x], C9[x], C10[x], C11[x], C12[x], C13[x]])    
        
        print len(coeff_f3)
        
        filename = coeff_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in coeff_f3:
                filehandle.write('%s\n' % listitem) 
        
        # FIR Coeff Diff
        print '------------- *** FIR Coeff Diff ***  -------------'
        print 'FIR Coeff Diff 0-1'
        d.board_ss_diff(coeff_f0,coeff_f1)
        print 'FIR Coeff Diff 0-2'
        d.board_ss_diff(coeff_f0,coeff_f2)
        print 'FIR Coeff Diff 0-3'
        d.board_ss_diff(coeff_f0,coeff_f3)
        print 'FIR Coeff Diff 1-2'
        d.board_ss_diff(coeff_f1,coeff_f2)
        print 'FIR Coeff Diff 1-3'
        d.board_ss_diff(coeff_f1,coeff_f3)
        print 'FIR Coeff Diff 2-3'
        d.board_ss_diff(coeff_f2,coeff_f3)
                
# ---------------------------------------------------------------------------------------------------------------------------------        
 
    
    def fir_int_diff(self):
        print ' ' 
        print 'Grabbing FIR Int SS'  
               
        # -- FHost 0
        fhost_num = 0  
        #fir_snap = f0.snapshots.pfb_snap_fir_out_ss.read()['data'] 
        fir_snap = f0.snapshots.pfb_pfb_fir_generic_snap_fir_out_ss.read(arm=False)['data'] 
        fir_snap1 = f0.snapshots.pfb_pfb_fir_generic_snap_fir_out1_ss.read(arm=False)['data'] 
        
        fird0 = fir_snap['real0']  #NOTE: Label issue on SS - should not be real0, imag0 etc.
        fird1 = fir_snap['imag0']
        fird2 = fir_snap['real1']
        fird3 = fir_snap['imag1']
        
        fird4 = fir_snap1['real2']
        fird5 = fir_snap1['imag2']
        fird6 = fir_snap1['real3']
        fird7 = fir_snap1['imag3']
                   
        fir_int_f0 = []
                                       
        for x in range(0, len(fird0)):
            fir_int_f0.extend(
                [fird0[x], fird1[x], fird2[x], fird3[x], fird4[x], fird5[x], fird6[x], fird7[x]])    
        
        print len(fir_int_f0)
        
        #with open('fir_2018_0.txt', 'w') as filehandle:
        #    for listitem in fir_int_f0:
        #        filehandle.write('%s\n' % listitem)
                
        filename = fir_int_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fir_int_f0:
                filehandle.write('%s\n' % listitem)   
        
        #fir_data = fir_out[1:sample_len]
        #fft_fir_out = np.fft.fft(fir_data)
        
        # -- FHost 1
        fhost_num = 1 
        fir_snap = f1.snapshots.pfb_pfb_fir_generic_snap_fir_out_ss.read(arm=False)['data'] 
        fir_snap1 = f1.snapshots.pfb_pfb_fir_generic_snap_fir_out1_ss.read(arm=False)['data'] 
        
        fird0 = fir_snap['real0']  #NOTE: Label issue on SS - should not be real0, imag0 etc.
        fird1 = fir_snap['imag0']
        fird2 = fir_snap['real1']
        fird3 = fir_snap['imag1']
        
        fird4 = fir_snap1['real2']
        fird5 = fir_snap1['imag2']
        fird6 = fir_snap1['real3']
        fird7 = fir_snap1['imag3']
                   
        fir_int_f1 = []
                                       
        for x in range(0, len(fird0)):
            fir_int_f1.extend(
                [fird0[x], fird1[x], fird2[x], fird3[x], fird4[x], fird5[x], fird6[x], fird7[x]])    
        
        print len(fir_int_f1)
        
        #with open('fir_2018_1.txt', 'w') as filehandle:
        #    for listitem in fir_int_f1:
        #        filehandle.write('%s\n' % listitem)
        
        filename = fir_int_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fir_int_f1:
                filehandle.write('%s\n' % listitem)   
        
        # -- FHost 2
        fhost_num = 2  
        fir_snap = f2.snapshots.pfb_pfb_fir_generic_snap_fir_out_ss.read(arm=False)['data'] 
        fir_snap1 = f2.snapshots.pfb_pfb_fir_generic_snap_fir_out1_ss.read(arm=False)['data'] 
        
        fird0 = fir_snap['real0']  #NOTE: Label issue on SS - should not be real0, imag0 etc.
        fird1 = fir_snap['imag0']
        fird2 = fir_snap['real1']
        fird3 = fir_snap['imag1']
        
        fird4 = fir_snap1['real2']
        fird5 = fir_snap1['imag2']
        fird6 = fir_snap1['real3']
        fird7 = fir_snap1['imag3']
                   
        fir_int_f2 = []
                                       
        for x in range(0, len(fird0)):
            fir_int_f2.extend(
                [fird0[x], fird1[x], fird2[x], fird3[x], fird4[x], fird5[x], fird6[x], fird7[x]])    
        
        print len(fir_int_f2)
        
        filename = fir_int_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fir_int_f2:
                filehandle.write('%s\n' % listitem)   
        
        # -- FHost 3
        fhost_num = 3
        fir_snap = f3.snapshots.pfb_pfb_fir_generic_snap_fir_out_ss.read(arm=False)['data'] 
        fir_snap1 = f3.snapshots.pfb_pfb_fir_generic_snap_fir_out1_ss.read(arm=False)['data'] 
        
        fird0 = fir_snap['real0']  #NOTE: Label issue on SS - should not be real0, imag0 etc.
        fird1 = fir_snap['imag0']
        fird2 = fir_snap['real1']
        fird3 = fir_snap['imag1']
        
        fird4 = fir_snap1['real2']
        fird5 = fir_snap1['imag2']
        fird6 = fir_snap1['real3']
        fird7 = fir_snap1['imag3']
                   
        fir_int_f3 = []
                                       
        for x in range(0, len(fird0)):
            fir_int_f3.extend(
                [fird0[x], fird1[x], fird2[x], fird3[x], fird4[x], fird5[x], fird6[x], fird7[x]])    
        
        print len(fir_int_f3)
        
        filename = fir_int_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fir_int_f3:
                filehandle.write('%s\n' % listitem)   
                
        # FIR Int Diff
        print '-------------  *** FIR Int Diff ***  -------------'
        print 'FIR Int Diff 0-1'
        d.board_ss_diff(fir_int_f0,fir_int_f1)
        print 'FIR Int Diff 0-2'
        d.board_ss_diff(fir_int_f0,fir_int_f2)
        print 'FIR Int Diff 0-3'
        d.board_ss_diff(fir_int_f0,fir_int_f3)
        print 'FIR Int Diff 1-2'
        d.board_ss_diff(fir_int_f1,fir_int_f2)
        print 'FIR Int Diff 1-3'
        d.board_ss_diff(fir_int_f1,fir_int_f3)
        print 'FIR Int Diff 2-3'
        d.board_ss_diff(fir_int_f2,fir_int_f3)
        
        
        
        

    def fir_diff(self):
        print ' ' 
        print 'Grabbing FIR SS'  
               
        # -- FHost 0
        fhost_num = 0  
        #fir_snap = f0.snapshots.pfb_snap_fir_out_ss.read()['data'] 
        fir_snap = f0.snapshots.pfb_snap_fir_out_ss.read(arm=False)['data'] 
        fir_snap1 = f0.snapshots.pfb_snap_fir_out1_ss.read(arm=False)['data'] 
        
        fird0 = fir_snap['i0']
        fird1 = fir_snap['i1']
        fird2 = fir_snap['i2']
        fird3 = fir_snap['i3']
        
        fird4 = fir_snap1['i4']
        fird5 = fir_snap1['i5']
        fird6 = fir_snap1['i6']
        fird7 = fir_snap1['i7']
                   
        fir_f0 = []
                                       
        for x in range(0, len(fird0)):
            fir_f0.extend(
                [fird0[x], fird1[x], fird2[x], fird3[x], fird4[x], fird5[x], fird6[x], fird7[x]])    
        
        print len(fir_f0)
        
        #with open('fir_2018_0.txt', 'w') as filehandle:
        #    for listitem in fir_f0:
        #        filehandle.write('%s\n' % listitem)
                
        filename = fir_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fir_f0:
                filehandle.write('%s\n' % listitem)   
        
        #fir_data = fir_out[1:sample_len]
        #fft_fir_out = np.fft.fft(fir_data)
        
        # -- FHost 1
        fhost_num = 1 
        fir_snap = f1.snapshots.pfb_snap_fir_out_ss.read(arm=False)['data'] 
        fir_snap1 = f1.snapshots.pfb_snap_fir_out1_ss.read(arm=False)['data'] 
        
        fird0 = fir_snap['i0']
        fird1 = fir_snap['i1']
        fird2 = fir_snap['i2']
        fird3 = fir_snap['i3']
        
        fird4 = fir_snap1['i4']
        fird5 = fir_snap1['i5']
        fird6 = fir_snap1['i6']
        fird7 = fir_snap1['i7']
                   
        fir_f1 = []
                                       
        for x in range(0, len(fird0)):
            fir_f1.extend(
                [fird0[x], fird1[x], fird2[x], fird3[x], fird4[x], fird5[x], fird6[x], fird7[x]])    
        
        print len(fir_f1)
        
        #with open('fir_2018_1.txt', 'w') as filehandle:
        #    for listitem in fir_f1:
        #        filehandle.write('%s\n' % listitem)
        
        filename = fir_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fir_f1:
                filehandle.write('%s\n' % listitem)   
        
        # -- FHost 2
        fhost_num = 2  
        fir_snap = f2.snapshots.pfb_snap_fir_out_ss.read(arm=False)['data'] 
        fir_snap1 = f2.snapshots.pfb_snap_fir_out1_ss.read(arm=False)['data'] 
        
        fird0 = fir_snap['i0']
        fird1 = fir_snap['i1']
        fird2 = fir_snap['i2']
        fird3 = fir_snap['i3']
        
        fird4 = fir_snap1['i4']
        fird5 = fir_snap1['i5']
        fird6 = fir_snap1['i6']
        fird7 = fir_snap1['i7']
                   
        fir_f2 = []
                                       
        for x in range(0, len(fird0)):
            fir_f2.extend(
                [fird0[x], fird1[x], fird2[x], fird3[x], fird4[x], fird5[x], fird6[x], fird7[x]])    
        
        print len(fir_f2)
        
        filename = fir_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fir_f2:
                filehandle.write('%s\n' % listitem)   
        
        # -- FHost 3
        fhost_num = 3
        fir_snap = f3.snapshots.pfb_snap_fir_out_ss.read(arm=False)['data'] 
        fir_snap1 = f3.snapshots.pfb_snap_fir_out1_ss.read(arm=False)['data'] 
        
        fird0 = fir_snap['i0']
        fird1 = fir_snap['i1']
        fird2 = fir_snap['i2']
        fird3 = fir_snap['i3']
        
        fird4 = fir_snap1['i4']
        fird5 = fir_snap1['i5']
        fird6 = fir_snap1['i6']
        fird7 = fir_snap1['i7']
                   
        fir_f3 = []
                                       
        for x in range(0, len(fird0)):
            fir_f3.extend(
                [fird0[x], fird1[x], fird2[x], fird3[x], fird4[x], fird5[x], fird6[x], fird7[x]])    
        
        print len(fir_f3)
        
        filename = fir_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fir_f3:
                filehandle.write('%s\n' % listitem)   
                
        # FIR Out Diff
        print '-------------  *** FIR Out Diff ***   -------------'
        print 'FIR Out Diff 0-1'
        d.board_ss_diff(fir_f0,fir_f1)
        print 'FIR Out Diff 0-2'
        d.board_ss_diff(fir_f0,fir_f2)
        print 'FIR Out Diff 0-3'
        d.board_ss_diff(fir_f0,fir_f3)
        print 'FIR Out Diff 1-2'
        d.board_ss_diff(fir_f1,fir_f2)
        print 'FIR Out Diff 1-3'
        d.board_ss_diff(fir_f1,fir_f3)
        print 'FIR Out Diff 2-3'
        d.board_ss_diff(fir_f2,fir_f3)
                
# -------------------------------------------------------------------------------------------------------------------------------       
        
    def fft_bp_core_s3_diff(self):
        print ' ' 
        print 'Grabbing FFT BP Core Stage 3 SS'   
        
        # -- FHost 0
        fhost_num = 0
       
        fftbp_core_s3_snap = f0.snapshots.pfb_fft_bi_core_s30_ss.read(arm=False)['data']
        fftbp_core_s3_snap1 = f0.snapshots.pfb_fft_bi_core_s31_ss.read(arm=False)['data']
        
        fftr0 = fftbp_core_s3_snap['real0']
        ffti0 = fftbp_core_s3_snap['imag0']
        fftr1 = fftbp_core_s3_snap['real1']
        ffti1 = fftbp_core_s3_snap['imag1']
        
        fftr2 = fftbp_core_s3_snap1['real2']
        ffti2 = fftbp_core_s3_snap1['imag2']
        fftr3 = fftbp_core_s3_snap1['real3']
        ffti3 = fftbp_core_s3_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_core_s3_cmplx_f0 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_core_s3_cmplx_f0)
        
        filename = fftbp_core_s3_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_core_s3_cmplx_f0:
                filehandle.write('%s\n' % listitem)        
                
        # -- FHost 1
        fhost_num = 1
       
        fftbp_core_s3_snap = f1.snapshots.pfb_fft_bi_core_s30_ss.read(arm=False)['data']
        fftbp_core_s3_snap1 = f1.snapshots.pfb_fft_bi_core_s31_ss.read(arm=False)['data']
        
        fftr0 = fftbp_core_s3_snap['real0']
        ffti0 = fftbp_core_s3_snap['imag0']
        fftr1 = fftbp_core_s3_snap['real1']
        ffti1 = fftbp_core_s3_snap['imag1']
        
        fftr2 = fftbp_core_s3_snap1['real2']
        ffti2 = fftbp_core_s3_snap1['imag2']
        fftr3 = fftbp_core_s3_snap1['real3']
        ffti3 = fftbp_core_s3_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_core_s3_cmplx_f1 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_core_s3_cmplx_f1)
        
        filename = fftbp_core_s3_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_core_s3_cmplx_f1:
                filehandle.write('%s\n' % listitem)  
        
        
        # -- FHost 2
        fhost_num = 2
       
        fftbp_core_s3_snap = f2.snapshots.pfb_fft_bi_core_s30_ss.read(arm=False)['data']
        fftbp_core_s3_snap1 = f2.snapshots.pfb_fft_bi_core_s31_ss.read(arm=False)['data']
        
        fftr0 = fftbp_core_s3_snap['real0']
        ffti0 = fftbp_core_s3_snap['imag0']
        fftr1 = fftbp_core_s3_snap['real1']
        ffti1 = fftbp_core_s3_snap['imag1']
        
        fftr2 = fftbp_core_s3_snap1['real2']
        ffti2 = fftbp_core_s3_snap1['imag2']
        fftr3 = fftbp_core_s3_snap1['real3']
        ffti3 = fftbp_core_s3_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_core_s3_cmplx_f2 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_core_s3_cmplx_f2)
        
        filename = fftbp_core_s3_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_core_s3_cmplx_f2:
                filehandle.write('%s\n' % listitem)          


        # -- FHost 3
        fhost_num = 3
       
        fftbp_core_s3_snap = f3.snapshots.pfb_fft_bi_core_s30_ss.read(arm=False)['data']
        fftbp_core_s3_snap1 = f3.snapshots.pfb_fft_bi_core_s31_ss.read(arm=False)['data']
        
        fftr0 = fftbp_core_s3_snap['real0']
        ffti0 = fftbp_core_s3_snap['imag0']
        fftr1 = fftbp_core_s3_snap['real1']
        ffti1 = fftbp_core_s3_snap['imag1']
        
        fftr2 = fftbp_core_s3_snap1['real2']
        ffti2 = fftbp_core_s3_snap1['imag2']
        fftr3 = fftbp_core_s3_snap1['real3']
        ffti3 = fftbp_core_s3_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_core_s3_cmplx_f3 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_core_s3_cmplx_f3)
        
        filename = fftbp_core_s3_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_core_s3_cmplx_f3:
                filehandle.write('%s\n' % listitem)  
       
        # FFT BP Core S3 Diff
        print '-------------  *** FFT BP Diff ***   -------------'
        print 'FFT BP Core S3 Diff 0-1'
        d.board_ss_diff(fftbp_core_s3_cmplx_f0,fftbp_core_s3_cmplx_f1)
        print 'FFT BP Core S3 Diff 0-2'
        d.board_ss_diff(fftbp_core_s3_cmplx_f0,fftbp_core_s3_cmplx_f2)
        print 'FFT BP Core S3 Diff 0-3'
        d.board_ss_diff(fftbp_core_s3_cmplx_f0,fftbp_core_s3_cmplx_f3)
        print 'FFT BP Core S3 Diff 1-2'
        d.board_ss_diff(fftbp_core_s3_cmplx_f1,fftbp_core_s3_cmplx_f2)
        print 'FFT BP Core S3 Diff 1-3'
        d.board_ss_diff(fftbp_core_s3_cmplx_f1,fftbp_core_s3_cmplx_f3)
        print 'FFT BP Core S3 Diff 2-3'
        d.board_ss_diff(fftbp_core_s3_cmplx_f2,fftbp_core_s3_cmplx_f3)

# -------------------------------------------------------------------------------------------------------------------------------       
        
    def fft_bp_core_diff(self):   
        print ' ' 
        print 'Grabbing FFT BP Core SS'   
        
        # -- FHost 0
        fhost_num = 0
       
        fftbp_core_snap = f0.snapshots.pfb_fft_bi_ss_bpc_ss.read(arm=False)['data']
        fftbp_core_snap1 = f0.snapshots.pfb_fft_bi_ss_bpc1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_core_snap['real0']
        ffti0 = fftbp_core_snap['imag0']
        fftr1 = fftbp_core_snap['real1']
        ffti1 = fftbp_core_snap['imag1']
        
        fftr2 = fftbp_core_snap1['real2']
        ffti2 = fftbp_core_snap1['imag2']
        fftr3 = fftbp_core_snap1['real3']
        ffti3 = fftbp_core_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_core_cmplx_f0 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_core_cmplx_f0)
        
        filename = fftbp_core_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_core_cmplx_f0:
                filehandle.write('%s\n' % listitem) 
        
        
        # -- FHost 1
        fhost_num = 1
       
        fftbp_core_snap = f1.snapshots.pfb_fft_bi_ss_bpc_ss.read(arm=False)['data']
        fftbp_core_snap1 = f1.snapshots.pfb_fft_bi_ss_bpc1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_core_snap['real0']
        ffti0 = fftbp_core_snap['imag0']
        fftr1 = fftbp_core_snap['real1']
        ffti1 = fftbp_core_snap['imag1']
        
        fftr2 = fftbp_core_snap1['real2']
        ffti2 = fftbp_core_snap1['imag2']
        fftr3 = fftbp_core_snap1['real3']
        ffti3 = fftbp_core_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_core_cmplx_f1 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_core_cmplx_f1)
        
        filename = fftbp_core_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_core_cmplx_f1:
                filehandle.write('%s\n' % listitem)         
 
    
        # -- FHost 2
        fhost_num = 2
       
        fftbp_core_snap = f2.snapshots.pfb_fft_bi_ss_bpc_ss.read(arm=False)['data']
        fftbp_core_snap1 = f2.snapshots.pfb_fft_bi_ss_bpc1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_core_snap['real0']
        ffti0 = fftbp_core_snap['imag0']
        fftr1 = fftbp_core_snap['real1']
        ffti1 = fftbp_core_snap['imag1']
        
        fftr2 = fftbp_core_snap1['real2']
        ffti2 = fftbp_core_snap1['imag2']
        fftr3 = fftbp_core_snap1['real3']
        ffti3 = fftbp_core_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_core_cmplx_f2 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_core_cmplx_f2)
        
        filename = fftbp_core_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_core_cmplx_f2:
                filehandle.write('%s\n' % listitem)      
    
    
        # -- FHost 3
        fhost_num = 3
       
        fftbp_core_snap = f3.snapshots.pfb_fft_bi_ss_bpc_ss.read(arm=False)['data']
        fftbp_core_snap1 = f3.snapshots.pfb_fft_bi_ss_bpc1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_core_snap['real0']
        ffti0 = fftbp_core_snap['imag0']
        fftr1 = fftbp_core_snap['real1']
        ffti1 = fftbp_core_snap['imag1']
        
        fftr2 = fftbp_core_snap1['real2']
        ffti2 = fftbp_core_snap1['imag2']
        fftr3 = fftbp_core_snap1['real3']
        ffti3 = fftbp_core_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_core_cmplx_f3 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_core_cmplx_f3)
        
        filename = fftbp_core_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_core_cmplx_f3:
                filehandle.write('%s\n' % listitem)    
    
    

        # FFT BP Core Diff
        print '-------------  *** FFT BP Diff ***   -------------'
        print 'FFT BP Core Diff 0-1'
        d.board_ss_diff(fftbp_core_cmplx_f0,fftbp_core_cmplx_f1)
        print 'FFT BP Core Diff 0-2'
        d.board_ss_diff(fftbp_core_cmplx_f0,fftbp_core_cmplx_f2)
        print 'FFT BP Core Diff 0-3'
        d.board_ss_diff(fftbp_core_cmplx_f0,fftbp_core_cmplx_f3)
        print 'FFT BP Core Diff 1-2'
        d.board_ss_diff(fftbp_core_cmplx_f1,fftbp_core_cmplx_f2)
        print 'FFT BP Core Diff 1-3'
        d.board_ss_diff(fftbp_core_cmplx_f1,fftbp_core_cmplx_f3)
        print 'FFT BP Core Diff 2-3'
        d.board_ss_diff(fftbp_core_cmplx_f2,fftbp_core_cmplx_f3)
        
        
# -------------------------------------------------------------------------------------------------------------------------------       

    def fft_bp_unscramble_ro_diff(self):   
        print ' ' 
        print 'Grabbing FFT BP Unscramble Reorder SS'   
        
        #f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro_ss.print_snap()
        
        # -- FHost 0
        fhost_num = 0
       
        fftbp_unscr_ro_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap1 = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_ro_snap['real0']
        ffti0 = fftbp_unscr_ro_snap['imag0']
        fftr1 = fftbp_unscr_ro_snap['real1']
        ffti1 = fftbp_unscr_ro_snap['imag1']
        ro_sync = fftbp_unscr_ro_snap['sync']
        ro_dv = fftbp_unscr_ro_snap['dv']
        
        fftr2 = fftbp_unscr_ro_snap1['real2']
        ffti2 = fftbp_unscr_ro_snap1['imag2']
        fftr3 = fftbp_unscr_ro_snap1['real3']
        ffti3 = fftbp_unscr_ro_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_ro_cmplx_f0 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_ro_cmplx_f0)
        
        filename = fftbp_unscr_ro_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_ro_cmplx_f0:
                filehandle.write('%s\n' % listitem) 
        
        
        # Extra file write debug
        filename = fftbp_unscr_ro_filename + '_sync_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in ro_sync:
                filehandle.write('%s\n' % listitem)                 
                
        filename = fftbp_unscr_ro_filename + '_dv_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in ro_dv:
                filehandle.write('%s\n' % listitem)                   
                
        filename = fftbp_unscr_ro_filename + '_fftr0_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr0:
                filehandle.write('%s\n' % listitem)     
            
        
          # -- FHost 1
        fhost_num = 1
       
        fftbp_unscr_ro_snap = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap1 = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_ro_snap['real0']
        ffti0 = fftbp_unscr_ro_snap['imag0']
        fftr1 = fftbp_unscr_ro_snap['real1']
        ffti1 = fftbp_unscr_ro_snap['imag1']
        
        fftr2 = fftbp_unscr_ro_snap1['real2']
        ffti2 = fftbp_unscr_ro_snap1['imag2']
        fftr3 = fftbp_unscr_ro_snap1['real3']
        ffti3 = fftbp_unscr_ro_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_ro_cmplx_f1 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_ro_cmplx_f1)
        
        filename = fftbp_unscr_ro_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_ro_cmplx_f1:
                filehandle.write('%s\n' % listitem)    
    

          # -- FHost 2
        fhost_num = 2
       
        fftbp_unscr_ro_snap = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap1 = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_ro_snap['real0']
        ffti0 = fftbp_unscr_ro_snap['imag0']
        fftr1 = fftbp_unscr_ro_snap['real1']
        ffti1 = fftbp_unscr_ro_snap['imag1']
        
        fftr2 = fftbp_unscr_ro_snap1['real2']
        ffti2 = fftbp_unscr_ro_snap1['imag2']
        fftr3 = fftbp_unscr_ro_snap1['real3']
        ffti3 = fftbp_unscr_ro_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_ro_cmplx_f2 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_ro_cmplx_f2)
        
        filename = fftbp_unscr_ro_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_ro_cmplx_f2:
                filehandle.write('%s\n' % listitem)  

        # -- FHost 3
        fhost_num = 3
       
        fftbp_unscr_ro_snap = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap1 = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_ro_snap['real0']
        ffti0 = fftbp_unscr_ro_snap['imag0']
        fftr1 = fftbp_unscr_ro_snap['real1']
        ffti1 = fftbp_unscr_ro_snap['imag1']
        
        fftr2 = fftbp_unscr_ro_snap1['real2']
        ffti2 = fftbp_unscr_ro_snap1['imag2']
        fftr3 = fftbp_unscr_ro_snap1['real3']
        ffti3 = fftbp_unscr_ro_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_ro_cmplx_f3 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_ro_cmplx_f3)
        
        filename = fftbp_unscr_ro_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_ro_cmplx_f3:
                filehandle.write('%s\n' % listitem) 

        # FFT BP Uncramble Reorder Diff
        print '-------------  *** FFT BP Unscramble Reorder Diff ***   -------------'
        print 'FFT BP Unscramble Reorder Diff 0-1'
        d.board_ss_diff(fftbp_unscr_ro_cmplx_f0,fftbp_unscr_ro_cmplx_f1)
        print 'FFT BP Unscramble Reorder Diff 0-2'
        d.board_ss_diff(fftbp_unscr_ro_cmplx_f0,fftbp_unscr_ro_cmplx_f2)
        print 'FFT BP Unscramble Reorder Diff 0-3'
        d.board_ss_diff(fftbp_unscr_ro_cmplx_f0,fftbp_unscr_ro_cmplx_f3)
        print 'FFT BP Unscramble Reorder Diff 1-2'
        d.board_ss_diff(fftbp_unscr_ro_cmplx_f1,fftbp_unscr_ro_cmplx_f2)
        print 'FFT BP Unscramble Reorder Diff 1-3'
        d.board_ss_diff(fftbp_unscr_ro_cmplx_f1,fftbp_unscr_ro_cmplx_f3)
        print 'FFT BP Unscramble Reorder Diff 2-3'
        d.board_ss_diff(fftbp_unscr_ro_cmplx_f2,fftbp_unscr_ro_cmplx_f3)
        
        
        
# -------------------------------------------------------------------------------------------------------------------------------       

    def fft_bp_unscramble_logic_diff(self):   
        print ' ' 
        print 'Grabbing FFT BP Unscramble Logic SS'   
        
        # -- FHost 0
        fhost_num = 0
       
        fftbp_unscr_logic_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint2_ss.read(arm=False)['data']
        
        logic0_rst = fftbp_unscr_logic_snap['rst']
        logic0_count = fftbp_unscr_logic_snap['count']
        logic0_rel0 = fftbp_unscr_logic_snap['rel0']
        logic0_rel1 = fftbp_unscr_logic_snap['rel1']
        logic0_sync = fftbp_unscr_logic_snap['sync']
        logic0_dv = fftbp_unscr_logic_snap['dv']        

        print len(logic0_count)
        
        filename = fftbp_unscr_logic_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in logic0_count:
                filehandle.write('%s\n' % listitem) 
            
            
        # Extra file write debug
        filename = fftbp_unscr_logic_filename + '_sync_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in logic0_sync:
                filehandle.write('%s\n' % listitem)                 
                
        filename = fftbp_unscr_logic_filename + '_dv_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in logic0_dv:
                filehandle.write('%s\n' % listitem)                   
                
        filename = fftbp_unscr_logic_filename + '_count_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in logic0_count:
                filehandle.write('%s\n' % listitem)     
            
            
        
        # -- FHost 1
        fhost_num = 1
       
        fftbp_unscr_logic_snap = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint2_ss.read(arm=False)['data']
        
        logic1_rst = fftbp_unscr_logic_snap['rst']
        logic1_count = fftbp_unscr_logic_snap['count']
        logic1_rel0 = fftbp_unscr_logic_snap['rel0']
        logic1_rel1 = fftbp_unscr_logic_snap['rel1']
        logic1_sync = fftbp_unscr_logic_snap['sync']
        logic1_dv = fftbp_unscr_logic_snap['dv']        

        print len(logic1_count)
        
        filename = fftbp_unscr_logic_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in logic1_count:
                filehandle.write('%s\n' % listitem) 
                
        
        # -- FHost 2
        fhost_num = 2
       
        fftbp_unscr_logic_snap = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint2_ss.read(arm=False)['data']
        
        logic2_rst = fftbp_unscr_logic_snap['rst']
        logic2_count = fftbp_unscr_logic_snap['count']
        logic2_rel0 = fftbp_unscr_logic_snap['rel0']
        logic2_rel1 = fftbp_unscr_logic_snap['rel1']
        logic2_sync = fftbp_unscr_logic_snap['sync']
        logic2_dv = fftbp_unscr_logic_snap['dv']        

        print len(logic2_count)
        
        filename = fftbp_unscr_logic_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in logic2_count:
                filehandle.write('%s\n' % listitem) 
                
        
        # -- FHost 3
        fhost_num = 3
       
        fftbp_unscr_logic_snap = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint2_ss.read(arm=False)['data']
        
        logic3_rst = fftbp_unscr_logic_snap['rst']
        logic3_count = fftbp_unscr_logic_snap['count']
        logic3_rel0 = fftbp_unscr_logic_snap['rel0']
        logic3_rel1 = fftbp_unscr_logic_snap['rel1']
        logic3_sync = fftbp_unscr_logic_snap['sync']
        logic3_dv = fftbp_unscr_logic_snap['dv']        

        print len(logic3_count)
        
        filename = fftbp_unscr_logic_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in logic3_count:
                filehandle.write('%s\n' % listitem) 
                
                
        # Biplex UnScramble Logic Dif
#        print '-------------  *** Biplex UnScramble Logic Diff ***   -------------'
#        print 'Biplex UnScramble Logic Diff 0-1'
#        d.board_ss_diff(logic0_count,logic1_count)
#        print 'Biplex UnScramble Logic Dif 0-2'
#        d.board_ss_diff(logic0_count,logic2_count)
#        print 'Biplex UnScramble Logic Diff 0-3'
#        d.board_ss_diff(logic0_count,logic3_count)
#        print 'FBiplex UnScramble Logic Dif 1-2'
#        d.board_ss_diff(logic1_count,logic2_count)
#        print 'Biplex UnScramble Logic Dif 1-3'
#        d.board_ss_diff(logic1_count,logic3_count)
#        print 'Biplex UnScramble Logic Diff 2-3'
#        d.board_ss_diff(logic2_count,logic3_count)
                

# -------------------------------------------------------------------------------------------------------------------------------       

    def fft_bp_unscramble_hilbert_input_diff(self):   
        print ' ' 
        print 'Grabbing FFT BP Unscramble Hilbert Input SS'   
        
        # -- FHost 0
        fhost_num = 0
       
        fftbp_unscr_hilin_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin_ss.read(arm=False)['data']
        fftbp_unscr_hilin1_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_hilin_snap['real0']
        ffti0 = fftbp_unscr_hilin_snap['imag0']
        fftr1 = fftbp_unscr_hilin_snap['real1']
        ffti1 = fftbp_unscr_hilin_snap['imag1']
        hilin_sync = fftbp_unscr_hilin_snap['sync']
        hilin_dv = fftbp_unscr_hilin_snap['dv']
        
        
        fftr2 = fftbp_unscr_hilin1_snap['real2']
        ffti2 = fftbp_unscr_hilin1_snap['imag2']
        fftr3 = fftbp_unscr_hilin1_snap['real3']
        ffti3 = fftbp_unscr_hilin1_snap['imag3']

        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hilin_cmplx_f0 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hilin_cmplx_f0)
        
        filename = fftbp_unscr_hilin_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hilin_cmplx_f0:
                filehandle.write('%s\n' % listitem) 
                
        
        # Extra file write debug
        filename = fftbp_unscr_hilin_filename + '_sync_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilin_sync:
                filehandle.write('%s\n' % listitem)                 
                
        filename = fftbp_unscr_hilin_filename + '_dv_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilin_dv:
                filehandle.write('%s\n' % listitem)                   
                
        filename = fftbp_unscr_hilin_filename + '_fftr0_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr0:
                filehandle.write('%s\n' % listitem)                   
                
                
                
                
        # -- FHost 1
        fhost_num = 1
       
        fftbp_unscr_hilin_snap = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin_ss.read(arm=False)['data']
        fftbp_unscr_hilin1_snap = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_hilin_snap['real0']
        ffti0 = fftbp_unscr_hilin_snap['imag0']
        fftr1 = fftbp_unscr_hilin_snap['real1']
        ffti1 = fftbp_unscr_hilin_snap['imag1']
        hilin_sync = fftbp_unscr_hilin_snap['sync']
        hilin_dv = fftbp_unscr_hilin_snap['dv']
        
        fftr2 = fftbp_unscr_hilin1_snap['real2']
        ffti2 = fftbp_unscr_hilin1_snap['imag2']
        fftr3 = fftbp_unscr_hilin1_snap['real3']
        ffti3 = fftbp_unscr_hilin1_snap['imag3']

        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hilin_cmplx_f1 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hilin_cmplx_f1)
        
        filename = fftbp_unscr_hilin_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hilin_cmplx_f1:
                filehandle.write('%s\n' % listitem) 
                
                
        # Extra file write debug
        filename = fftbp_unscr_hilin_filename + '_sync_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilin_sync:
                filehandle.write('%s\n' % listitem)                 
                
        filename = fftbp_unscr_hilin_filename + '_dv_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilin_dv:
                filehandle.write('%s\n' % listitem)                   
                
        filename = fftbp_unscr_hilin_filename + '_fftr0_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr0:
                filehandle.write('%s\n' % listitem)    
                
                
        # -- FHost 2
        fhost_num = 2
       
        fftbp_unscr_hilin_snap = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin_ss.read(arm=False)['data']
        fftbp_unscr_hilin1_snap = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_hilin_snap['real0']
        ffti0 = fftbp_unscr_hilin_snap['imag0']
        fftr1 = fftbp_unscr_hilin_snap['real1']
        ffti1 = fftbp_unscr_hilin_snap['imag1']
        hilin_sync = fftbp_unscr_hilin_snap['sync']
        hilin_dv = fftbp_unscr_hilin_snap['dv']
        
        fftr2 = fftbp_unscr_hilin1_snap['real2']
        ffti2 = fftbp_unscr_hilin1_snap['imag2']
        fftr3 = fftbp_unscr_hilin1_snap['real3']
        ffti3 = fftbp_unscr_hilin1_snap['imag3']

        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hilin_cmplx_f2 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hilin_cmplx_f2)
        
        filename = fftbp_unscr_hilin_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hilin_cmplx_f2:
                filehandle.write('%s\n' % listitem) 
                
                
        # Extra file write debug
        filename = fftbp_unscr_hilin_filename + '_sync_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilin_sync:
                filehandle.write('%s\n' % listitem)                 
                
        filename = fftbp_unscr_hilin_filename + '_dv_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilin_dv:
                filehandle.write('%s\n' % listitem)                   
                
        filename = fftbp_unscr_hilin_filename + '_fftr0_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr0:
                filehandle.write('%s\n' % listitem)                    

        # -- FHost 3
        fhost_num = 3
       
        fftbp_unscr_hilin_snap = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin_ss.read(arm=False)['data']
        fftbp_unscr_hilin1_snap = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_hilin_snap['real0']
        ffti0 = fftbp_unscr_hilin_snap['imag0']
        fftr1 = fftbp_unscr_hilin_snap['real1']
        ffti1 = fftbp_unscr_hilin_snap['imag1']
        hilin_sync = fftbp_unscr_hilin_snap['sync']
        hilin_dv = fftbp_unscr_hilin_snap['dv']
        
        fftr2 = fftbp_unscr_hilin1_snap['real2']
        ffti2 = fftbp_unscr_hilin1_snap['imag2']
        fftr3 = fftbp_unscr_hilin1_snap['real3']
        ffti3 = fftbp_unscr_hilin1_snap['imag3']

        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hilin_cmplx_f3 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hilin_cmplx_f3)
        
        filename = fftbp_unscr_hilin_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hilin_cmplx_f3:
                filehandle.write('%s\n' % listitem)            
                
        # Extra file write debug
        filename = fftbp_unscr_hilin_filename + '_sync_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilin_sync:
                filehandle.write('%s\n' % listitem)                 
                
        filename = fftbp_unscr_hilin_filename + '_dv_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilin_dv:
                filehandle.write('%s\n' % listitem)                   
                
        filename = fftbp_unscr_hilin_filename + '_fftr0_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr0:
                filehandle.write('%s\n' % listitem)    
                

        # FFT BP Uncramble Hilbert Diff
        print '-------------  *** FFT BP Unscramble Hilbert Input Diff ***   -------------'
        print 'FFT BP Unscramble Hilbert Input Diff 0-1'
        d.board_ss_diff(fftbp_unscr_hilin_cmplx_f0,fftbp_unscr_hilin_cmplx_f1)
        print 'FFT BP Unscramble Hilbert Input Diff 0-2'
        d.board_ss_diff(fftbp_unscr_hilin_cmplx_f0,fftbp_unscr_hilin_cmplx_f2)
        print 'FFT BP Unscramble Hilbert Input Diff 0-3'
        d.board_ss_diff(fftbp_unscr_hilin_cmplx_f0,fftbp_unscr_hilin_cmplx_f3)
        print 'FFT BP Unscramble Hilbert Input Diff 1-2'
        d.board_ss_diff(fftbp_unscr_hilin_cmplx_f1,fftbp_unscr_hilin_cmplx_f2)
        print 'FFT BP Unscramble Hilbert Input Diff 1-3'
        d.board_ss_diff(fftbp_unscr_hilin_cmplx_f1,fftbp_unscr_hilin_cmplx_f3)
        print 'FFT BP Unscramble Hilbert Input Diff 2-3'
        d.board_ss_diff(fftbp_unscr_hilin_cmplx_f2,fftbp_unscr_hilin_cmplx_f3)

# -------------------------------------------------------------------------------------------------------------------------------       

    def fft_bp_unscramble_hilbert_internal_diff(self):   
        print ' ' 
        print 'Grabbing FFT BP Unscramble Hilbert Internal SS'   
        
        # -- FHost 0
        fhost_num = 0
       
        fftbp_unscr_hilint_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint_ss.read(arm=False)['data']
        fftbp_unscr_hilint1_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_hilint_snap['real0']
        ffti0 = fftbp_unscr_hilint_snap['imag0']
        fftr1 = fftbp_unscr_hilint_snap['real1']
        ffti1 = fftbp_unscr_hilint_snap['imag1']
        hilint_sync = fftbp_unscr_hilint_snap['sync']
        hilint_dv = fftbp_unscr_hilint_snap['dv']        
        
        fftr2 = fftbp_unscr_hilint1_snap['real2']
        ffti2 = fftbp_unscr_hilint1_snap['imag2']
        fftr3 = fftbp_unscr_hilint1_snap['real3']
        ffti3 = fftbp_unscr_hilint1_snap['imag3']

        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hilint_cmplx_f0 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hilint_cmplx_f0)
        
        filename = fftbp_unscr_hilint_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hilint_cmplx_f0:
                filehandle.write('%s\n' % listitem) 
                
                
        # Extra file write debug
        filename = fftbp_unscr_hilint_filename + '_sync_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilint_sync:
                filehandle.write('%s\n' % listitem)                 
                
        filename = fftbp_unscr_hilint_filename + '_dv_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilint_dv:
                filehandle.write('%s\n' % listitem)                   
                
        filename = fftbp_unscr_hilint_filename + '_fftr0_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr0:
                filehandle.write('%s\n' % listitem)   
                
                
        # -- FHost 1
        fhost_num = 1
       
        fftbp_unscr_hilint_snap = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint_ss.read(arm=False)['data']
        fftbp_unscr_hilint1_snap = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_hilint_snap['real0']
        ffti0 = fftbp_unscr_hilint_snap['imag0']
        fftr1 = fftbp_unscr_hilint_snap['real1']
        ffti1 = fftbp_unscr_hilint_snap['imag1']
        
        fftr2 = fftbp_unscr_hilint1_snap['real2']
        ffti2 = fftbp_unscr_hilint1_snap['imag2']
        fftr3 = fftbp_unscr_hilint1_snap['real3']
        ffti3 = fftbp_unscr_hilint1_snap['imag3']

        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hilint_cmplx_f1 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hilint_cmplx_f1)
        
        filename = fftbp_unscr_hilint_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hilint_cmplx_f1:
                filehandle.write('%s\n' % listitem) 

        # -- FHost 2
        fhost_num = 2
       
        fftbp_unscr_hilint_snap = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint_ss.read(arm=False)['data']
        fftbp_unscr_hilint1_snap = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_hilint_snap['real0']
        ffti0 = fftbp_unscr_hilint_snap['imag0']
        fftr1 = fftbp_unscr_hilint_snap['real1']
        ffti1 = fftbp_unscr_hilint_snap['imag1']
        
        fftr2 = fftbp_unscr_hilint1_snap['real2']
        ffti2 = fftbp_unscr_hilint1_snap['imag2']
        fftr3 = fftbp_unscr_hilint1_snap['real3']
        ffti3 = fftbp_unscr_hilint1_snap['imag3']

        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hilint_cmplx_f2 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hilint_cmplx_f2)
        
        filename = fftbp_unscr_hilint_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hilint_cmplx_f2:
                filehandle.write('%s\n' % listitem) 


        # -- FHost 3
        fhost_num = 3
       
        fftbp_unscr_hilint_snap = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint_ss.read(arm=False)['data']
        fftbp_unscr_hilint1_snap = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_hilint_snap['real0']
        ffti0 = fftbp_unscr_hilint_snap['imag0']
        fftr1 = fftbp_unscr_hilint_snap['real1']
        ffti1 = fftbp_unscr_hilint_snap['imag1']
        
        fftr2 = fftbp_unscr_hilint1_snap['real2']
        ffti2 = fftbp_unscr_hilint1_snap['imag2']
        fftr3 = fftbp_unscr_hilint1_snap['real3']
        ffti3 = fftbp_unscr_hilint1_snap['imag3']

        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hilint_cmplx_f3 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hilint_cmplx_f3)
        
        filename = fftbp_unscr_hilint_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hilint_cmplx_f3:
                filehandle.write('%s\n' % listitem) 


        # FFT BP Uncramble Hilbert Internal Diff
        print '-------------  *** FFT BP Unscramble Hilbert Internal Diff ***   -------------'
        print 'FFT BP Unscramble Hilbert Internal Diff 0-1'
        d.board_ss_diff(fftbp_unscr_hilint_cmplx_f0,fftbp_unscr_hilint_cmplx_f1)
        print 'FFT BP Unscramble Hilbert Internal Diff 0-2'
        d.board_ss_diff(fftbp_unscr_hilint_cmplx_f0,fftbp_unscr_hilint_cmplx_f2)
        print 'FFT BP Unscramble Hilbert Internal Diff 0-3'
        d.board_ss_diff(fftbp_unscr_hilint_cmplx_f0,fftbp_unscr_hilint_cmplx_f3)
        print 'FFT BP Unscramble Hilbert Internal Diff 1-2'
        d.board_ss_diff(fftbp_unscr_hilint_cmplx_f1,fftbp_unscr_hilint_cmplx_f2)
        print 'FFT BP Unscramble Hilbert Internal Diff 1-3'
        d.board_ss_diff(fftbp_unscr_hilint_cmplx_f1,fftbp_unscr_hilint_cmplx_f3)
        print 'FFT BP Unscramble Hilbert Internal Diff 2-3'
        d.board_ss_diff(fftbp_unscr_hilint_cmplx_f2,fftbp_unscr_hilint_cmplx_f3)
        
        
        
# -------------------------------------------------------------------------------------------------------------------------------       

    def fft_bp_unscramble_hilbert_internal_convert_diff(self):   
        print ' ' 
        print 'Grabbing FFT BP Unscramble Hilbert Internal Convert SS'   
        
        # -- FHost 0
        fhost_num = 0
       
        fftbp_unscr_hilintc_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc_ss.read(arm=False)['data']
        fftbp_unscr_hilintc1_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_hilintc_snap['real0']
        ffti0 = fftbp_unscr_hilintc_snap['imag0']
        fftr1 = fftbp_unscr_hilintc_snap['real1']
        ffti1 = fftbp_unscr_hilintc_snap['imag1']
        hilint_conv_sync = fftbp_unscr_hilintc_snap['sync']
        hilint_conv_dv = fftbp_unscr_hilintc_snap['dv']            
        
        fftr2 = fftbp_unscr_hilintc1_snap['real2']
        ffti2 = fftbp_unscr_hilintc1_snap['imag2']
        fftr3 = fftbp_unscr_hilintc1_snap['real3']
        ffti3 = fftbp_unscr_hilintc1_snap['imag3']

        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hilintc_cmplx_f0 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hilintc_cmplx_f0)
        
        filename = fftbp_unscr_hilint_conv_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hilintc_cmplx_f0:
                filehandle.write('%s\n' % listitem) 


        # Extra file write debug
        filename = fftbp_unscr_hilint_conv_filename + '_sync_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilint_conv_sync:
                filehandle.write('%s\n' % listitem)                 
                
        filename = fftbp_unscr_hilint_conv_filename + '_dv_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilint_conv_dv:
                filehandle.write('%s\n' % listitem)                   
                
        filename = fftbp_unscr_hilint_conv_filename + '_fftr0_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr0:
                filehandle.write('%s\n' % listitem)   
                

        # -- FHost 1
        fhost_num = 1
       
        fftbp_unscr_hilintc_snap = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc_ss.read(arm=False)['data']
        fftbp_unscr_hilintc1_snap = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_hilintc_snap['real0']
        ffti0 = fftbp_unscr_hilintc_snap['imag0']
        fftr1 = fftbp_unscr_hilintc_snap['real1']
        ffti1 = fftbp_unscr_hilintc_snap['imag1']
        
        fftr2 = fftbp_unscr_hilintc1_snap['real2']
        ffti2 = fftbp_unscr_hilintc1_snap['imag2']
        fftr3 = fftbp_unscr_hilintc1_snap['real3']
        ffti3 = fftbp_unscr_hilintc1_snap['imag3']

        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hilintc_cmplx_f1 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hilintc_cmplx_f1)
        
        filename = fftbp_unscr_hilint_conv_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hilintc_cmplx_f1:
                filehandle.write('%s\n' % listitem) 
                
                
        # -- FHost 2
        fhost_num = 2
       
        fftbp_unscr_hilintc_snap = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc_ss.read(arm=False)['data']
        fftbp_unscr_hilintc1_snap = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_hilintc_snap['real0']
        ffti0 = fftbp_unscr_hilintc_snap['imag0']
        fftr1 = fftbp_unscr_hilintc_snap['real1']
        ffti1 = fftbp_unscr_hilintc_snap['imag1']
        
        fftr2 = fftbp_unscr_hilintc1_snap['real2']
        ffti2 = fftbp_unscr_hilintc1_snap['imag2']
        fftr3 = fftbp_unscr_hilintc1_snap['real3']
        ffti3 = fftbp_unscr_hilintc1_snap['imag3']

        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hilintc_cmplx_f2 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hilintc_cmplx_f2)
        
        filename = fftbp_unscr_hilint_conv_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hilintc_cmplx_f2:
                filehandle.write('%s\n' % listitem) 


        # -- FHost 3
        fhost_num = 3
       
        fftbp_unscr_hilintc_snap = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc_ss.read(arm=False)['data']
        fftbp_unscr_hilintc1_snap = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc1_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_hilintc_snap['real0']
        ffti0 = fftbp_unscr_hilintc_snap['imag0']
        fftr1 = fftbp_unscr_hilintc_snap['real1']
        ffti1 = fftbp_unscr_hilintc_snap['imag1']
        
        fftr2 = fftbp_unscr_hilintc1_snap['real2']
        ffti2 = fftbp_unscr_hilintc1_snap['imag2']
        fftr3 = fftbp_unscr_hilintc1_snap['real3']
        ffti3 = fftbp_unscr_hilintc1_snap['imag3']

        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hilintc_cmplx_f3 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hilintc_cmplx_f3)
        
        filename = fftbp_unscr_hilint_conv_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hilintc_cmplx_f3:
                filehandle.write('%s\n' % listitem)                                 


        # FFT BP Uncramble Hilbert Internal Conv Diff
        print '-------------  *** FFT BP Unscramble Hilbert Internal Convert Diff ***   -------------'
        print 'FFT BP Unscramble Hilbert Internal Convert Diff 0-1'
        d.board_ss_diff(fftbp_unscr_hilintc_cmplx_f0,fftbp_unscr_hilintc_cmplx_f1)
        print 'FFT BP Unscramble Hilbert Internal Convert Diff 0-2'
        d.board_ss_diff(fftbp_unscr_hilintc_cmplx_f0,fftbp_unscr_hilintc_cmplx_f2)
        print 'FFT BP Unscramble Hilbert Internal Convert Diff 0-3'
        d.board_ss_diff(fftbp_unscr_hilintc_cmplx_f0,fftbp_unscr_hilintc_cmplx_f3)
        print 'FFT BP Unscramble Hilbert Internal Convert Diff 1-2'
        d.board_ss_diff(fftbp_unscr_hilintc_cmplx_f1,fftbp_unscr_hilintc_cmplx_f2)
        print 'FFT BP Unscramble Hilbert Internal Convert Diff 1-3'
        d.board_ss_diff(fftbp_unscr_hilintc_cmplx_f1,fftbp_unscr_hilintc_cmplx_f3)
        print 'FFT BP Unscramble Hilbert Internal Convert Diff 2-3'
        d.board_ss_diff(fftbp_unscr_hilintc_cmplx_f2,fftbp_unscr_hilintc_cmplx_f3)

# -------------------------------------------------------------------------------------------------------------------------------       

    def fft_bp_unscramble_hilbert_diff(self):   
        print ' ' 
        print 'Grabbing FFT BP Unscramble Hilbert SS'   
        
        # -- FHost 0
        fhost_num = 0
       
        fftbp_unscr_ro_out_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.read(arm=False)['data']
        fftbp_unscr_ro_out_snap1 = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil1_ss.read(arm=False)['data']
        fftbp_unscr_ro_out_snap2 = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil2_ss.read(arm=False)['data']
        fftbp_unscr_ro_out_snap3 = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil3_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_ro_out_snap['real0']
        ffti0 = fftbp_unscr_ro_out_snap['imag0']
        fftr1 = fftbp_unscr_ro_out_snap['real1']
        ffti1 = fftbp_unscr_ro_out_snap['imag1']
        hilout_sync = fftbp_unscr_ro_out_snap['sync']
        hilout_dv = fftbp_unscr_ro_out_snap['dv']        
        
        
        fftr2 = fftbp_unscr_ro_out_snap1['real2']
        ffti2 = fftbp_unscr_ro_out_snap1['imag2']
        fftr3 = fftbp_unscr_ro_out_snap1['real3']
        ffti3 = fftbp_unscr_ro_out_snap1['imag3']

        fftr4 = fftbp_unscr_ro_out_snap2['real4']
        ffti4 = fftbp_unscr_ro_out_snap2['imag4']
        fftr5 = fftbp_unscr_ro_out_snap2['real5']
        ffti5 = fftbp_unscr_ro_out_snap2['imag5']
        
        fftr6 = fftbp_unscr_ro_out_snap3['real6']
        ffti6 = fftbp_unscr_ro_out_snap3['imag6']
        fftr7 = fftbp_unscr_ro_out_snap3['real7']
        ffti7 = fftbp_unscr_ro_out_snap3['imag7']        
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x], fftr4[x], fftr5[x], fftr6[x], fftr7[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x], ffti4[x], ffti5[x], ffti6[x], ffti7[x]])
                    
        fftbp_unscr_hil_cmplx_f0 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hil_cmplx_f0)
        
        filename = fftbp_unscr_hil_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hil_cmplx_f0:
                filehandle.write('%s\n' % listitem) 
                
                
                
        # Extra file write debug
        filename = fftbp_unscr_hil_filename + '_sync_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilout_sync:
                filehandle.write('%s\n' % listitem)                 
                
        filename = fftbp_unscr_hil_filename + '_dv_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hilout_dv:
                filehandle.write('%s\n' % listitem)                   
                
        filename = fftbp_unscr_hil_filename + '_fftr0_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr0:
                filehandle.write('%s\n' % listitem)  
        
        
        # -- FHost 1
        fhost_num = 1
       
        fftbp_unscr_ro_out_snap = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.read(arm=False)['data']
        fftbp_unscr_ro_out_snap1 = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil1_ss.read(arm=False)['data']
        fftbp_unscr_ro_out_snap2 = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil2_ss.read(arm=False)['data']
        fftbp_unscr_ro_out_snap3 = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil3_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_ro_out_snap['real0']
        ffti0 = fftbp_unscr_ro_out_snap['imag0']
        fftr1 = fftbp_unscr_ro_out_snap['real1']
        ffti1 = fftbp_unscr_ro_out_snap['imag1']
        hilout_sync = fftbp_unscr_ro_out_snap['sync']
        hilout_dv = fftbp_unscr_ro_out_snap['dv']        
        
        
        fftr2 = fftbp_unscr_ro_out_snap1['real2']
        ffti2 = fftbp_unscr_ro_out_snap1['imag2']
        fftr3 = fftbp_unscr_ro_out_snap1['real3']
        ffti3 = fftbp_unscr_ro_out_snap1['imag3']

        fftr4 = fftbp_unscr_ro_out_snap2['real4']
        ffti4 = fftbp_unscr_ro_out_snap2['imag4']
        fftr5 = fftbp_unscr_ro_out_snap2['real5']
        ffti5 = fftbp_unscr_ro_out_snap2['imag5']
        
        fftr6 = fftbp_unscr_ro_out_snap3['real6']
        ffti6 = fftbp_unscr_ro_out_snap3['imag6']
        fftr7 = fftbp_unscr_ro_out_snap3['real7']
        ffti7 = fftbp_unscr_ro_out_snap3['imag7']         
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x], fftr4[x], fftr5[x], fftr6[x], fftr7[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x], ffti4[x], ffti5[x], ffti6[x], ffti7[x]])
                    
        fftbp_unscr_hil_cmplx_f1 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hil_cmplx_f1)
        
        filename = fftbp_unscr_hil_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hil_cmplx_f1:
                filehandle.write('%s\n' % listitem) 
        
        # -- FHost 2
        fhost_num = 2
       
        fftbp_unscr_ro_out_snap = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.read(arm=False)['data']
        fftbp_unscr_ro_out_snap1 = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil1_ss.read(arm=False)['data']
        fftbp_unscr_ro_out_snap2 = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil2_ss.read(arm=False)['data']
        fftbp_unscr_ro_out_snap3 = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil3_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_ro_out_snap['real0']
        ffti0 = fftbp_unscr_ro_out_snap['imag0']
        fftr1 = fftbp_unscr_ro_out_snap['real1']
        ffti1 = fftbp_unscr_ro_out_snap['imag1']
        hilout_sync = fftbp_unscr_ro_out_snap['sync']
        hilout_dv = fftbp_unscr_ro_out_snap['dv']        
        
        
        fftr2 = fftbp_unscr_ro_out_snap1['real2']
        ffti2 = fftbp_unscr_ro_out_snap1['imag2']
        fftr3 = fftbp_unscr_ro_out_snap1['real3']
        ffti3 = fftbp_unscr_ro_out_snap1['imag3']

        fftr4 = fftbp_unscr_ro_out_snap2['real4']
        ffti4 = fftbp_unscr_ro_out_snap2['imag4']
        fftr5 = fftbp_unscr_ro_out_snap2['real5']
        ffti5 = fftbp_unscr_ro_out_snap2['imag5']
        
        fftr6 = fftbp_unscr_ro_out_snap3['real6']
        ffti6 = fftbp_unscr_ro_out_snap3['imag6']
        fftr7 = fftbp_unscr_ro_out_snap3['real7']
        ffti7 = fftbp_unscr_ro_out_snap3['imag7']          
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x], fftr4[x], fftr5[x], fftr6[x], fftr7[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x], ffti4[x], ffti5[x], ffti6[x], ffti7[x]])
                    
        fftbp_unscr_hil_cmplx_f2 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hil_cmplx_f2)
        
        filename = fftbp_unscr_hil_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hil_cmplx_f2:
                filehandle.write('%s\n' % listitem) 

        # -- FHost 3
        fhost_num = 3
       
        fftbp_unscr_ro_out_snap = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.read(arm=False)['data']
        fftbp_unscr_ro_out_snap1 = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil1_ss.read(arm=False)['data']
        fftbp_unscr_ro_out_snap2 = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil2_ss.read(arm=False)['data']
        fftbp_unscr_ro_out_snap3 = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil3_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_ro_out_snap['real0']
        ffti0 = fftbp_unscr_ro_out_snap['imag0']
        fftr1 = fftbp_unscr_ro_out_snap['real1']
        ffti1 = fftbp_unscr_ro_out_snap['imag1']
        hilout_sync = fftbp_unscr_ro_out_snap['sync']
        hilout_dv = fftbp_unscr_ro_out_snap['dv']        
        
        
        fftr2 = fftbp_unscr_ro_out_snap1['real2']
        ffti2 = fftbp_unscr_ro_out_snap1['imag2']
        fftr3 = fftbp_unscr_ro_out_snap1['real3']
        ffti3 = fftbp_unscr_ro_out_snap1['imag3']

        fftr4 = fftbp_unscr_ro_out_snap2['real4']
        ffti4 = fftbp_unscr_ro_out_snap2['imag4']
        fftr5 = fftbp_unscr_ro_out_snap2['real5']
        ffti5 = fftbp_unscr_ro_out_snap2['imag5']
        
        fftr6 = fftbp_unscr_ro_out_snap3['real6']
        ffti6 = fftbp_unscr_ro_out_snap3['imag6']
        fftr7 = fftbp_unscr_ro_out_snap3['real7']
        ffti7 = fftbp_unscr_ro_out_snap3['imag7']           
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x], fftr4[x], fftr5[x], fftr6[x], fftr7[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x], ffti4[x], ffti5[x], ffti6[x], ffti7[x]])
                    
        fftbp_unscr_hil_cmplx_f3 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_unscr_hil_cmplx_f3)
        
        filename = fftbp_unscr_hil_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hil_cmplx_f3:
                filehandle.write('%s\n' % listitem)         
        
        
        # FFT BP Uncramble Hilbert Diff
        print '-------------  *** FFT BP Unscramble Hilbert Diff ***   -------------'
        print 'FFT BP Unscramble Hilbert Diff 0-1'
        d.board_ss_diff(fftbp_unscr_hil_cmplx_f0,fftbp_unscr_hil_cmplx_f1)
        print 'FFT BP Unscramble Hilbert Diff 0-2'
        d.board_ss_diff(fftbp_unscr_hil_cmplx_f0,fftbp_unscr_hil_cmplx_f2)
        print 'FFT BP Unscramble Hilbert Diff 0-3'
        d.board_ss_diff(fftbp_unscr_hil_cmplx_f0,fftbp_unscr_hil_cmplx_f3)
        print 'FFT BP Unscramble Hilbert Diff 1-2'
        d.board_ss_diff(fftbp_unscr_hil_cmplx_f1,fftbp_unscr_hil_cmplx_f2)
        print 'FFT BP Unscramble Hilbert Diff 1-3'
        d.board_ss_diff(fftbp_unscr_hil_cmplx_f1,fftbp_unscr_hil_cmplx_f3)
        print 'FFT BP Unscramble Hilbert Diff 2-3'
        d.board_ss_diff(fftbp_unscr_hil_cmplx_f2,fftbp_unscr_hil_cmplx_f3)
        
        
        
    def fft_bp_unscramble_buffer(self):   
        print ' ' 
        print 'Grabbing FFT BP Unscramble Buffer SS'   
        
        # -- FHost 0
        fhost_num = 0
       
        fftbp_unscr_buf0_in_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf0_in_ss.read(arm=False)['data']
        fftbp_unscr_buf1_in_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf1_in_ss.read(arm=False)['data']
        
        fftbp_unscr_buf0_out_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf0_out_ss.read(arm=False)['data']
        fftbp_unscr_buf1_out_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf1_out_ss.read(arm=False)['data']
        
        fftr0_in = fftbp_unscr_buf0_in_snap['b0_in0']
        ffti0_in = fftbp_unscr_buf0_in_snap['b0_in1']
        fftr1_in = fftbp_unscr_buf0_in_snap['b0_in2']
        ffti1_in = fftbp_unscr_buf0_in_snap['b0_in3']
        
        fftr2_in = fftbp_unscr_buf1_in_snap['b0_in0']
        ffti2_in = fftbp_unscr_buf1_in_snap['b0_in1']
        fftr3_in = fftbp_unscr_buf1_in_snap['b0_in2']
        ffti3_in = fftbp_unscr_buf1_in_snap['b0_in3']

        fftr0_out = fftbp_unscr_buf0_in_snap['b0_out0']
        ffti0_out = fftbp_unscr_buf0_in_snap['b0_out1']
        fftr1_out = fftbp_unscr_buf0_in_snap['b0_out2']
        ffti1_out = fftbp_unscr_buf0_in_snap['b0_out3']
        
        fftr2_out = fftbp_unscr_buf1_in_snap['b1_out0']
        ffti2_out = fftbp_unscr_buf1_in_snap['b1_out1']
        fftr3_out = fftbp_unscr_buf1_in_snap['b1_out2']
        ffti3_out = fftbp_unscr_buf1_in_snap['b1_out3']
       
        buf_sync_in = fftbp_unscr_buf0_in_snap['sync_in']
        buf_dv_in = fftbp_unscr_buf0_in_snap['dv_in']
        buf_sync_out = fftbp_unscr_buf0_in_snap['sync_out']
        buf_dv_out = fftbp_unscr_buf0_in_snap['dv_out']
        buf_and = fftbp_unscr_buf0_in_snap['and']

        
        # Extra file write debug
        filename = fftbp_unscr_hil_buf_filename + '_sync_in_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in buf_sync_in:
                filehandle.write('%s\n' % listitem)                 
                
        filename = fftbp_unscr_hil_buf_filename + '_dv_in_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in buf_dv_in:
                filehandle.write('%s\n' % listitem)   

        filename = fftbp_unscr_hil_buf_filename + '_and_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in buf_and:
                filehandle.write('%s\n' % listitem)  

        filename = fftbp_unscr_hil_buf_filename + '_sync_out_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in buf_sync_out:
                filehandle.write('%s\n' % listitem) 

        filename = fftbp_unscr_hil_buf_filename + '_dv_out_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in buf_dv_out:
                filehandle.write('%s\n' % listitem)                   
                

        filename = fftbp_unscr_hil_buf_filename + '_fftr0_in_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr0_in:
                filehandle.write('%s\n' % listitem)  
                
        filename = fftbp_unscr_hil_buf_filename + '_fftr0_out_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr0_out:
                filehandle.write('%s\n' % listitem)  


        filename = fftbp_unscr_hil_buf_filename + '_fftr2_in_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr2_in:
                filehandle.write('%s\n' % listitem)  
                
        filename = fftbp_unscr_hil_buf_filename + '_fftr2_out_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr2_out:
                filehandle.write('%s\n' % listitem)          

                

        
    def fft_bp_unscramble_hilbert_split_diff(self):   
        print ' ' 
        print 'Grabbing FFT BP Unscramble Hilbert SS'   
        
        # -- FHost 0
        fhost_num = 0
       
        #f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.print_snap()
        
        fftbp_unscr_ro_snap = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap1 = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil1_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap2 = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil2_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap3 = f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil3_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_ro_snap['real0']
        ffti0 = fftbp_unscr_ro_snap['imag0']
        fftr1 = fftbp_unscr_ro_snap['real1']
        ffti1 = fftbp_unscr_ro_snap['imag1']
        hil_sync = fftbp_unscr_ro_snap['sync']
        hil_dv = fftbp_unscr_ro_snap['dv']
        
        fftr2 = fftbp_unscr_ro_snap1['real2']
        ffti2 = fftbp_unscr_ro_snap1['imag2']
        fftr3 = fftbp_unscr_ro_snap1['real3']
        ffti3 = fftbp_unscr_ro_snap1['imag3']

        fftr4 = fftbp_unscr_ro_snap2['real4']
        ffti4 = fftbp_unscr_ro_snap2['imag4']
        fftr5 = fftbp_unscr_ro_snap2['real5']
        ffti5 = fftbp_unscr_ro_snap2['imag5']
        
        fftr6 = fftbp_unscr_ro_snap3['real6']
        ffti6 = fftbp_unscr_ro_snap3['imag6']
        fftr7 = fftbp_unscr_ro_snap3['real7']
        ffti7 = fftbp_unscr_ro_snap3['imag7']    
        
        
        
        fft_real_upper = []
        fft_imag_upper = []

                              
        for x in range(0, len(fftr0)):
            fft_real_upper.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag_upper.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hil_upper_cmplx_f0 = fft_real_upper + np.multiply(fft_imag_upper, 1j)
        
        print len(fftbp_unscr_hil_upper_cmplx_f0)
        
        filename = fftbp_unscr_hil_upper_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hil_upper_cmplx_f0:
                filehandle.write('%s\n' % listitem) 
                
                
        # Extra file write debug
        filename = fftbp_unscr_hil_upper_filename + '_sync_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hil_sync:
                filehandle.write('%s\n' % listitem)                 
                
        filename = fftbp_unscr_hil_upper_filename + '_dv_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hil_dv:
                filehandle.write('%s\n' % listitem)                   
                
        filename = fftbp_unscr_hil_upper_filename + '_fftr0_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr0:
                filehandle.write('%s\n' % listitem)  
                
        # -------------------------------------------------------------------    
                
        fft_real_lower = []
        fft_imag_lower = []                
                
        for x in range(0, len(fftr0)):
            fft_real_lower.extend(
                [fftr4[x], fftr5[x], fftr6[x], fftr7[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag_lower.extend(
                [ffti4[x], ffti5[x], ffti6[x], ffti7[x]])
                    
        fftbp_unscr_hil_lower_cmplx_f0 = fft_real_lower + np.multiply(fft_imag_lower, 1j)
        
        print len(fftbp_unscr_hil_lower_cmplx_f0)
        
        filename = fftbp_unscr_hil_lower_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hil_lower_cmplx_f0:
                filehandle.write('%s\n' % listitem)                 


        # Extra file write debug
        filename = fftbp_unscr_hil_lower_filename + '_sync_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hil_sync:
                filehandle.write('%s\n' % listitem)                 
                
        filename = fftbp_unscr_hil_lower_filename + '_dv_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in hil_dv:
                filehandle.write('%s\n' % listitem)                   
                
        filename = fftbp_unscr_hil_lower_filename + '_fftr4_' + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftr4:
                filehandle.write('%s\n' % listitem)  
                
                
        
        # -- FHost 1
        fhost_num = 1
       
        fftbp_unscr_ro_snap = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap1 = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil1_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap2 = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil2_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap3 = f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil3_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_ro_snap['real0']
        ffti0 = fftbp_unscr_ro_snap['imag0']
        fftr1 = fftbp_unscr_ro_snap['real1']
        ffti1 = fftbp_unscr_ro_snap['imag1']
        
        fftr2 = fftbp_unscr_ro_snap1['real2']
        ffti2 = fftbp_unscr_ro_snap1['imag2']
        fftr3 = fftbp_unscr_ro_snap1['real3']
        ffti3 = fftbp_unscr_ro_snap1['imag3']

        fftr4 = fftbp_unscr_ro_snap2['real4']
        ffti4 = fftbp_unscr_ro_snap2['imag4']
        fftr5 = fftbp_unscr_ro_snap2['real5']
        ffti5 = fftbp_unscr_ro_snap2['imag5']
        
        fftr6 = fftbp_unscr_ro_snap3['real6']
        ffti6 = fftbp_unscr_ro_snap3['imag6']
        fftr7 = fftbp_unscr_ro_snap3['real7']
        ffti7 = fftbp_unscr_ro_snap3['imag7']        
        
        fft_real_upper = []
        fft_imag_upper = []

                              
        for x in range(0, len(fftr0)):
            fft_real_upper.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag_upper.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hil_upper_cmplx_f1 = fft_real_upper + np.multiply(fft_imag_upper, 1j)
        
        print len(fftbp_unscr_hil_upper_cmplx_f1)
        
        filename = fftbp_unscr_hil_upper_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hil_upper_cmplx_f1:
                filehandle.write('%s\n' % listitem) 
                
                
        fft_real_lower = []
        fft_imag_lower = []                
                
        for x in range(0, len(fftr0)):
            fft_real_lower.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag_lower.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hil_lower_cmplx_f1 = fft_real_lower + np.multiply(fft_imag_lower, 1j)
        
        print len(fftbp_unscr_hil_lower_cmplx_f1)
        
        filename = fftbp_unscr_hil_lower_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hil_lower_cmplx_f1:
                filehandle.write('%s\n' % listitem)   
        
        # -- FHost 2
        fhost_num = 2
       
        fftbp_unscr_ro_snap = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap1 = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil1_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap2 = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil2_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap3 = f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil3_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_ro_snap['real0']
        ffti0 = fftbp_unscr_ro_snap['imag0']
        fftr1 = fftbp_unscr_ro_snap['real1']
        ffti1 = fftbp_unscr_ro_snap['imag1']
        
        fftr2 = fftbp_unscr_ro_snap1['real2']
        ffti2 = fftbp_unscr_ro_snap1['imag2']
        fftr3 = fftbp_unscr_ro_snap1['real3']
        ffti3 = fftbp_unscr_ro_snap1['imag3']

        fftr4 = fftbp_unscr_ro_snap2['real4']
        ffti4 = fftbp_unscr_ro_snap2['imag4']
        fftr5 = fftbp_unscr_ro_snap2['real5']
        ffti5 = fftbp_unscr_ro_snap2['imag5']
        
        fftr6 = fftbp_unscr_ro_snap3['real6']
        ffti6 = fftbp_unscr_ro_snap3['imag6']
        fftr7 = fftbp_unscr_ro_snap3['real7']
        ffti7 = fftbp_unscr_ro_snap3['imag7']        
        
        fft_real_upper = []
        fft_imag_upper = []

                              
        for x in range(0, len(fftr0)):
            fft_real_upper.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag_upper.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hil_upper_cmplx_f2 = fft_real_upper + np.multiply(fft_imag_upper, 1j)
        
        print len(fftbp_unscr_hil_upper_cmplx_f2)
        
        filename = fftbp_unscr_hil_upper_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hil_upper_cmplx_f2:
                filehandle.write('%s\n' % listitem) 
                
                
        fft_real_lower = []
        fft_imag_lower = []                
                
        for x in range(0, len(fftr0)):
            fft_real_lower.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag_lower.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hil_lower_cmplx_f2 = fft_real_lower + np.multiply(fft_imag_lower, 1j)
        
        print len(fftbp_unscr_hil_lower_cmplx_f2)
        
        filename = fftbp_unscr_hil_lower_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hil_lower_cmplx_f2:
                filehandle.write('%s\n' % listitem)   

        # -- FHost 3
        fhost_num = 3
       
        fftbp_unscr_ro_snap = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap1 = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil1_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap2 = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil2_ss.read(arm=False)['data']
        fftbp_unscr_ro_snap3 = f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil3_ss.read(arm=False)['data']
        
        fftr0 = fftbp_unscr_ro_snap['real0']
        ffti0 = fftbp_unscr_ro_snap['imag0']
        fftr1 = fftbp_unscr_ro_snap['real1']
        ffti1 = fftbp_unscr_ro_snap['imag1']
        
        fftr2 = fftbp_unscr_ro_snap1['real2']
        ffti2 = fftbp_unscr_ro_snap1['imag2']
        fftr3 = fftbp_unscr_ro_snap1['real3']
        ffti3 = fftbp_unscr_ro_snap1['imag3']

        fftr4 = fftbp_unscr_ro_snap2['real4']
        ffti4 = fftbp_unscr_ro_snap2['imag4']
        fftr5 = fftbp_unscr_ro_snap2['real5']
        ffti5 = fftbp_unscr_ro_snap2['imag5']
        
        fftr6 = fftbp_unscr_ro_snap3['real6']
        ffti6 = fftbp_unscr_ro_snap3['imag6']
        fftr7 = fftbp_unscr_ro_snap3['real7']
        ffti7 = fftbp_unscr_ro_snap3['imag7']        
        
        fft_real_upper = []
        fft_imag_upper = []

                              
        for x in range(0, len(fftr0)):
            fft_real_upper.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag_upper.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hil_upper_cmplx_f3 = fft_real_upper + np.multiply(fft_imag_upper, 1j)
        
        print len(fftbp_unscr_hil_upper_cmplx_f3)
        
        filename = fftbp_unscr_hil_upper_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hil_upper_cmplx_f3:
                filehandle.write('%s\n' % listitem) 
                
                
        fft_real_lower = []
        fft_imag_lower = []                
                
        for x in range(0, len(fftr0)):
            fft_real_lower.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag_lower.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftbp_unscr_hil_lower_cmplx_f3 = fft_real_lower + np.multiply(fft_imag_lower, 1j)
        
        print len(fftbp_unscr_hil_lower_cmplx_f3)
        
        filename = fftbp_unscr_hil_lower_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_unscr_hil_lower_cmplx_f3:
                filehandle.write('%s\n' % listitem)          
        
        
        # FFT BP Uncramble Hilbert Diff
        print '-------------  *** FFT BP Unscramble Hilbert Split (lower) Diff ***   -------------'
        print 'FFT BP Unscramble Hilbert Split Diff (lower) 0-1'
        d.board_ss_diff(fftbp_unscr_hil_lower_cmplx_f0,fftbp_unscr_hil_lower_cmplx_f1)
        print 'FFT BP Unscramble Hilbert Split Diff (lower) 0-2'
        d.board_ss_diff(fftbp_unscr_hil_lower_cmplx_f0,fftbp_unscr_hil_lower_cmplx_f2)
        print 'FFT BP Unscramble Hilbert Split Diff (lower) 0-3'
        d.board_ss_diff(fftbp_unscr_hil_lower_cmplx_f0,fftbp_unscr_hil_lower_cmplx_f3)
        print 'FFT BP Unscramble Hilbert Split Diff (lower) 1-2'
        d.board_ss_diff(fftbp_unscr_hil_lower_cmplx_f1,fftbp_unscr_hil_lower_cmplx_f2)
        print 'FFT BP Unscramble Hilbert Split Diff (lower) 1-3'
        d.board_ss_diff(fftbp_unscr_hil_lower_cmplx_f1,fftbp_unscr_hil_lower_cmplx_f3)
        print 'FFT BP Unscramble Hilbert Split Diff (lower) 2-3'
        d.board_ss_diff(fftbp_unscr_hil_lower_cmplx_f2,fftbp_unscr_hil_lower_cmplx_f3)
        
        print '-------------  *** FFT BP Unscramble Hilbert Split (Upper) Diff ***   -------------'
        print 'FFT BP Unscramble Hilbert Split Diff (Upper) 0-1'
        d.board_ss_diff(fftbp_unscr_hil_upper_cmplx_f0,fftbp_unscr_hil_upper_cmplx_f1)
        print 'FFT BP Unscramble Hilbert Split Diff (Upper) 0-2'
        d.board_ss_diff(fftbp_unscr_hil_upper_cmplx_f0,fftbp_unscr_hil_upper_cmplx_f2)
        print 'FFT BP Unscramble Hilbert Split Diff (Upper) 0-3'
        d.board_ss_diff(fftbp_unscr_hil_upper_cmplx_f0,fftbp_unscr_hil_upper_cmplx_f3)
        print 'FFT BP Unscramble Hilbert Split Diff (Upper) 1-2'
        d.board_ss_diff(fftbp_unscr_hil_upper_cmplx_f1,fftbp_unscr_hil_upper_cmplx_f2)
        print 'FFT BP Unscramble Hilbert Split Diff (Upper) 1-3'
        d.board_ss_diff(fftbp_unscr_hil_upper_cmplx_f1,fftbp_unscr_hil_upper_cmplx_f3)
        print 'FFT BP Unscramble Hilbert Split Diff (Upper) 2-3'
        d.board_ss_diff(fftbp_unscr_hil_upper_cmplx_f2,fftbp_unscr_hil_upper_cmplx_f3)        
        
        

# -------------------------------------------------------------------------------------------------------------------------------       
             

    def fft_bp_diff(self):       
        print ' ' 
        print 'Grabbing FFT BP SS'   
        
        # -- FHost 0
        fhost_num = 0
        
        #fftbp_snap = f0.snapshots.pfb_fft_wideband_real_snap_fftbp_ss.read(arm=False)['data']
        #fftbp_snap1 = f0.snapshots.pfb_fft_wideband_real_snap_fftbp1_ss.read(arm=False)['data']
        #fftbp_snap2 = f0.snapshots.pfb_fft_wideband_real_snap_fftbp2_ss.read(arm=False)['data']
        #fftbp_snap3 = f0.snapshots.pfb_fft_wideband_real_snap_fftbp3_ss.read(arm=False)['data']
        
        fftbp_snap = f0.snapshots.pfb_fft_snap_fftbp_ss.read(arm=False)['data']
        fftbp_snap1 = f0.snapshots.pfb_fft_snap_fftbp1_ss.read(arm=False)['data']
        fftbp_snap2 = f0.snapshots.pfb_fft_snap_fftbp2_ss.read(arm=False)['data']
        fftbp_snap3 = f0.snapshots.pfb_fft_snap_fftbp3_ss.read(arm=False)['data']
        
        fftr0 = fftbp_snap['real0']
        ffti0 = fftbp_snap['imag0']
        fftr1 = fftbp_snap['real1']
        ffti1 = fftbp_snap['imag1']
        
        fftr2 = fftbp_snap1['real2']
        ffti2 = fftbp_snap1['imag2']
        fftr3 = fftbp_snap1['real3']
        ffti3 = fftbp_snap1['imag3']
                   
        fftr4 = fftbp_snap2['real4']
        ffti4 = fftbp_snap2['imag4']
        fftr5 = fftbp_snap2['real5']
        ffti5 = fftbp_snap2['imag5']
        
        fftr6 = fftbp_snap3['real6']
        ffti6 = fftbp_snap3['imag6']
        fftr7 = fftbp_snap3['real7']
        ffti7 = fftbp_snap3['imag7']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x], fftr4[x], fftr5[x], fftr6[x], fftr7[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x], ffti4[x], ffti5[x], ffti6[x], ffti7[x]])
                    
        fftbp_cmplx_f0 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_cmplx_f0)
        
        filename = fftbp_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_cmplx_f0:
                filehandle.write('%s\n' % listitem) 
        
        
        # -- FHost 1
        fhost_num = 1
        
        #fftbp_snap = f1.snapshots.pfb_fft_wideband_real_snap_fftbp_ss.read(arm=False)['data']
        #fftbp_snap1 = f1.snapshots.pfb_fft_wideband_real_snap_fftbp1_ss.read(arm=False)['data']
        #fftbp_snap2 = f1.snapshots.pfb_fft_wideband_real_snap_fftbp2_ss.read(arm=False)['data']
        #fftbp_snap3 = f1.snapshots.pfb_fft_wideband_real_snap_fftbp3_ss.read(arm=False)['data']
        
        fftbp_snap = f1.snapshots.pfb_fft_snap_fftbp_ss.read(arm=False)['data']
        fftbp_snap1 = f1.snapshots.pfb_fft_snap_fftbp1_ss.read(arm=False)['data']
        fftbp_snap2 = f1.snapshots.pfb_fft_snap_fftbp2_ss.read(arm=False)['data']
        fftbp_snap3 = f1.snapshots.pfb_fft_snap_fftbp3_ss.read(arm=False)['data']
        
        fftr0 = fftbp_snap['real0']
        ffti0 = fftbp_snap['imag0']
        fftr1 = fftbp_snap['real1']
        ffti1 = fftbp_snap['imag1']
        
        fftr2 = fftbp_snap1['real2']
        ffti2 = fftbp_snap1['imag2']
        fftr3 = fftbp_snap1['real3']
        ffti3 = fftbp_snap1['imag3']
                   
        fftr4 = fftbp_snap2['real4']
        ffti4 = fftbp_snap2['imag4']
        fftr5 = fftbp_snap2['real5']
        ffti5 = fftbp_snap2['imag5']
        
        fftr6 = fftbp_snap3['real6']
        ffti6 = fftbp_snap3['imag6']
        fftr7 = fftbp_snap3['real7']
        ffti7 = fftbp_snap3['imag7']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x], fftr4[x], fftr5[x], fftr6[x], fftr7[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x], ffti4[x], ffti5[x], ffti6[x], ffti7[x]])
                    
        fftbp_cmplx_f1 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_cmplx_f1)
        
        filename = fftbp_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_cmplx_f1:
                filehandle.write('%s\n' % listitem) 
        
        
        # -- FHost 2
        fhost_num = 2
        
        #fftbp_snap = f2.snapshots.pfb_fft_wideband_real_snap_fftbp_ss.read(arm=False)['data']
        #fftbp_snap1 = f2.snapshots.pfb_fft_wideband_real_snap_fftbp1_ss.read(arm=False)['data']
        #fftbp_snap2 = f2.snapshots.pfb_fft_wideband_real_snap_fftbp2_ss.read(arm=False)['data']
        #fftbp_snap3 = f2.snapshots.pfb_fft_wideband_real_snap_fftbp3_ss.read(arm=False)['data']
        
        fftbp_snap = f2.snapshots.pfb_fft_snap_fftbp_ss.read(arm=False)['data']
        fftbp_snap1 = f2.snapshots.pfb_fft_snap_fftbp1_ss.read(arm=False)['data']
        fftbp_snap2 = f2.snapshots.pfb_fft_snap_fftbp2_ss.read(arm=False)['data']
        fftbp_snap3 = f2.snapshots.pfb_fft_snap_fftbp3_ss.read(arm=False)['data']
        
        fftr0 = fftbp_snap['real0']
        ffti0 = fftbp_snap['imag0']
        fftr1 = fftbp_snap['real1']
        ffti1 = fftbp_snap['imag1']
        
        fftr2 = fftbp_snap1['real2']
        ffti2 = fftbp_snap1['imag2']
        fftr3 = fftbp_snap1['real3']
        ffti3 = fftbp_snap1['imag3']
                   
        fftr4 = fftbp_snap2['real4']
        ffti4 = fftbp_snap2['imag4']
        fftr5 = fftbp_snap2['real5']
        ffti5 = fftbp_snap2['imag5']
        
        fftr6 = fftbp_snap3['real6']
        ffti6 = fftbp_snap3['imag6']
        fftr7 = fftbp_snap3['real7']
        ffti7 = fftbp_snap3['imag7']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x], fftr4[x], fftr5[x], fftr6[x], fftr7[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x], ffti4[x], ffti5[x], ffti6[x], ffti7[x]])
                    
        fftbp_cmplx_f2 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_cmplx_f2)
        
        filename = fftbp_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_cmplx_f2:
                filehandle.write('%s\n' % listitem) 
        
        
        # -- FHost 3
        fhost_num = 3
        
        #fftbp_snap = f3.snapshots.pfb_fft_wideband_real_snap_fftbp_ss.read(arm=False)['data']
        #fftbp_snap1 = f3.snapshots.pfb_fft_wideband_real_snap_fftbp1_ss.read(arm=False)['data']
        #fftbp_snap2 = f3.snapshots.pfb_fft_wideband_real_snap_fftbp2_ss.read(arm=False)['data']
        #fftbp_snap3 = f3.snapshots.pfb_fft_wideband_real_snap_fftbp3_ss.read(arm=False)['data']
        
        fftbp_snap = f3.snapshots.pfb_fft_snap_fftbp_ss.read(arm=False)['data']
        fftbp_snap1 = f3.snapshots.pfb_fft_snap_fftbp1_ss.read(arm=False)['data']
        fftbp_snap2 = f3.snapshots.pfb_fft_snap_fftbp2_ss.read(arm=False)['data']
        fftbp_snap3 = f3.snapshots.pfb_fft_snap_fftbp3_ss.read(arm=False)['data']
        
        fftr0 = fftbp_snap['real0']
        ffti0 = fftbp_snap['imag0']
        fftr1 = fftbp_snap['real1']
        ffti1 = fftbp_snap['imag1']
        
        fftr2 = fftbp_snap1['real2']
        ffti2 = fftbp_snap1['imag2']
        fftr3 = fftbp_snap1['real3']
        ffti3 = fftbp_snap1['imag3']
                   
        fftr4 = fftbp_snap2['real4']
        ffti4 = fftbp_snap2['imag4']
        fftr5 = fftbp_snap2['real5']
        ffti5 = fftbp_snap2['imag5']
        
        fftr6 = fftbp_snap3['real6']
        ffti6 = fftbp_snap3['imag6']
        fftr7 = fftbp_snap3['real7']
        ffti7 = fftbp_snap3['imag7']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x], fftr4[x], fftr5[x], fftr6[x], fftr7[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x], ffti4[x], ffti5[x], ffti6[x], ffti7[x]])
                    
        fftbp_cmplx_f3 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftbp_cmplx_f3)
        
        filename = fftbp_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftbp_cmplx_f3:
                filehandle.write('%s\n' % listitem) 

        # FFT BP Diff
        print '-------------  *** FFT BP Diff ***   -------------'
        print 'FFT BP Diff 0-1'
        d.board_ss_diff(fftbp_cmplx_f0,fftbp_cmplx_f1)
        print 'FFT BP Diff 0-2'
        d.board_ss_diff(fftbp_cmplx_f0,fftbp_cmplx_f2)
        print 'FFT BP Diff 0-3'
        d.board_ss_diff(fftbp_cmplx_f0,fftbp_cmplx_f3)
        print 'FFT BP Diff 1-2'
        d.board_ss_diff(fftbp_cmplx_f1,fftbp_cmplx_f2)
        print 'FFT BP Diff 1-3'
        d.board_ss_diff(fftbp_cmplx_f1,fftbp_cmplx_f3)
        print 'FFT BP Diff 2-3'
        d.board_ss_diff(fftbp_cmplx_f2,fftbp_cmplx_f3)
        
        
# -------------------------------------------------------------------------------------------------------------------------------       
            
    def fft_dir_diff(self):          
        print ' ' 
        print 'Grabbing FFT Dir SS'   
        
        # -- FHost 0
        fhost_num = 0
        
        fftdir_snap = f0.snapshots.pfb_fft_wideband_real_snap_fftdir_ss.read(arm=False)['data']
        fftdir_snap1 = f0.snapshots.pfb_fft_wideband_real_snap_fftdir1_ss.read(arm=False)['data']
        
        fftr0 = fftdir_snap['real0']
        ffti0 = fftdir_snap['imag0']
        fftr1 = fftdir_snap['real1']
        ffti1 = fftdir_snap['imag1']
        
        fftr2 = fftdir_snap1['real2']
        ffti2 = fftdir_snap1['imag2']
        fftr3 = fftdir_snap1['real3']
        ffti3 = fftdir_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftdir_cmplx_f0 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftdir_cmplx_f0)
        
        filename = fftdir_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftdir_cmplx_f0:
                filehandle.write('%s\n' % listitem) 
                
                
        # -- FHost 1
        fhost_num = 1
        
        fftdir_snap = f1.snapshots.pfb_fft_wideband_real_snap_fftdir_ss.read(arm=False)['data']
        fftdir_snap1 = f1.snapshots.pfb_fft_wideband_real_snap_fftdir1_ss.read(arm=False)['data']
        
        fftr0 = fftdir_snap['real0']
        ffti0 = fftdir_snap['imag0']
        fftr1 = fftdir_snap['real1']
        ffti1 = fftdir_snap['imag1']
        
        fftr2 = fftdir_snap1['real2']
        ffti2 = fftdir_snap1['imag2']
        fftr3 = fftdir_snap1['real3']
        ffti3 = fftdir_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftdir_cmplx_f1 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftdir_cmplx_f1)
        
        filename = fftdir_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftdir_cmplx_f1:
                filehandle.write('%s\n' % listitem)         
                
        
        # -- FHost 2
        fhost_num = 2
        
        fftdir_snap = f2.snapshots.pfb_fft_wideband_real_snap_fftdir_ss.read(arm=False)['data']
        fftdir_snap1 = f2.snapshots.pfb_fft_wideband_real_snap_fftdir1_ss.read(arm=False)['data']
        
        fftr0 = fftdir_snap['real0']
        ffti0 = fftdir_snap['imag0']
        fftr1 = fftdir_snap['real1']
        ffti1 = fftdir_snap['imag1']
        
        fftr2 = fftdir_snap1['real2']
        ffti2 = fftdir_snap1['imag2']
        fftr3 = fftdir_snap1['real3']
        ffti3 = fftdir_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftdir_cmplx_f2 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftdir_cmplx_f2)
        
        filename = fftdir_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftdir_cmplx_f2:
                filehandle.write('%s\n' % listitem)    
        
        
        # -- FHost 3
        fhost_num = 3
        
        fftdir_snap = f3.snapshots.pfb_fft_wideband_real_snap_fftdir_ss.read(arm=False)['data']
        fftdir_snap1 = f3.snapshots.pfb_fft_wideband_real_snap_fftdir1_ss.read(arm=False)['data']
        
        fftr0 = fftdir_snap['real0']
        ffti0 = fftdir_snap['imag0']
        fftr1 = fftdir_snap['real1']
        ffti1 = fftdir_snap['imag1']
        
        fftr2 = fftdir_snap1['real2']
        ffti2 = fftdir_snap1['imag2']
        fftr3 = fftdir_snap1['real3']
        ffti3 = fftdir_snap1['imag3']
        
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fftdir_cmplx_f3 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fftdir_cmplx_f3)
        
        filename = fftdir_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fftdir_cmplx_f3:
                filehandle.write('%s\n' % listitem)   
        
        # FFT Dir Diff
        print '-------------  *** FFT Dir Diff ***   -------------'
        print 'FFT Dir Diff 0-1'
        d.board_ss_diff(fftdir_cmplx_f0,fftdir_cmplx_f1)
        print 'FFT Dir Diff 0-2'
        d.board_ss_diff(fftdir_cmplx_f0,fftdir_cmplx_f2)
        print 'FFT Dir Diff 0-3'
        d.board_ss_diff(fftdir_cmplx_f0,fftdir_cmplx_f3)
        print 'FFT Dir Diff 1-2'
        d.board_ss_diff(fftdir_cmplx_f1,fftdir_cmplx_f2)
        print 'FFT Dir Diff 1-3'
        d.board_ss_diff(fftdir_cmplx_f1,fftdir_cmplx_f3)
        print 'FFT Dir Diff 2-3'
        d.board_ss_diff(fftdir_cmplx_f2,fftdir_cmplx_f3)
            
# -------------------------------------------------------------------------------------------------------------       
        
    def fft_out_diff(self):
        print ' ' 
        print 'Grabbing FFT SS'   
        
        # -- FHost 0
        fhost_num = 0
        #fft_snap = f0.snapshots.pfb_snap_fft_out_ss.read()['data'] 
        fft_snap = f0.snapshots.pfb_snap_fft_out_ss.read(arm=False)['data']
        fft_snap1 = f0.snapshots.pfb_snap_fft_out1_ss.read(arm=False)['data']
        
        fftr0 = fft_snap['real0']
        ffti0 = fft_snap['imag0']
        fftr1 = fft_snap['real1']
        ffti1 = fft_snap['imag1']
        
        fftr2 = fft_snap1['real2']
        ffti2 = fft_snap1['imag2']
        fftr3 = fft_snap1['real3']
        ffti3 = fft_snap1['imag3']
                   
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fft_complx_f0 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fft_complx_f0)
        
        #with open('fft_2018_0.txt', 'w') as filehandle:
        #    for listitem in fft_complx_f0:
        #        filehandle.write('%s\n' % listitem)
        
        filename = fft_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fft_complx_f0:
                filehandle.write('%s\n' % listitem)   
        
        # -- FHost 1
        fhost_num = 1
        fft_snap = f1.snapshots.pfb_snap_fft_out_ss.read(arm=False)['data']
        fft_snap1 = f1.snapshots.pfb_snap_fft_out1_ss.read(arm=False)['data']
        
        fftr0 = fft_snap['real0']
        ffti0 = fft_snap['imag0']
        fftr1 = fft_snap['real1']
        ffti1 = fft_snap['imag1']
        
        fftr2 = fft_snap1['real2']
        ffti2 = fft_snap1['imag2']
        fftr3 = fft_snap1['real3']
        ffti3 = fft_snap1['imag3']
        
                   
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fft_complx_f1 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fft_complx_f1)
        
        #with open('fft_2018_1.txt', 'w') as filehandle:
        #    for listitem in fft_complx_f1:
        #        filehandle.write('%s\n' % listitem)
        
        filename = fft_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fft_complx_f1:
                filehandle.write('%s\n' % listitem)   
        
        # -- FHost 2
        fhost_num = 2
        fft_snap = f2.snapshots.pfb_snap_fft_out_ss.read(arm=False)['data']
        fft_snap1 = f2.snapshots.pfb_snap_fft_out1_ss.read(arm=False)['data']
        
        fftr0 = fft_snap['real0']
        ffti0 = fft_snap['imag0']
        fftr1 = fft_snap['real1']
        ffti1 = fft_snap['imag1']
        
        fftr2 = fft_snap1['real2']
        ffti2 = fft_snap1['imag2']
        fftr3 = fft_snap1['real3']
        ffti3 = fft_snap1['imag3']
        
                   
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fft_complx_f2 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fft_complx_f2)
        
        filename = fft_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fft_complx_f2:
                filehandle.write('%s\n' % listitem)   
        
        # -- FHost 3
        fhost_num = 3
        fft_snap = f3.snapshots.pfb_snap_fft_out_ss.read(arm=False)['data']
        fft_snap1 = f3.snapshots.pfb_snap_fft_out1_ss.read(arm=False)['data']
        
        fftr0 = fft_snap['real0']
        ffti0 = fft_snap['imag0']
        fftr1 = fft_snap['real1']
        ffti1 = fft_snap['imag1']
        
        fftr2 = fft_snap1['real2']
        ffti2 = fft_snap1['imag2']
        fftr3 = fft_snap1['real3']
        ffti3 = fft_snap1['imag3']
                   
        fft_real = []
        fft_imag = []
                               
        for x in range(0, len(fftr0)):
            fft_real.extend(
                [fftr0[x], fftr1[x], fftr2[x], fftr3[x]])
                    
        for x in range(0, len(ffti0)):
            fft_imag.extend(
                [ffti0[x], ffti1[x], ffti2[x], ffti3[x]])
                    
        fft_complx_f3 = fft_real + np.multiply(fft_imag, 1j)
        
        print len(fft_complx_f3)
        
        filename = fft_filename + build_ver + str(fhost_num) + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in fft_complx_f3:
                filehandle.write('%s\n' % listitem)   
        
        
        # FFT Out Diff
        print '-------------  *** FFT Out Diff ***   -------------'
        print 'FFT Out Diff 0-1'
        d.board_ss_diff(fft_complx_f0,fft_complx_f1)
        print 'FFT Out Diff 0-2'
        d.board_ss_diff(fft_complx_f0,fft_complx_f2)
        print 'FFT Out Diff 0-3'
        d.board_ss_diff(fft_complx_f0,fft_complx_f3)
        print 'FFT Out Diff 1-2'
        d.board_ss_diff(fft_complx_f1,fft_complx_f2)
        print 'FFT Out Diff 1-3'
        d.board_ss_diff(fft_complx_f1,fft_complx_f3)
        print 'FFT Out Diff 2-3'
        d.board_ss_diff(fft_complx_f2,fft_complx_f3)

        #==============================================================================
#        print ' ' 
#        print 'Grabbing Quant SS'  
#        snap_quant = f0.snapshots.snap_quant0_ss.read(arm=False)['data'] 
#        
#        q_r0 = snap_quant['real0']
#        q_i0 = snap_quant['imag0']
#        q_r1 = snap_quant['real1']
#        q_i1 = snap_quant['imag1']
#        q_r2 = snap_quant['real2']
#        q_i2 = snap_quant['imag2']
#        q_r3 = snap_quant['real3']
#        q_i3 = snap_quant['imag3']
#        
#        fftQ_real = []
#        fftQ_imag = []
#                               
#        for x in range(0, len(q_r0)):
#            fftQ_real.extend(
#                [q_r0[x], q_r1[x], q_r2[x], q_r3[x]])
#                    
#        for x in range(0, len(q_i0)):
#            fftQ_imag.extend(
#                [q_i0[x], q_i1[x], q_i2[x], q_i3[x]])
#                    
#        fftQ_complx = fftQ_real + np.multiply(fftQ_imag, 1j)
        
        #==============================================================================
#        print ' ' 
#        print 'Grabbing FD SS'  
#        snap_fd = f0.snapshots.snap_quant0_ss.read(arm=False)['data'] 
#        
#        fd_r0 = snap_fd['real0']
#        fd_i0 = snap_fd['imag0']
#        fd_r1 = snap_fd['real1']
#        fd_i1 = snap_fd['imag1']
#        fd_r2 = snap_fd['real2']
#        fd_i2 = snap_fd['imag2']
#        fd_r3 = snap_fd['real3']
#        fd_i3 = snap_fd['imag3']
#        
#        fd_real = []
#        fd_imag = []
#                               
#        for x in range(0, len(q_r0)):
#            fd_real.extend(
#                [fd_r0[x], fd_r1[x], fd_r2[x], fd_r3[x]])
#                    
#        for x in range(0, len(q_i0)):
#            fd_imag.extend(
#                [fd_i0[x], fd_i1[x], fd_i2[x], fd_i3[x]])
#                    
#        fd_complx = fd_real + np.multiply(fd_imag, 1j)            
            
            

            
            
            
            
            
        
hosts = ['skarab020303-01', 'skarab020308-01', 'skarab02030A-01', 'skarab02030E-01']
c=corr2.fxcorrelator.FxCorrelator('bob', config_source='/etc/corr/avdbyl_test_32k.ini')
c.initialise(program=False, configure=False, require_epoch=False)
        
f0 = c.fhosts[0]
f1 = c.fhosts[1]
f2 = c.fhosts[2]
f3 = c.fhosts[3]

#Disable auto reset
c.fops.auto_rst_disable()

# Reset Count Rst
f0.registers.control.write(cnt_rst='pulse')
f1.registers.control.write(cnt_rst='pulse')
f2.registers.control.write(cnt_rst='pulse')
f3.registers.control.write(cnt_rst='pulse')

#Impulse TVG Control
f0.registers.impulse0.write(offset=tvg_offset)
f0.registers.impulse0.write(amplitude=tvg_amp)
f0.registers.control.write(tvg_adc0=tvg_state)

f1.registers.impulse0.write(offset=tvg_offset)
f1.registers.impulse0.write(amplitude=tvg_amp)
f1.registers.control.write(tvg_adc0=tvg_state)

f2.registers.impulse0.write(offset=tvg_offset)
f2.registers.impulse0.write(amplitude=tvg_amp)
f2.registers.control.write(tvg_adc0=tvg_state)

f3.registers.impulse0.write(offset=tvg_offset)
f3.registers.impulse0.write(amplitude=tvg_amp)
f3.registers.control.write(tvg_adc0=tvg_state)

#CD Bypass Control
f0.registers.control.write(cd_bypass=cd_bypass)
f1.registers.control.write(cd_bypass=cd_bypass)
f2.registers.control.write(cd_bypass=cd_bypass)
f3.registers.control.write(cd_bypass=cd_bypass)

#Ramp TVG Control
f0.registers.ramp_tvg_en.write(en=ramp_tvg_en)
f1.registers.ramp_tvg_en.write(en=ramp_tvg_en)
f2.registers.ramp_tvg_en.write(en=ramp_tvg_en)
f3.registers.ramp_tvg_en.write(en=ramp_tvg_en)

#SS Trig Src
f0.registers.ss_trig_src.write(en=snapshot_trig_src)
f1.registers.ss_trig_src.write(en=snapshot_trig_src)
f2.registers.ss_trig_src.write(en=snapshot_trig_src)
f3.registers.ss_trig_src.write(en=snapshot_trig_src)

#SS Single Trig Enable
f0.registers.ss_single_trig.write(en=snapshot_single_trig)
f1.registers.ss_single_trig.write(en=snapshot_single_trig)
f2.registers.ss_single_trig.write(en=snapshot_single_trig)
f3.registers.ss_single_trig.write(en=snapshot_single_trig)

#f0.registers.hmc_bp.write(en=hmc_bp)
#f1.registers.hmc_bp.write(en=hmc_bp)
#f2.registers.hmc_bp.write(en=hmc_bp)
#f3.registers.hmc_bp.write(en=hmc_bp)
#
#f0.registers.tl_cd0_bp.write(en=tl_cd0_bp)
#f1.registers.tl_cd0_bp.write(en=tl_cd0_bp)
#f2.registers.tl_cd0_bp.write(en=tl_cd0_bp)
#f3.registers.tl_cd0_bp.write(en=tl_cd0_bp)

# ADC
f0.snapshots.snap_adc0_ss.arm(man_trig=False, man_valid=False)  
f1.snapshots.snap_adc0_ss.arm(man_trig=False, man_valid=False)  
f2.snapshots.snap_adc0_ss.arm(man_trig=False, man_valid=False)  
f3.snapshots.snap_adc0_ss.arm(man_trig=False, man_valid=False)  

## CD
#f0.snapshots.snap_cd_out_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.snap_cd_out_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.snap_cd_out_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.snap_cd_out_ss.arm(man_trig=False, man_valid=False)  

## Coeffs
#f0.snapshots.pfb_pfb_fir_generic_snap_coeff_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_pfb_fir_generic_snap_coeff_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_pfb_fir_generic_snap_coeff_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_pfb_fir_generic_snap_coeff_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_pfb_fir_generic_snap_coeff1_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_pfb_fir_generic_snap_coeff1_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_pfb_fir_generic_snap_coeff1_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_pfb_fir_generic_snap_coeff1_ss.arm(man_trig=False, man_valid=False)  
#
## FIR Int
#f0.snapshots.pfb_pfb_fir_generic_snap_fir_out_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_pfb_fir_generic_snap_fir_out_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_pfb_fir_generic_snap_fir_out_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_pfb_fir_generic_snap_fir_out_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_pfb_fir_generic_snap_fir_out1_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_pfb_fir_generic_snap_fir_out1_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_pfb_fir_generic_snap_fir_out1_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_pfb_fir_generic_snap_fir_out1_ss.arm(man_trig=False, man_valid=False)  


# FIR Out
#f0.snapshots.pfb_snap_fir_out_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_snap_fir_out_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_snap_fir_out_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_snap_fir_out_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_snap_fir_out1_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_snap_fir_out1_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_snap_fir_out1_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_snap_fir_out1_ss.arm(man_trig=False, man_valid=False)  

## FFT BP
#f0.snapshots.pfb_fft_wideband_real_snap_fftbp_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_wideband_real_snap_fftbp_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_wideband_real_snap_fftbp_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_wideband_real_snap_fftbp_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_fft_wideband_real_snap_fftbp1_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_wideband_real_snap_fftbp1_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_wideband_real_snap_fftbp1_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_wideband_real_snap_fftbp1_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_fft_wideband_real_snap_fftbp2_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_wideband_real_snap_fftbp2_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_wideband_real_snap_fftbp2_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_wideband_real_snap_fftbp2_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_fft_wideband_real_snap_fftbp3_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_wideband_real_snap_fftbp3_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_wideband_real_snap_fftbp3_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_wideband_real_snap_fftbp3_ss.arm(man_trig=False, man_valid=False)  


# FFT BP
#f0.snapshots.pfb_fft_snap_fftbp_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_snap_fftbp_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_snap_fftbp_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_snap_fftbp_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_fft_snap_fftbp1_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_snap_fftbp1_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_snap_fftbp1_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_snap_fftbp1_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_fft_snap_fftbp2_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_snap_fftbp2_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_snap_fftbp2_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_snap_fftbp2_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_fft_snap_fftbp3_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_snap_fftbp3_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_snap_fftbp3_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_snap_fftbp3_ss.arm(man_trig=False, man_valid=False)  

# FFT BP before Unscramble
f0.snapshots.pfb_fft_bi_ss_bpc_ss.arm(man_trig=False, man_valid=False)  
f1.snapshots.pfb_fft_bi_ss_bpc_ss.arm(man_trig=False, man_valid=False)  
f2.snapshots.pfb_fft_bi_ss_bpc_ss.arm(man_trig=False, man_valid=False)  
f3.snapshots.pfb_fft_bi_ss_bpc_ss.arm(man_trig=False, man_valid=False)  

f0.snapshots.pfb_fft_bi_ss_bpc1_ss.arm(man_trig=False, man_valid=False)  
f1.snapshots.pfb_fft_bi_ss_bpc1_ss.arm(man_trig=False, man_valid=False)  
f2.snapshots.pfb_fft_bi_ss_bpc1_ss.arm(man_trig=False, man_valid=False)  
f3.snapshots.pfb_fft_bi_ss_bpc1_ss.arm(man_trig=False, man_valid=False)  



# FFT BP Core Stage 1
#f0.snapshots.pfb_fft_bi_core_s10_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_bi_core_s10_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_bi_core_s10_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_bi_core_s10_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_fft_bi_core_s11_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_bi_core_s11_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_bi_core_s11_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_bi_core_s11_ss.arm(man_trig=False, man_valid=False)  

# FFT BP Core Stage 1 Internal
#f0.snapshots.pfb_fft_bi_core_ffts1_s0_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_bi_core_ffts1_s0_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_bi_core_ffts1_s0_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_bi_core_ffts1_s0_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_fft_bi_core_ffts1_s1_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_bi_core_ffts1_s1_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_bi_core_ffts1_s1_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_bi_core_ffts1_s1_ss.arm(man_trig=False, man_valid=False)  



# FFT BP Core Stage 2
#f0.snapshots.pfb_fft_bi_core_s20_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_bi_core_s20_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_bi_core_s20_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_bi_core_s20_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_fft_bi_core_s21_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_bi_core_s21_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_bi_core_s21_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_bi_core_s21_ss.arm(man_trig=False, man_valid=False)  

# FFT BP Core Stage 2 Internal
#f0.snapshots.pfb_fft_bi_core_ffts2_s0_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_bi_core_ffts2_s0_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_bi_core_ffts2_s0_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_bi_core_ffts2_s0_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_fft_bi_core_ffts2_s1_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_bi_core_ffts2_s1_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_bi_core_ffts2_s1_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_bi_core_ffts2_s1_ss.arm(man_trig=False, man_valid=False)  





# FFT BP Core Stage 3
#f0.snapshots.pfb_fft_bi_core_s30_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_bi_core_s30_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_bi_core_s30_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_bi_core_s30_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_fft_bi_core_s31_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_bi_core_s31_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_bi_core_s31_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_bi_core_s31_ss.arm(man_trig=False, man_valid=False)  

# FFT BP Unscramble Reorder
#f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro_ss.arm(man_trig=False, man_valid=True)  
#f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro_ss.arm(man_trig=False, man_valid=True)  
#f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro_ss.arm(man_trig=False, man_valid=True)  
#f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro_ss.arm(man_trig=False, man_valid=True)  
#
#f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro1_ss.arm(man_trig=False, man_valid=True)  
#f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro1_ss.arm(man_trig=False, man_valid=True)  
#f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro1_ss.arm(man_trig=False, man_valid=True)  
#f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_ro1_ss.arm(man_trig=False, man_valid=True)  

# FFT BP Unscramble Logic
#f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint2_ss.arm(man_trig=False, man_valid=True)  
#f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint2_ss.arm(man_trig=False, man_valid=True)  
#f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint2_ss.arm(man_trig=False, man_valid=True)  
#f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint2_ss.arm(man_trig=False, man_valid=True) 


# FFT BP Unscramble Hilbert Input
#f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin_ss.arm(man_trig=False, man_valid=True)  
#f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin_ss.arm(man_trig=False, man_valid=True)  
#f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin_ss.arm(man_trig=False, man_valid=True)  
#f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin_ss.arm(man_trig=False, man_valid=True)  
#
#f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin1_ss.arm(man_trig=False, man_valid=True)  
#f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin1_ss.arm(man_trig=False, man_valid=True)  
#f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin1_ss.arm(man_trig=False, man_valid=True)  
#f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilin1_ss.arm(man_trig=False, man_valid=True)  

# FFT BP Unscramble Hilbert Internal
#f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint_ss.arm(man_trig=False, man_valid=True)  
#f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint_ss.arm(man_trig=False, man_valid=True)  
#f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint_ss.arm(man_trig=False, man_valid=True)  
#f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint_ss.arm(man_trig=False, man_valid=True)  
#
#f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint1_ss.arm(man_trig=False, man_valid=True)  
#f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint1_ss.arm(man_trig=False, man_valid=True)  
#f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint1_ss.arm(man_trig=False, man_valid=True)  
#f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilint1_ss.arm(man_trig=False, man_valid=True) 

# FFT BP Unscramble Hilbert Internal
#f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc_ss.arm(man_trig=False, man_valid=True)  
#f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc_ss.arm(man_trig=False, man_valid=True)  
#f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc_ss.arm(man_trig=False, man_valid=True)  
#f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc_ss.arm(man_trig=False, man_valid=True)  
#
#f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc1_ss.arm(man_trig=False, man_valid=True)  
#f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc1_ss.arm(man_trig=False, man_valid=True)  
#f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc1_ss.arm(man_trig=False, man_valid=True)  
#f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_hilintc1_ss.arm(man_trig=False, man_valid=True) 




# FFT BP Unscramble Hilbert
f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.arm(man_trig=False, man_valid=True)  
f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.arm(man_trig=False, man_valid=True)  
f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.arm(man_trig=False, man_valid=True)  
f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil_ss.arm(man_trig=False, man_valid=True)  

f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil1_ss.arm(man_trig=False, man_valid=True)  
f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil1_ss.arm(man_trig=False, man_valid=True)  
f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil1_ss.arm(man_trig=False, man_valid=True)  
f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil1_ss.arm(man_trig=False, man_valid=True)  

f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil2_ss.arm(man_trig=False, man_valid=True)  
f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil2_ss.arm(man_trig=False, man_valid=True)  
f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil2_ss.arm(man_trig=False, man_valid=True)  
f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil2_ss.arm(man_trig=False, man_valid=True) 

f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil3_ss.arm(man_trig=False, man_valid=True)  
f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil3_ss.arm(man_trig=False, man_valid=True)  
f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil3_ss.arm(man_trig=False, man_valid=True)  
f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_hil3_ss.arm(man_trig=False, man_valid=True) 


# FFT BP Buffer
f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf00_ss.arm(man_trig=False, man_valid=True)  
f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf00_ss.arm(man_trig=False, man_valid=True)  
f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf00_ss.arm(man_trig=False, man_valid=True)  
f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf00_ss.arm(man_trig=False, man_valid=True)  

f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf01_ss.arm(man_trig=False, man_valid=True)  
f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf01_ss.arm(man_trig=False, man_valid=True)  
f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf01_ss.arm(man_trig=False, man_valid=True)  
f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf01_ss.arm(man_trig=False, man_valid=True)  

f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf10_ss.arm(man_trig=False, man_valid=True)  
f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf10_ss.arm(man_trig=False, man_valid=True)  
f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf10_ss.arm(man_trig=False, man_valid=True)  
f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf10_ss.arm(man_trig=False, man_valid=True)  

f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf11_ss.arm(man_trig=False, man_valid=True)  
f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf11_ss.arm(man_trig=False, man_valid=True)  
f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf11_ss.arm(man_trig=False, man_valid=True)  
f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_buf11_ss.arm(man_trig=False, man_valid=True)  



# FFT BP Unscramble Mirror
f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro_ss.arm(man_trig=False, man_valid=False)  
f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro_ss.arm(man_trig=False, man_valid=False)  
f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro_ss.arm(man_trig=False, man_valid=False)  
f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro_ss.arm(man_trig=False, man_valid=False)  

f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro1_ss.arm(man_trig=False, man_valid=False)  
f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro1_ss.arm(man_trig=False, man_valid=False)  
f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro1_ss.arm(man_trig=False, man_valid=False)  
f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro1_ss.arm(man_trig=False, man_valid=False)  

f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro2_ss.arm(man_trig=False, man_valid=False)  
f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro2_ss.arm(man_trig=False, man_valid=False)  
f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro2_ss.arm(man_trig=False, man_valid=False)  
f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro2_ss.arm(man_trig=False, man_valid=False) 

f0.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro3_ss.arm(man_trig=False, man_valid=False)  
f1.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro3_ss.arm(man_trig=False, man_valid=False)  
f2.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro3_ss.arm(man_trig=False, man_valid=False)  
f3.snapshots.pfb_fft_bi_bi_real_unscr_4x_ss_mro3_ss.arm(man_trig=False, man_valid=False) 

# FFT DIR Out
#f0.snapshots.pfb_fft_wideband_real_snap_fftdir_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_wideband_real_snap_fftdir_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_wideband_real_snap_fftdir_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_wideband_real_snap_fftdir_ss.arm(man_trig=False, man_valid=False) 
#
#f0.snapshots.pfb_fft_wideband_real_snap_fftdir1_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_fft_wideband_real_snap_fftdir1_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_fft_wideband_real_snap_fftdir1_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_fft_wideband_real_snap_fftdir1_ss.arm(man_trig=False, man_valid=False) 

# FFT Out
#f0.snapshots.pfb_snap_fft_out_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_snap_fft_out_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_snap_fft_out_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_snap_fft_out_ss.arm(man_trig=False, man_valid=False)  
#
#f0.snapshots.pfb_snap_fft_out1_ss.arm(man_trig=False, man_valid=False)  
#f1.snapshots.pfb_snap_fft_out1_ss.arm(man_trig=False, man_valid=False)  
#f2.snapshots.pfb_snap_fft_out1_ss.arm(man_trig=False, man_valid=False)  
#f3.snapshots.pfb_snap_fft_out1_ss.arm(man_trig=False, man_valid=False)  


d = skarab()

#d.adc_diff()

# CD Output
#d.cd_diff()

# FIR Coefficients 
#d.fir_coeff_diff()

# FIR Internal 
#d.fir_int_diff()

# FIR Output
#d.fir_diff()

# FFT Biplex Core Stage 3 Diff
#d.fft_bp_core_s3_diff()


# FFT Biplex Core Diff
#d.fft_bp_core_diff()

#d.fft_bp_unscramble_ro_diff()

#d.fft_bp_unscramble_logic_diff()

#d.fft_bp_unscramble_hilbert_input_diff()

#d.fft_bp_unscramble_hilbert_internal_diff()

#d.fft_bp_unscramble_hilbert_internal_convert_diff()

#d.fft_bp_unscramble_hilbert_split_diff()

d.fft_bp_unscramble_buffer()


#d.fft_bp_unscramble_hilbert_diff()



# FFT Biplex Diff
#d.fft_bp_diff()






##==============================================================================
#
#plt.figure(1)
#plt.clf()    
#plt.subplot(211)
#plt.plot(adc_data)
#plt.subplot(212)
#plt.semilogy(np.abs(fft_adc_out))
#
#plt.figure(2)
#plt.clf()    
#plt.subplot(211)
#plt.plot(hmc_data)
#plt.subplot(212)
#plt.semilogy(np.abs(fft_hmc_out))

#plt.figure(3)
#plt.clf()
#plt.subplot(211)
#plt.plot(cd_out)
#plt.title('CD')
#plt.subplot(212)
#plt.semilogy(np.abs(fft_cd_out))
#
#plt.figure(4)
#plt.clf()
#plt.subplot(211)
#plt.title('Fir')
#plt.plot(fir_out)
#plt.subplot(212)
#plt.semilogy(np.abs(fft_fir_out))
#
#plt.figure(5)
#plt.clf()
#plt.title('FFT')
#plt.semilogy(np.square(np.abs(fft_complx)))

#plt.figure(6)
#plt.clf()
#plt.title('Quant')
#plt.semilogy(np.square(np.abs(fftQ_complx)))
#
#plt.figure(7)
#plt.clf()
#plt.title('FD')
#plt.semilogy(np.square(np.abs(fd_complx)))

#plt.show()


# Display Count Reset
#print 'Input Sync Count'
#print 'FHost 0'
#print f0.registers.sync_count.read()
#print 'FHost 1'
#print f1.registers.sync_count.read()
#print 'FHost 2'
#print f2.registers.sync_count.read()
#print 'FHost 3'
#print f3.registers.sync_count.read()
#print ' '

#print 'CD Sync Count'
#print 'FHost 0'
#print f0.registers.cd_sync_count.read()
#print 'FHost 1'
#print f1.registers.cd_sync_count.read()
#print 'FHost 2'
#print f2.registers.cd_sync_count.read()
#print 'FHost 3'
#print f3.registers.cd_sync_count.read()
#print ' '

#print 'PFB Sync Count'
#print 'FHost 0'
#print f0.registers.pfb_sync_count.read()
#print 'FHost 1'
#print f1.registers.pfb_sync_count.read()
#print 'FHost 2'
#print f2.registers.pfb_sync_count.read()
#print 'FHost 3'
#print f3.registers.pfb_sync_count.read()
#print ' '

