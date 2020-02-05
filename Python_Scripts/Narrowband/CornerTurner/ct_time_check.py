import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

hosts = ['skarab020a03-01','skarab020918-01','skarab02091b-01','skarab020A45-01']
StartIdx = 0
EndIdx = 100

CT_debug = True
Qout_debug = False
Tag_debug = True

print(hosts)

c=corr2.fxcorrelator.FxCorrelator('bob',config_source='/etc/corr/avdbyl_nb_107_32k.ini')
c.initialise(program=False,configure=False,require_epoch=False)

f0 = c.fhosts[0]
f1 = c.fhosts[1]
f2 = c.fhosts[2]
f3 = c.fhosts[3]

def CT_SS(ct_snap):
    print('Sync:'+str(ct_snap['sync'][StartIdx:EndIdx]))
    print(' ')
    print('DV:'+str(ct_snap['dv'][StartIdx:EndIdx]))
    print(' ')
    print('Data:'+str(ct_snap['data'][StartIdx:EndIdx]))
    print(' ')
    print('Time:'+str(ct_snap['time'][StartIdx:EndIdx]))
    print(' ')
    print('Time Diff:'+str(ct_snap['time_diff'][StartIdx:EndIdx]))
    print(' ')
    print('Freq:'+str(ct_snap['freq'][StartIdx:EndIdx]))
    print(' ')
    print('PktStart:'+str(ct_snap['pktstart'][StartIdx:EndIdx]))
    print(' ')

def Tag_SS(tag_snap):
    print('Tag Sync:'+str(tag_snap['sync'][StartIdx:EndIdx]))
    print(' ')
    print('Tag DV:'+str(tag_snap['dv'][StartIdx:EndIdx]))
    print(' ')
    print('Tag Tag:'+str(tag_snap['tag'][StartIdx:EndIdx]))
    print(' ')
    print('Tag Data:'+str(tag_snap['data'][StartIdx:EndIdx]))
    print(' ')
    print('Tag Time:'+str(tag_snap['time'][StartIdx:EndIdx]))
    print(' ')
    print('Tag rd_rdy:'+str(tag_snap['rd_rdy'][StartIdx:EndIdx]))
    print(' ')

def Qout_SS(qout_snap):
    print('Qout Sync:'+str(qout_snap['sync'][StartIdx:EndIdx]))
    print(' ')
    print('QOut DV:'+str(qout_snap['dv'][StartIdx:EndIdx]))
    print(' ')
    print('Qout Data:'+str(qout_snap['data'][StartIdx:EndIdx]))
    print(' ')
    print('QOut Time:'+str(qout_snap['time'][StartIdx:EndIdx]))
    print(' ')

def HMC_SS(hmc_snap):
    print('HMC Sync:'+str(hmc_snap['sync'][StartIdx:EndIdx]))
    print(' ')
    print('HMC DV:'+str(hmc_snap['dv'][StartIdx:EndIdx]))
    print(' ')
    print('HMC Data:'+str(hmc_snap['data_hmc'][StartIdx:EndIdx]))
    print(' ')
    print('HMC Time:'+str(hmc_snap['time_hmc'][StartIdx:EndIdx]))
    print(' ')

def Proc_SS(proc_snap):
    print('Proc Sync:'+str(proc_snap['sync'][StartIdx:EndIdx]))
    print(' ')
    print('Proc DV:'+str(proc_snap['dv'][StartIdx:EndIdx]))
    print(' ')
    print('Proc Data:'+str(proc_snap['data_proc'][StartIdx:EndIdx]))
    print(' ')
    print('Proc Time:'+str(proc_snap['time_proc'][StartIdx:EndIdx]))
    print(' ')

# Arm Snapshots
f0.snapshots.snap_ctout_ss.arm(man_trig=False, man_valid=False)
f1.snapshots.snap_ctout_ss.arm(man_trig=False, man_valid=False)
f2.snapshots.snap_ctout_ss.arm(man_trig=False, man_valid=False)
f3.snapshots.snap_ctout_ss.arm(man_trig=False, man_valid=False)

