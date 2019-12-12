import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
from numpy import matrix
import matplotlib.pyplot as plt
from IPython import embed


host = 'skarab020306-01'

filename = '/home/avanderbyl/fpgs/single_port_bram_test_2019-12-09_1522.fpg'

#==============================================================================
#   Classes and methods
#==============================================================================

class skarab_debug: 
               
    def program_fpga(self, f):
        print 'Program FPGA' 
        f.upload_to_ram_and_program(filename)
        f.get_system_information(filename)        
        

    def single_port_debug(self):
#        ss0 = f0.snapshots.snap_cnt_ss.read(arm=False)['data']
#        bram0_in = ss0['bram_in']
#        bram0_out = ss0['bram_out']
#        dv0_in = ss0['dv_in']
#        dv0_out = ss0['dv_out']
#        trig0 = ss0['trig']
#        
#        ss1 = f0.snapshots.snap_cnt1_ss.read(arm=False)['data']
#        bram1_in = ss1['bram_in']
#        bram1_out = ss1['bram_out']
#        dv1_in = ss1['dv_in']
#        dv1_out = ss1['dv_out']
#        trig1 = ss1['trig']
#        
#        ss2 = f0.snapshots.snap_cnt2_ss.read(arm=False)['data']
#        bram2_in = ss2['bram_in']
#        bram2_out = ss2['bram_out']
#        dv2_in = ss2['dv_in']
#        dv2_out = ss2['dv_out']
#        trig2 = ss2['trig']
#        
#        ss3 = f0.snapshots.snap_cnt3_ss.read(arm=False)['data']
#        bram3_in = ss3['bram_in']
#        bram3_out = ss3['bram_out']
#        dv3_in = ss3['dv_in']
#        dv3_out = ss3['dv_out']
#        trig3 = ss3['trig']
#        
#        ss4 = f0.snapshots.snap_cnt4_ss.read(arm=False)['data']
#        bram4_in = ss4['bram_in']
#        bram4_out = ss4['bram_out']
#        dv4_in = ss4['dv_in']
#        dv4_out = ss4['dv_out']
#        trig4 = ss4['trig']              
#        
#        
#        ss5 = f0.snapshots.snap_cnt5_ss.read(arm=False)['data']
#        bram5_in = ss5['bram_in']
#        bram5_out = ss5['bram_out']
#        dv5_in = ss5['dv_in']
#        dv5_out = ss5['dv_out']
#        trig5 = ss5['trig']    
#             
#        ss6 = f0.snapshots.snap_cnt6_ss.read(arm=False)['data']
#        bram6_in = ss6['bram_in']
#        bram6_out = ss6['bram_out']
#        dv6_in = ss6['dv_in']
#        dv6_out = ss6['dv_out']
#        trig6 = ss6['trig']    
#        
#        ss7 = f0.snapshots.snap_cnt7_ss.read(arm=False)['data']
#        bram7_in = ss7['bram_in']
#        bram7_out = ss7['bram_out']
#        dv7_in = ss7['dv_in']
#        dv7_out = ss7['dv_out']
#        trig7 = ss7['trig']   

        ss11 = f0.snapshots.snap_cnt11_ss.read(arm=False)['data']
        bram11_in = ss11['bram_in']
        bram11_out = ss11['bram_out']
        dv11_in = ss11['dv_in']
        dv11_out = ss11['dv_out']
        trig11 = ss11['trig'] 
        
        ss12 = f0.snapshots.snap_cnt12_ss.read(arm=False)['data']
        bram12_in = ss12['bram_in']
        bram12_out = ss12['bram_out']
        dv12_in = ss12['dv_in']
        dv12_out = ss12['dv_out']
        trig12 = ss12['trig']     

#        ss13 = f0.snapshots.snap_cnt13_ss.read(arm=False)['data']
#        bram13_in = ss13['bram_in']
#        bram13_out = ss13['bram_out']
#        dv13_in = ss13['dv_in']
#        dv13_out = ss13['dv_out']
#        trig13 = ss13['trig']   
        
