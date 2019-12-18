import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
from numpy import matrix
import matplotlib.pyplot as plt
from IPython import embed


host = 'skarab020306-01'

filename = '/home/avanderbyl/fpgs/single_port_bram_test_2019-12-18_0935.fpg'

#==============================================================================
#   Classes and methods
#==============================================================================

class skarab_debug: 
               
    def program_fpga(self, f):
        print 'Program FPGA' 
        f.upload_to_ram_and_program(filename)
        f.get_system_information(filename)        
        

    def single_port_debug(self):
        print 'Debug'
        
        ss11 = f0.snapshots.snap_cnt11_ss.read(arm=False)['data']
        bram11_in = ss11['bram_in']
        bram11_out = ss11['bram_out']
        dv11_in = ss11['dv_in']
        dv11_out = ss11['dv_out']
        trig11 = ss11['trig'] 
        
        
        
        filename = 'sp_bram_in' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in bram11_in:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'sp_bram_out' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in bram11_out:
                filehandle.write('%s\n' % listitem)  
        
        Diff = [m - n for m,n in zip(bram11_in,bram11_out)]
        
        filename = 'sp_bram_inout_Diff' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in Diff:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'sp_dv_in' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dv11_in:
                filehandle.write('%s\n' % listitem)  
        
        filename = 'sp_dv_out' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in dv11_out:
                filehandle.write('%s\n' % listitem) 
                
        filename = 'sp_trig' + '.txt'
        print(filename)
        with open(filename, 'w') as filehandle:
            for listitem in trig11:
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

f0.registers.gap_sel.write(sel=0)
f0.registers.gap_len.write(len=0)
f0.registers.gap_scale.write(scale=10)

f0.registers.pkt_sel.write(sel=0)
f0.registers.pkt_len.write(len=4)
f0.registers.pkt_scale.write(scale=10)

#Shift DV in time 
f0.registers.shift.write(addr=4)

# Single Port
f0.snapshots.snap_cnt11_ss.arm(man_trig=False, man_valid=False)  

f0.registers.sys_start.write(en=1)
f0.registers.sys_rst.write(rst='pulse')

d.single_port_debug()