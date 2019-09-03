import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

HOST = 'skarab020304-01'

f = casperfpga.CasperFpga(HOST)
#f.upload_to_ram_and_program('/home/avanderbyl/fpgs/fsfd_sim_2019-05-14_1447.fpg')
#f.get_system_information('/home/avanderbyl/fpgs/fsfd_sim_2019-05-14_1447.fpg')

#f.upload_to_ram_and_program('/home/avanderbyl/fpgs/fsfd_sim_2019-05-17_1252.fpg')
f.get_system_information('/home/avanderbyl/fpgs/fsfd_sim_2019-05-17_1252.fpg')
    
# *** Setting Registers ***
print 'Setting Registers'   
f.registers.delay_whole0.write(initial=5)
f.registers.delay_frac0.write(initial=0.5)
f.registers.delta_delay_whole0.write(initial=1)
f.registers.delta_delay_frac0.write(initial=0.0)
f.registers.phase0.write(initial=0)
f.registers.phase0.write(delta=0)

freq = ((749e6+53.5e6)*np.power(2,22))/1712e6
f.registers.freq_cwg_osc1.write(frequency=freq)

# *** Arm Snapshots ***
print 'Arming Snapshots'    

f.snapshots.phase_compensation1_fd_fs_ss_fd_fs_ss.arm(man_trig=True, man_valid=True)
f.snapshots.phase_compensation1_delay_gen_delay_gen_delay_calc_ss_delay_calc_ss.arm(man_trig=True, man_valid=True)
f.snapshots.phase_compensation1_delay_gen_delay_gen_delay_calc_ss_delay_coeff_ss.arm(man_trig=True, man_valid=True)
f.snapshots.phase_compensation1_delay_gen_ss_inputs_ss.arm(man_trig=True, man_valid=True)

f.registers.tl_cd0_control0.write(load_immediate='pulse')
f.registers.tl_cd0_control0.write(arm='pulse')
f.registers.control.write(cnt_rst='pulse')
f.registers.control.write(sys_rst='pulse')
f.registers.sys_en.write(en=1)


# *** Read back registers ***
print 'Read Back Registers'   
print f.registers.tl_fd0_status.read()
print f.registers.phase_compensation1_delay_msw.read()
print f.registers.phase_compensation1_delay_lsw.read()
print f.registers.phase_compensation1_dt_delay_msw.read()
print f.registers.phase_compensation1_dt_delay_lsw.read()
print f.registers.phase_compensation1_phase.read()
print f.registers.phase_compensation1_dt_phase.read()

# *** Read Snapshots ***
print 'Read SS'   
inputs = f.snapshots.phase_compensation1_delay_gen_ss_inputs_ss.read(arm=False)['data']
delay_calc = f.snapshots.phase_compensation1_delay_gen_delay_gen_delay_calc_ss_delay_calc_ss.read(arm=False)['data']
delay_coeff = f.snapshots.phase_compensation1_delay_gen_delay_gen_delay_calc_ss_delay_coeff_ss.read(arm=False)['data']
fd_fs = f.snapshots.phase_compensation1_fd_fs_ss_fd_fs_ss.read(arm=False)['data']


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

#------------------------------------------------------------------------------
#                           Figures
#------------------------------------------------------------------------------
    
plt.figure(1)
plt.clf()
plt.subplot(811)
plt.plot(input_sync)
plt.subplot(812)
plt.plot(input_init)
plt.subplot(813)
plt.plot(input_idx)
plt.subplot(814)
plt.plot(input_en)
plt.subplot(815)
plt.plot(input_load)
plt.subplot(816)
plt.plot(input_phase)
plt.subplot(817)
plt.plot(input_dt_phase)
plt.subplot(818)
plt.plot(input_delay)

plt.figure(2)
plt.clf()    
plt.subplot(411)
plt.plot(delay_calc_sel)
plt.subplot(412)
plt.plot(delay_calc_val)
plt.subplot(413)
plt.plot(delay_calc_update)
plt.subplot(414)
plt.plot(delay_calc_val_inc)

plt.figure(3)
plt.clf()    
plt.subplot(211)
plt.plot(delay_calc_sel)
plt.subplot(212)
plt.plot(delay_coeff_coeff)

plt.figure(4)
plt.clf()    
plt.subplot(511)
plt.plot(fd_fs_sync)
plt.subplot(512)
plt.plot(fd_fs_x)
plt.subplot(513)
plt.plot(fd_fs_a0)
plt.subplot(514)
plt.plot(fd_fs_a1)
plt.subplot(515)
plt.plot(fd_fs_cos)


plt.show()    
    