#        filename = 'SPBRAM' + '_bram0_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram0_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_bram0_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram0_out:
#                filehandle.write('%s\n' % listitem)  
#        
#        Diff = [m - n for m,n in zip(bram0_in,bram0_out)]
#        
#        filename = 'SPBRAM' + '_bram0_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv0_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv0_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv0_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv0_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'SPBRAM' + '_trig0' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in trig0:
#                filehandle.write('%s\n' % listitem)          
#        
#        # ----------------------------------------------------------------------------
#        
#        filename = 'SPBRAM' + '_bram1_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram1_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_bram1_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram1_out:
#                filehandle.write('%s\n' % listitem)  
#                
#        Diff = [m - n for m,n in zip(bram1_in,bram1_out)]
#        
#        filename = 'SPBRAM' + '_bram1_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv1_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv1_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv1_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv1_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'SPBRAM' + '_trig1' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in trig1:
#                filehandle.write('%s\n' % listitem)  
#        
#        
#        # ----------------------------------------------------------------------------
#        
#        filename = 'SPBRAM' + '_bram2_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram2_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_bram2_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram2_out:
#                filehandle.write('%s\n' % listitem)  
#        
#        Diff = [m - n for m,n in zip(bram2_in,bram2_out)]
#        
#        filename = 'SPBRAM' + '_bram2_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv2_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv2_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv2_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv2_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'SPBRAM' + '_trig2' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in trig2:
#                filehandle.write('%s\n' % listitem)  
#        
#        
#        # ----------------------------------------------------------------------------
#        
#        filename = 'SPBRAM' + '_bram3_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram3_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_bram3_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram3_out:
#                filehandle.write('%s\n' % listitem)  
#        
#        Diff = [m - n for m,n in zip(bram3_in,bram3_out)]
#        
#        filename = 'SPBRAM' + '_bram3_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv3_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv3_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv3_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv3_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'SPBRAM' + '_trig3' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in trig3:
#                filehandle.write('%s\n' % listitem)  
#        
#        
#        # ----------------------------------------------------------------------------
#        
#        filename = 'SPBRAM' + '_bram4_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram4_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_bram4_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram4_out:
#                filehandle.write('%s\n' % listitem)  
#        
#        
#        Diff = [m - n for m,n in zip(bram4_in,bram4_out)]
#        
#        filename = 'SPBRAM' + '_bram4_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv4_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv4_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv4_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv4_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'SPBRAM' + '_trig4' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in trig4:
#                filehandle.write('%s\n' % listitem)  
#        
#        # ----------------------------------------------------------------------------
#        
#        filename = 'SPBRAM' + '_bram5_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram5_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_bram5_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram5_out:
#                filehandle.write('%s\n' % listitem)  
#                
#        Diff = [m - n for m,n in zip(bram5_in,bram5_out)]
#        
#        filename = 'SPBRAM' + '_bram5_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)         
#        
#        filename = 'SPBRAM' + '_dv5_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv5_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv5_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv5_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'SPBRAM' + '_trig5' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in trig5:
#                filehandle.write('%s\n' % listitem)  
#        
#        
#        
#        # ----------------------------------------------------------------------------
#        
#        filename = 'SPBRAM' + '_bram6_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram6_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_bram6_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram6_out:
#                filehandle.write('%s\n' % listitem)  
#        
#        Diff = [m - n for m,n in zip(bram6_in,bram6_out)]
#        
#        filename = 'SPBRAM' + '_bram6_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv6_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv6_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv6_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv6_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'SPBRAM' + '_trig6' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in trig6:
#                filehandle.write('%s\n' % listitem)  
#        
#        # ----------------------------------------------------------------------------
#        
#        filename = 'SPBRAM' + '_bram7_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram7_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_bram7_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram7_out:
#                filehandle.write('%s\n' % listitem)  
#        
#        Diff = [m - n for m,n in zip(bram7_in,bram7_out)]
#        
#        filename = 'SPBRAM' + '_bram7_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv7_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv7_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'SPBRAM' + '_dv7_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv7_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'SPBRAM' + '_trig7' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in trig7:
#                filehandle.write('%s\n' % listitem) 
#                
        # ----------------------------------------------------------------------------
        