if Qout_debug:
    f0.snapshots.snap_qout_ss.arm(man_trig=False, man_valid=False)
    f1.snapshots.snap_qout_ss.arm(man_trig=False, man_valid=False)
    f2.snapshots.snap_qout_ss.arm(man_trig=False, man_valid=False)
    f3.snapshots.snap_qout_ss.arm(man_trig=False, man_valid=False)

    print("Setting SS ctrl reg to 0")
    f0.registers.snap_qout_ss_ctrl.write_int(0) 
    f1.registers.snap_qout_ss_ctrl.write_int(0)
    f2.registers.snap_qout_ss_ctrl.write_int(0)
    f3.registers.snap_qout_ss_ctrl.write_int(0)

if Tag_debug:
    f0.snapshots.hmc_ct_snap_tag_ss.arm(man_trig=False, man_valid=False)
    f1.snapshots.hmc_ct_snap_tag_ss.arm(man_trig=False, man_valid=False)
    f2.snapshots.hmc_ct_snap_tag_ss.arm(man_trig=False, man_valid=False)
    f3.snapshots.hmc_ct_snap_tag_ss.arm(man_trig=False, man_valid=False)

    f0.snapshots.hmc_ct_obuf_snap_hmc_ss.arm(man_trig=False, man_valid=False)
    f1.snapshots.hmc_ct_obuf_snap_hmc_ss.arm(man_trig=False, man_valid=False)
    f2.snapshots.hmc_ct_obuf_snap_hmc_ss.arm(man_trig=False, man_valid=False)
    f3.snapshots.hmc_ct_obuf_snap_hmc_ss.arm(man_trig=False, man_valid=False)

    f0.snapshots.hmc_ct_obuf_snap_proc_ss.arm(man_trig=False, man_valid=False)
    f1.snapshots.hmc_ct_obuf_snap_proc_ss.arm(man_trig=False, man_valid=False)
    f2.snapshots.hmc_ct_obuf_snap_proc_ss.arm(man_trig=False, man_valid=False)
    f3.snapshots.hmc_ct_obuf_snap_proc_ss.arm(man_trig=False, man_valid=False)

# Issue Reset
c.fops.sys_reset()

# Print Status Registers
print(f0.registers.hmc_ct_status0.read())
print(f1.registers.hmc_ct_status0.read())
print(f2.registers.hmc_ct_status0.read())
print(f3.registers.hmc_ct_status0.read())
print("--------------------------------")

print(f0.registers.hmc_ct_status1.read())
print(f1.registers.hmc_ct_status1.read())
print(f2.registers.hmc_ct_status1.read())
print(f3.registers.hmc_ct_status1.read())
print("--------------------------------")

print(f0.registers.hmc_ct_status2.read())
print(f1.registers.hmc_ct_status2.read())
print(f2.registers.hmc_ct_status2.read())
print(f3.registers.hmc_ct_status2.read())
print("--------------------------------")

# Read Snapshots
if CT_debug:
    f0_ct_snap = f0.snapshots.snap_ctout_ss.read(arm=False)['data']
    f1_ct_snap = f1.snapshots.snap_ctout_ss.read(arm=False)['data']
    f2_ct_snap = f2.snapshots.snap_ctout_ss.read(arm=False)['data']
    f3_ct_snap = f3.snapshots.snap_ctout_ss.read(arm=False)['data']

if Qout_debug:
    f0_qout_snap = f0.snapshots.snap_qout_ss.read(arm=False)['data']
    f1_qout_snap = f1.snapshots.snap_qout_ss.read(arm=False)['data']
    f2_qout_snap = f2.snapshots.snap_qout_ss.read(arm=False)['data']
    f3_qout_snap = f3.snapshots.snap_qout_ss.read(arm=False)['data']

