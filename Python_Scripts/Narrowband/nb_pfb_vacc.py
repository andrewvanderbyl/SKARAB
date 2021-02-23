import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed


host = 'skarab020307-01'

highest_time_msw = 0
highest_time_lsw = 0

#filename = '/home/avanderbyl/fpgs/s_c107m32k_vacc_2021-01-12_1310_current107_vacc_curr_mlib_c70e192_curr_mkat_4689b1.fpg'
filename = '/home/avanderbyl/fpgs/s_c107m32k_vacc_2021-01-18_0922.fpg'

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

print 'Setting Acc Length'
f0.registers.acc_len1.write(reg=np.power(2,16))
# f0.registers.acc_scale.write(reg=0.9)
    
print ' ' 
print 'Arming Snapshots'      
print '================'  
    
f0.snapshots.snap_acc_ss.arm(man_trig=False, man_valid=False)

print ' ' 
print 'Issuing Reset'      

f0.registers.cnt_rst.write(reg='pulse')
# f0.registers.control.write(sys_rst='pulse')

print ' ' 
print 'Reset Done'      

#time.sleep(7)

#==============================================================================

# Grab SS Data for all skarabs

#pfb_snap = f0.snapshots.snap_pfb_ss.read(arm=False)['data'] 
#pfb_snap1 = f0.snapshots.snap_pfb1_ss.read(arm=False)['data'] 

#pfb_real0 = pfb_snap['real0']
#pfb_imag0 = pfb_snap['imag0']
#pfb_real1 = pfb_snap['real1']
#pfb_imag1 = pfb_snap['imag1']
#pfb_real2 = pfb_snap1['real2']
#pfb_imag2 = pfb_snap1['imag2']
#pfb_real3 = pfb_snap1['real3']
#pfb_imag3 = pfb_snap1['imag3']
#
#pfb_real = []
#            
#for x in range(0, len(pfb_real0)):
#    pfb_real.extend(
#        [pfb_real0[x], pfb_real1[x], pfb_real2[x], pfb_real3[x]])
#
#pfb_imag = []
#            
#for x in range(0, len(pfb_imag0)):
#    pfb_imag.extend(
#        [pfb_imag0[x], pfb_imag1[x], pfb_imag2[x], pfb_imag3[x]])
#
#pfb_complx = pfb_real + np.multiply(pfb_imag, 1j)

#==============================================================================
print ' ' 
print 'Grabbing Vacc'  
snap_vacc = f0.snapshots.snap_acc_ss.read(arm=False)['data'] 

vacc = snap_vacc['acc']

#==============================================================================


#plt.figure(1)
#plt.plot(np.abs(pfb_complx))

plt.figure(3)
plt.clf()
plt.plot(vacc)

plt.show()