#        filename = 'sp_bram8_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram8_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'sp_bram8_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram8_out:
#                filehandle.write('%s\n' % listitem)  
#        
#        Diff = [m - n for m,n in zip(bram8_in,bram8_out)]
#        
#        filename = 'sp_bram8_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'sp_dv8_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv8_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'sp_dv8_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv8_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'sp_trig8' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in trig8:
#                filehandle.write('%s\n' % listitem)         
#
#        # ----------------------------------------------------------------------------
#        
#        filename = 'sp_bram9_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram9_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'sp_bram9_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram9_out:
#                filehandle.write('%s\n' % listitem)  
#        
#        Diff = [m - n for m,n in zip(bram9_in,bram9_out)]
#        
#        filename = 'sp_bram9_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'sp_dv9_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv9_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'sp_dv9_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv9_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'sp_trig9' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in trig9:
#                filehandle.write('%s\n' % listitem)         
#
#        # ----------------------------------------------------------------------------
#        
#        filename = 'sp_bram10_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram10_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'sp_bram10_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram10_out:
#                filehandle.write('%s\n' % listitem)  
#        
#        Diff = [m - n for m,n in zip(bram10_in,bram10_out)]
#        
#        filename = 'sp_bram10_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'sp_dv10_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv10_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'sp_dv10_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv10_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'sp_trig10' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in trig10:
#                filehandle.write('%s\n' % listitem)         


        # ----------------------------------------------------------------------------
        
        filename = 'sp_bram11_in' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in bram11_in:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'sp_bram11_out' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in bram11_out:
                filehandle.write('%s\n' % listitem)  
        
        Diff = [m - n for m,n in zip(bram11_in,bram11_out)]
        
        filename = 'sp_bram11_inout_Diff' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in Diff:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'sp_dv11_in' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dv11_in:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'sp_dv11_out' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dv11_out:
                filehandle.write('%s\n' % listitem) 
                
        filename = 'sp_trig11' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in trig11:
                filehandle.write('%s\n' % listitem)   

        # ----------------------------------------------------------------------------
        
        filename = 'sp_bram12_in' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in bram12_in:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'sp_bram12_out' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in bram12_out:
                filehandle.write('%s\n' % listitem)  
        
        Diff = []
        Diff = [m - n for m,n in zip(bram12_in,bram12_out)]
        
        filename = 'sp_bram12_inout_Diff' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in Diff:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'sp_dv12_in' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dv12_in:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'sp_dv12_out' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dv12_out:
                filehandle.write('%s\n' % listitem) 
                
        filename = 'sp_trig12' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in trig12:
                filehandle.write('%s\n' % listitem)   


        # ----------------------------------------------------------------------------
        
#        filename = 'sp_bram13_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram13_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'sp_bram13_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in bram13_out:
#                filehandle.write('%s\n' % listitem)  
#        
#        Diff = []
#        Diff = [m - n for m,n in zip(bram13_in,bram13_out)]
#        
#        filename = 'sp_bram13_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'sp_dv13_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv13_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'sp_dv13_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dv13_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'sp_trig13' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in trig13:
#                filehandle.write('%s\n' % listitem)   


        # ----------------------------------------------------------------------------
        
    def dual_port_debug(self):