if Tag_debug:
    f0_tag_snap = f0.snapshots.hmc_ct_snap_tag_ss.read(arm=False)['data']
    f1_tag_snap = f1.snapshots.hmc_ct_snap_tag_ss.read(arm=False)['data']
    f2_tag_snap = f2.snapshots.hmc_ct_snap_tag_ss.read(arm=False)['data']
    f3_tag_snap = f3.snapshots.hmc_ct_snap_tag_ss.read(arm=False)['data']
    
    f0_hmc_snap = f0.snapshots.hmc_ct_obuf_snap_hmc_ss.read(arm=False)['data']
    f1_hmc_snap = f1.snapshots.hmc_ct_obuf_snap_hmc_ss.read(arm=False)['data']
    f2_hmc_snap = f2.snapshots.hmc_ct_obuf_snap_hmc_ss.read(arm=False)['data']
    f3_hmc_snap = f3.snapshots.hmc_ct_obuf_snap_hmc_ss.read(arm=False)['data']

    f0_proc_snap = f0.snapshots.hmc_ct_obuf_snap_proc_ss.read(arm=False)['data']
    f1_proc_snap = f1.snapshots.hmc_ct_obuf_snap_proc_ss.read(arm=False)['data']
    f2_proc_snap = f2.snapshots.hmc_ct_obuf_snap_proc_ss.read(arm=False)['data']
    f3_proc_snap = f3.snapshots.hmc_ct_obuf_snap_proc_ss.read(arm=False)['data']

print("FHost0")
print("------")
#f0_ct_snap = f0.snapshots.snap_ctout_ss.read()['data']
#f0_qout_snap = f0.snapshots.snap_qout_ss.read(arm=False)['data']
CT_SS(f0_ct_snap)
Tag_SS(f0_tag_snap)
HMC_SS(f0_hmc_snap)
Proc_SS(f0_proc_snap)
#Qout_SS(f0_qout_snap)

print('======================================================================================================================')
print(' ')

#-----------------------------------------------------------------------------
print("FHost1")
print("------")
# f1_ct_snap = f1.snapshots.snap_ctout_ss.read(read_nowait=True)
# f1_qout_snap = f1.snapshots.snap_qout_ss.read(arm=False, read_nowait=True)
#CT_SS(f1_ct_snap)
#Tag_SS(f1_tag_snap)
#Qout_SS(f1_qout_snap)
print('======================================================================================================================')
print(' ')

#-----------------------------------------------------------------------------
print("FHost2")
print("------")
# f2_ct_snap = f2.snapshots.snap_ctout_ss.read(read_nowait=True)
# f2_qout_snap = f2.snapshots.snap_qout_ss.read(arm=False, read_nowait=True)
#CT_SS(f2_ct_snap)
#Tag_SS(f2_tag_snap)
#Qout_SS(f2_qout_snap)
print('======================================================================================================================')
print(' ')

#-----------------------------------------------------------------------------
print("FHost3")
print("------")
# f3_ct_snap = f3.snapshots.snap_ctout_ss.read(read_nowait=True)
# f3_qout_snap = f3.snapshots.snap_qout_ss.read(arm=False, read_nowait=True)
#CT_SS(f3_ct_snap)
#Tag_SS(f3_tag_snap)
#Qout_SS(f3_qout_snap)






# f0_time = f0_ct_snap['data']['time'][1]
# f1_time = f1_ct_snap['data']['time'][1]
# f2_time = f2_ct_snap['data']['time'][1]
# f3_time = f3_ct_snap['data']['time'][1]

# print("CT Time Diffs")
# print("f0 vs f1")
# print((f0_time-f1_time)/(16))

# print("f0 vs f2")
# print((f0_time-f2_time)/(16))

# print("f0 vs f3")
# print((f0_time-f3_time)/(16))

# print("--------------------------------------------")
# print("f1 vs f2")
# print((f1_time-f2_time)/(16))

# print("f1 vs f3")
# print((f1_time-f3_time)/(16))

# print("--------------------------------------------")

# print("f2 vs f3")
# print((f2_time-f3_time)/(16))







