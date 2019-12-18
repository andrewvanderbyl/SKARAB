import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed


host = 'skarab020509-01'

highest_time_msw = 0
highest_time_lsw = 0

filename = '/home/avanderbyl/fpgs/bram_check_dualport_2019-11-19_1525.fpg'

#==============================================================================
#   Classes and methods
#==============================================================================

class skarab_debug: 
               
    def program_fpga(self, f):
        print 'Program FPGA' 
        f.upload_to_ram_and_program(filename)
        f.get_system_information(filename)        
        

#==============================================================================
# End of classes and methods
#==============================================================================
      
d = skarab_debug()

f0 = casperfpga.CasperFpga(host)
#d.program_fpga(f0)
f0.get_system_information(filename)

f0.snapshots.ss_dp_ss.arm(man_trig=True, man_valid=False)  
#ss = f0.snapshots.ss_dp_ss.read(arm=False)['data']

f0.snapshots.ss_dp_ss.print_snap(man_trig=True)

count = 0
while (count < 2):
    count = count + 1
    
    print 'DP0A'
    ss = f0.snapshots.ss_dp_ss.read(arm=False)['data']
    dp0A = ss['dp0A']
    dp1A = ss['dp1A']
    
    dp0B0 = ss['dp0B0']
    dp0B1 = ss['dp0B1']
    
    dp1B0 = ss['dp1B0']
    dp1B1 = ss['dp1B1']
    

    plt.figure(1)
    plt.clf()
    plt.plot(dp1B0)
    
    plt.figure(2)
    plt.clf()
    plt.plot(dp1B1)
       
  
    plt.show()