#        dp_ss1 = f0.snapshots.snap_dp1_ss.read(arm=False)['data']
#        dp_bram1_in = dp_ss1['bram_in']
#        dp_bram1_out = dp_ss1['bram_out']
#        dp_dv1_in = dp_ss1['dv_in']
#        dp_dv1_out = dp_ss1['dv_out']
#        dp_trig1 = dp_ss1['trig']    
#
#        dp_ss2 = f0.snapshots.snap_dp2_ss.read(arm=False)['data']
#        dp_bram2_in = dp_ss2['bram_in']
#        dp_bram2_out = dp_ss2['bram_out']
#        dp_dv2_in = dp_ss2['dv_in']
#        dp_dv2_out = dp_ss2['dv_out']
#        dp_trig2 = dp_ss2['trig']  
        
        dp_ss3 = f0.snapshots.snap_dp3_ss.read(arm=False)['data']
        dp_bram3_in = dp_ss3['bram_in']
        dp_bram3_out = dp_ss3['bram_out']
        dp_dv3_in = dp_ss3['dv_in']
        dp_dv3_out = dp_ss3['dv_out']
        dp_trig3 = dp_ss3['trig']          
        
        dp_ss4 = f0.snapshots.snap_dp4_ss.read(arm=False)['data']
        dp_bram4_in = dp_ss4['bram_in']
        dp_bram4_out = dp_ss4['bram_out']
        dp_dv4_in = dp_ss4['dv_in']
        dp_dv4_out = dp_ss4['dv_out']
        dp_trig4 = dp_ss4['trig']    

#        dp_ss5 = f0.snapshots.snap_dp5_ss.read(arm=False)['data']
#        dp_bram5_in = dp_ss5['bram_in']
#        dp_bram5_out = dp_ss5['bram_out']
#        dp_dv5_in = dp_ss5['dv_in']
#        dp_dv5_out = dp_ss5['dv_out']
#        dp_trig5 = dp_ss5['trig']    
#
#        dp_ss6 = f0.snapshots.snap_dp6_ss.read(arm=False)['data']
#        dp_bram6_in = dp_ss6['bram_in']
#        dp_bram6_out = dp_ss6['bram_out']
#        dp_dv6_in = dp_ss6['dv_in']
#        dp_dv6_out = dp_ss6['dv_out']
#        dp_trig6 = dp_ss6['trig']    
#
#        dp_ss7 = f0.snapshots.snap_dp7_ss.read(arm=False)['data']
#        dp_bram7_in = dp_ss7['bram_in']
#        dp_bram7_out = dp_ss7['bram_out']
#        dp_dv7_in = dp_ss7['dv_in']
#        dp_dv7_out = dp_ss7['dv_out']
#        dp_trig7 = dp_ss7['trig']   
#
#        dp_ss8 = f0.snapshots.snap_dp8_ss.read(arm=False)['data']
#        dp_bram8_in = dp_ss8['bram_in']
#        dp_bram8_out = dp_ss8['bram_out']
#        dp_dv8_in = dp_ss8['dv_in']
#        dp_dv8_out = dp_ss8['dv_out']
#        dp_trig8 = dp_ss8['trig']


#        filename = 'dp_bram1_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dp_bram1_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'dp_bram1_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dp_bram1_out:
#                filehandle.write('%s\n' % listitem)  
#        
#        Diff = [m - n for m,n in zip(dp_bram1_in,dp_bram1_out)]
#        
#        filename = 'dp_bram1_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'dp_dv1_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dp_dv1_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'dp_dv1_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dp_dv1_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'dp_trig1' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dp_trig1:
#                filehandle.write('%s\n' % listitem)    
#
## ----------------------------------------------------------------------------
#
#        filename = 'dp_bram2_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dp_bram2_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'dp_bram2_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dp_bram2_out:
#                filehandle.write('%s\n' % listitem)  
#        
#        Diff = [m - n for m,n in zip(dp_bram2_in,dp_bram2_out)]
#        
#        filename = 'dp_bram2_inout_Diff' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in Diff:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'dp_dv2_in' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dp_dv2_in:
#                filehandle.write('%s\n' % listitem)  
#        
#        filename = 'dp_dv2_out' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dp_dv2_out:
#                filehandle.write('%s\n' % listitem) 
#                
#        filename = 'dp_trig2' + '.txt'
#        print(filename)
#        with open(filename, 'w') as filehandle:
#            for listitem in dp_trig2:
#                filehandle.write('%s\n' % listitem)  
#          
# ----------------------------------------------------------------------------

        filename = 'dp_bram3_in' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dp_bram3_in:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'dp_bram3_out' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dp_bram3_out:
                filehandle.write('%s\n' % listitem)  
        
        Diff = [m - n for m,n in zip(dp_bram3_in,dp_bram3_out)]
        
        filename = 'dp_bram3_inout_Diff' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in Diff:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'dp_dv3_in' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dp_dv3_in:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'dp_dv3_out' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dp_dv3_out:
                filehandle.write('%s\n' % listitem) 
                
        filename = 'dp_trig3' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dp_trig3:
                filehandle.write('%s\n' % listitem)        
                

