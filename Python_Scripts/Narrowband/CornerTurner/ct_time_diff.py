import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

c=corr2.fxcorrelator.FxCorrelator('bob',config_source='/etc/corr/avdbyl_nb_107_1k.ini')
c.initialise(program=False,configure=False,require_epoch=False)

f0 = c.fhosts[0]
f1 = c.fhosts[1]
f2 = c.fhosts[2]
f3 = c.fhosts[3]

data = f0.snapshots.snap_ctout_ss.read()

for idx, freq in enumerate(data['data']['freq']):
    if(freq == 0):
        print(data['data']['time'][idx]-data['data']['time'][idx-1])