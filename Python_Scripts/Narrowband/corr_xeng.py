import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

hosts = ['skarab020302-01','skarab020304-01','skarab02030f-01','skarab020306-01']

#for x in hosts:
for x in range(1):
    fx = casperfpga.CasperFpga(hosts[0])
    
    fx.get_system_information('/srv/bofs/xeng/s_b4a4x64f_2018-07-09_1121.fpg')
    
     
    fx.snapshots.snap_gbe0_rx_ss.arm(man_trig=False, man_valid=False)
    
    # Grab Snapshot data
    gbe_rx_data = fx.snapshots.snap_gbe0_rx_ss.read(arm=False)['data']
    
    
    data = gbe_rx_data['data']
    valid = gbe_rx_data['valid']
    eof = gbe_rx_data['eof']
    dest_ip = gbe_rx_data['dest_ip']
    dest_port = gbe_rx_data['dest_port']
    src_ip = gbe_rx_data['src_ip']
    src_port = gbe_rx_data['src_port']
    rx_bad = gbe_rx_data['rx_bad']
    rx_over = gbe_rx_data['rx_over']
    #embed() 
    
    
    plt.figure(1)    
    plt.subplot(311)
    plt.plot(data)
    plt.subplot(312)
    plt.plot(valid)
    plt.subplot(313)
    plt.plot(rx_bad)
    
    plt.figure(2)    
    plt.subplot(311)
    plt.plot(dest_ip)
    
    
            
    plt.show()