# ----------------------------------------------------------------------------

        filename = 'dp_bram4_in' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dp_bram4_in:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'dp_bram4_out' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dp_bram4_out:
                filehandle.write('%s\n' % listitem)  
        
        Diff = [m - n for m,n in zip(dp_bram4_in,dp_bram4_out)]
        
        filename = 'dp_bram4_inout_Diff' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in Diff:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'dp_dv4_in' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dp_dv4_in:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'dp_dv4_out' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dp_dv4_out:
                filehandle.write('%s\n' % listitem) 
                
        filename = 'dp_trig4' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dp_trig4:
                filehandle.write('%s\n' % listitem)            
                
#==============================================================================
# End of classes and methods
#==============================================================================
      
d = skarab_debug()

f0 = casperfpga.CasperFpga(host)
#d.program_fpga(f0)
f0.get_system_information(filename)

print 'Setup Done'

f0.registers.sys_start.write(en=0)
f0.registers.sys_rst.write(rst='pulse')


# Setup packet length and gap size
f0.registers.gap_offset.write(offset=0)
f0.registers.pkt_len.write(len=2)

# Single Port

#f0.snapshots.snap_cnt_ss.arm(man_trig=False, man_valid=True)  
#
#f0.snapshots.snap_cnt1_ss.arm(man_trig=False, man_valid=True)  
#
#f0.snapshots.snap_cnt2_ss.arm(man_trig=False, man_valid=True)  
#
#f0.snapshots.snap_cnt3_ss.arm(man_trig=False, man_valid=True) 
#
#f0.snapshots.snap_cnt4_ss.arm(man_trig=False, man_valid=True) 
#
#f0.snapshots.snap_cnt5_ss.arm(man_trig=False, man_valid=True) 
#
#f0.snapshots.snap_cnt6_ss.arm(man_trig=False, man_valid=True) 
#
#f0.snapshots.snap_cnt7_ss.arm(man_trig=False, man_valid=True) 

f0.snapshots.snap_cnt11_ss.arm(man_trig=False, man_valid=True)

f0.snapshots.snap_cnt12_ss.arm(man_trig=False, man_valid=True)

#f0.snapshots.snap_cnt13_ss.arm(man_trig=False, man_valid=True)

# Dual Port
#f0.snapshots.snap_dp1_ss.arm(man_trig=False, man_valid=True)  
#
#f0.snapshots.snap_dp2_ss.arm(man_trig=False, man_valid=True)  

f0.snapshots.snap_dp3_ss.arm(man_trig=False, man_valid=True)  

f0.snapshots.snap_dp4_ss.arm(man_trig=False, man_valid=True) 

#f0.snapshots.snap_dp5_ss.arm(man_trig=False, man_valid=True) 
#
#f0.snapshots.snap_dp6_ss.arm(man_trig=False, man_valid=True) 
#
#f0.snapshots.snap_dp7_ss.arm(man_trig=False, man_valid=True) 
#
#f0.snapshots.snap_dp8_ss.arm(man_trig=False, man_valid=True) 


f0.registers.sys_start.write(en=1)
f0.registers.sys_rst.write(rst='pulse')


# Run Single Port    
d.single_port_debug()
d.dual_port_debug()           


f0.registers.sys_start.write(en=0)
