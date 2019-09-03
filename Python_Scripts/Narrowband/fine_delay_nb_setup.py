import time, corr2, casperfpga, sys, struct, pylab, logging; logging.basicConfig(level=logging.INFO)
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

time.sleep(0.2)

hosts = ['skarab020303-01', 'skarab020308-01', 'skarab02030A-01', 'skarab02030E-01']
c=corr2.fxcorrelator.FxCorrelator('bob', config_source='/etc/corr/avdbyl_test_dbelab06_4a_256_new.ini')
c.initialise(program=False, configure=False, require_epoch=False)

f0 = c.fhosts[0]
f1 = c.fhosts[1]
f2 = c.fhosts[2]
f3 = c.fhosts[3]

print "Checking Current Set Values"
print "---------------------------"

print "fhost: %s" % f0
print f0.registers.delay_whole0.read()
print f0.registers.delay_frac0.read()
print f0.registers.delta_delay_whole0.read()
print f0.registers.delta_delay_frac0.read()
print f0.registers.phase0.read()

print 'Loading Delays'
currtime = time.time()
loadtime = currtime + 400
c.fops.delay_set('ant0x', loadtime=loadtime, delay=(4.0/1712e6), delay_delta=0.5, phase=0.5, phase_delta=0.1)
c.fops.delay_set('ant0y', loadtime=loadtime, delay=(0/1712e6), delay_delta=0.0, phase=0, phase_delta=0)
c.fops.delay_set('ant1x', loadtime=loadtime, delay=(0/1712e6), delay_delta=0.0, phase=0, phase_delta=0)
c.fops.delay_set('ant1y', loadtime=loadtime, delay=(0/1712e6), delay_delta=0.0, phase=0, phase_delta=0)
c.fops.delay_set('ant2x', loadtime=loadtime, delay=(0/1712e6), delay_delta=0.0, phase=0, phase_delta=0)
c.fops.delay_set('ant2y', loadtime=loadtime, delay=(0/1712e6), delay_delta=0.0, phase=0, phase_delta=0)
c.fops.delay_set('ant3x', loadtime=loadtime, delay=(0/1712e6), delay_delta=0.0, phase=0, phase_delta=0)
c.fops.delay_set('ant3y', loadtime=loadtime, delay=(0/1712e6), delay_delta=0.0, phase=0, phase_delta=0)

f0.registers.tl_cd0_control0.write(load_immediate='pulse')
f1.registers.tl_cd0_control0.write(load_immediate='pulse')
f2.registers.tl_cd0_control0.write(load_immediate='pulse')
f3.registers.tl_cd0_control0.write(load_immediate='pulse')

# c.fops.delay_set('ant0x', loadtime=loadtime, delay=0.0, delay_delta=0.0, phase=0, phase_delta=0)
# c.fops.delay_set('ant0y', loadtime=loadtime, delay=0.0, delay_delta=0.0, phase=0, phase_delta=0)
# c.fops.delay_set('ant1x', loadtime=loadtime, delay=0.0, delay_delta=0.0, phase=0, phase_delta=0)
# c.fops.delay_set('ant1y', loadtime=loadtime, delay=0.0, delay_delta=0.0, phase=0, phase_delta=0)
# c.fops.delay_set('ant2x', loadtime=loadtime, delay=0.0, delay_delta=0.0, phase=0, phase_delta=0)
# c.fops.delay_set('ant2y', loadtime=loadtime, delay=0.0, delay_delta=0.0, phase=0, phase_delta=0)
# c.fops.delay_set('ant3x', loadtime=loadtime, delay=0.0, delay_delta=0.0, phase=0, phase_delta=0)
# c.fops.delay_set('ant3y', loadtime=loadtime, delay=0.0, delay_delta=0.0, phase=0, phase_delta=0)

#c.fops.auto_rst_disable()
#c.fops.sys_reset()
#c.fops.sys_reset()
#time.sleep(0.2)
#c.data_streams[-3].tx_enable()
#c.xops.vacc_sync()


print "Checking New Set Values"
print "-----------------------"

print "fhost: %s" % f0
print f0.registers.delay_whole0.read()
print f0.registers.delay_frac0.read()
print f0.registers.delta_delay_whole0.read()
print f0.registers.delta_delay_frac0.read()
print f0.registers.phase0.read()

print "fhost: %s" % f1
print f1.registers.delay_whole0.read()
print f1.registers.delay_frac0.read()
print f1.registers.delta_delay_whole0.read()
print f1.registers.delta_delay_frac0.read()
print f1.registers.phase0.read()

print "fhost: %s" % f2
print f2.registers.delay_whole0.read()
print f2.registers.delay_frac0.read()
print f2.registers.delta_delay_whole0.read()
print f2.registers.delta_delay_frac0.read()
print f2.registers.phase0.read()

print "fhost: %s" % f3
print f3.registers.delay_whole0.read()
print f3.registers.delay_frac0.read()
print f3.registers.delta_delay_whole0.read()
print f3.registers.delta_delay_frac0.read()
print f3.registers.phase0.read()