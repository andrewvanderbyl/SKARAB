import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

hosts = ['skarab020a03-01','skarab020918-01','skarab02091b-01','skarab020A45-01']

print(hosts)

c=corr2.fxcorrelator.FxCorrelator('bob',config_source='/etc/corr/avdbyl_nb_107_32k.ini')
c.initialise(program=False,configure=False,require_epoch=False)

c.fops.set_fft_shift_all('10s')
c.fops.set_center_freq(100e6)

for f in c.fhosts:
    print(f)
    f.registers.control.write(ddc_bypass=0)
    f.registers.control.write(fd_bypass=0)
    f.registers.control.write(pfb_bypass=0)
    print(f.registers.control.read())
