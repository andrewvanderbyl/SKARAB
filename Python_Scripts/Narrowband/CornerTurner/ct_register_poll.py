import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed
from os import system

hosts = ['skarab020a03-01','skarab020918-01','skarab02091b-01','skarab020A45-01']

print(hosts)

c=corr2.fxcorrelator.FxCorrelator('bob',config_source='/etc/corr/avdbyl_nb_107_32k.ini')
c.initialise(program=False,configure=False,require_epoch=False)


f0 = c.fhosts[0]
f1 = c.fhosts[1]
f2 = c.fhosts[2]
f3 = c.fhosts[3]

for fhost in range(len(c.fhosts)):
    c.fhosts[fhost].registers.control.write(cnt_rst='pulse')

for i in range(10):
   
    c.fops.sys_reset()
    time.sleep(4)
    
    _ = system('clear')

    hmc_in_msw = []
    hmc_in_lsw = []
    hmc_out_msw = []
    hmc_out_lsw = []
    hmc_int_msw = []
    hmc_int_lsw = []
    proc_msw = []
    proc_lsw = []

    sync_status = []
    sync_time_cd_count = []
    sync_time_ddc_count = []
    sync_time_pfb_count = []
    sync_time_ct_count = []

    cd_sync_count = []
    ddc_in_sync_count = []
    ddc_out_sync_count = []
    fft_sync_count = []
    pfb_sync_count = []
    quant_sync_count = []
    ct_sync_count = []

    for fhost in range(len(c.fhosts)):
        # Grab Sync Count
        cd_sync_count.append(c.fhosts[fhost].registers.cd_sync_cnt.read()['data']['reg']) 
        ddc_in_sync_count.append(c.fhosts[fhost].registers.DDC_ddc_in_sync_cnt.read()['data']['reg'])
        ddc_out_sync_count.append(c.fhosts[fhost].registers.DDC_ddc_out_sync_cnt.read()['data']['reg'])
        fft_sync_count.append(c.fhosts[fhost].registers.nb_pfb_fft_sync_cnt.read()['data']['reg'])        
        pfb_sync_count.append(c.fhosts[fhost].registers.pfb_sync_cnt.read()['data']['reg']) 
        quant_sync_count.append(c.fhosts[fhost].registers.quant_sync_cnt.read()['data']['reg']) 
        ct_sync_count.append(c.fhosts[fhost].registers.ct_sync_cnt.read()['data']['sync_out']) 

        # Grab Sync Latency
        sync_status.append(c.fhosts[fhost].registers.sync_status0.read()['data'])
        sync_time_cd_count.append(c.fhosts[fhost].registers.sync_time_cd_count.read()['data'])
        sync_time_ddc_count.append(c.fhosts[fhost].registers.sync_time_ddc_count.read()['data'])
        sync_time_pfb_count.append(c.fhosts[fhost].registers.sync_time_pfb_count.read()['data'])
        sync_time_ct_count.append(c.fhosts[fhost].registers.sync_time_ct_count.read()['data'])

        # Grab Sync Time Gen
        hmc_in_msw.append(c.fhosts[fhost].registers.hmc_ct_sync_time_hmc_in_msw.read()['data']['msw'])
        hmc_in_lsw.append(c.fhosts[fhost].registers.hmc_ct_sync_time_hmc_in_lsw.read()['data']['lsw'])

        hmc_out_msw.append(c.fhosts[fhost].registers.hmc_ct_sync_time_hmc_out_msw.read()['data']['msw'])
        hmc_out_lsw.append(c.fhosts[fhost].registers.hmc_ct_sync_time_hmc_out_lsw.read()['data']['lsw'])

        hmc_int_msw.append(c.fhosts[fhost].registers.hmc_ct_obuf_sync_time_hmc_msw.read()['data']['msw'])
        hmc_int_lsw.append(c.fhosts[fhost].registers.hmc_ct_obuf_sync_time_hmc_lsw.read()['data']['lsw'])

        proc_msw.append(c.fhosts[fhost].registers.hmc_ct_obuf_sync_time_proc_msw.read()['data']['msw'])
        proc_lsw.append(c.fhosts[fhost].registers.hmc_ct_obuf_sync_time_proc_lsw.read()['data']['lsw'])

    #-----------------------------------------------------------------------
    print(' *** Register Poll ***')
    print('--------------------- ')
    print(' ')

    print('Sync Status:')      
    for fhost in range(len(c.fhosts)):
        print(sync_status[fhost])
    print('-----------------------------------------------------------------------')
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CD Sync Count: FHost{0}:{1}".format(fhost,cd_sync_count[fhost]))

    for fhost in range(len(c.fhosts)):
        print("DDC In Sync Count: FHost{0}:{1}".format(fhost,ddc_in_sync_count[fhost]))
        
    for fhost in range(len(c.fhosts)):
        print("DDC Out Sync Count: FHost{0}:{1}".format(fhost,ddc_out_sync_count[fhost]))

    for fhost in range(len(c.fhosts)):
        print("FFT Out Sync Count: FHost{0}:{1}".format(fhost,fft_sync_count[fhost]))

    for fhost in range(len(c.fhosts)):
        print("PFB Sync Count: FHost{0}:{1}".format(fhost,pfb_sync_count[fhost])) 

    for fhost in range(len(c.fhosts)):
        print("Quant Sync Count: FHost{0}:{1}".format(fhost,quant_sync_count[fhost])) 

    for fhost in range(len(c.fhosts)):
        print("CT Sync Count: FHost{0}:{1}".format(fhost,ct_sync_count[fhost])) 

    print('-----------------------------------------------------------------------')
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CD Sync Latency: FHost{0}:{1}".format(fhost,sync_time_cd_count[fhost])) 
    
    for fhost in range(len(c.fhosts)):
        print("DDC Sync Latency: FHost{0}:{1}".format(fhost,sync_time_ddc_count[fhost])) 
    
    for fhost in range(len(c.fhosts)):
        print("PFB Sync Latency: FHost{0}:{1}".format(fhost,sync_time_pfb_count[fhost])) 

    for fhost in range(len(c.fhosts)):
        print("CT Sync Latency: FHost{0}:{1}".format(fhost,sync_time_ct_count[fhost])) 


    print('-----------------------------------------------------------------------')
    print(' ')

    print('HMC In:')
    hmc_in_time_diff = []

    for r in range(len(hmc_in_msw)):
        # Current Element
        fhost_time_msw = hmc_in_msw[r]
        fhost_time_lsw = hmc_in_lsw[r]

        for n in range(len(hmc_in_msw)-r-1):
            # Next Element
            fhost_time_msw_next = hmc_in_msw[r+n+1]
            fhost_time_lsw_next = hmc_in_lsw[r+n+1]

            hmc_in_msw_diff_temp = fhost_time_msw - fhost_time_msw_next
            hmc_in_lsw_diff_temp = fhost_time_lsw - fhost_time_lsw_next
            hmc_in_time_diff_temp = np.add(np.abs(hmc_in_msw_diff_temp)<<32, np.abs(hmc_in_lsw_diff_temp))
            hmc_in_time_diff.append(hmc_in_time_diff_temp)
            print("Diff: FHost{0} - FHost{1} is:{2}".format(r, (r+n+1), hmc_in_time_diff_temp))

    print('HMC Out:')
    hmc_out_time_diff = []

    for r in range(len(hmc_out_msw)):
        # Current Element
        fhost_time_msw = hmc_out_msw[r]
        fhost_time_lsw = hmc_out_lsw[r]

        for n in range(len(hmc_out_msw)-r-1):
            # Next Element
            fhost_time_msw_next = hmc_out_msw[r+n+1]
            fhost_time_lsw_next = hmc_out_lsw[r+n+1]

            hmc_out_msw_diff_temp = fhost_time_msw - fhost_time_msw_next
            hmc_out_lsw_diff_temp = fhost_time_lsw - fhost_time_lsw_next
            hmc_out_time_diff_temp = np.add(np.abs(hmc_out_msw_diff_temp)<<32, np.abs(hmc_out_lsw_diff_temp))
            hmc_out_time_diff.append(hmc_out_time_diff_temp)
            print("Diff: FHost{0} - FHost{1} is:{2}".format(r, (r+n+1), hmc_out_time_diff_temp))


    print('Tag Reorder In:')
    hmc_int_time_diff = []

    for r in range(len(hmc_out_msw)):
        # Current Element
        fhost_time_msw = hmc_int_msw[r]
        fhost_time_lsw = hmc_int_lsw[r]

        for n in range(len(hmc_out_msw)-r-1):
            # Next Element
            fhost_time_msw_next = hmc_int_msw[r+n+1]
            fhost_time_lsw_next = hmc_int_lsw[r+n+1]

            hmc_int_msw_diff_temp = fhost_time_msw - fhost_time_msw_next
            hmc_int_lsw_diff_temp = fhost_time_lsw - fhost_time_lsw_next
            hmc_int_time_diff_temp = np.add(np.abs(hmc_int_msw_diff_temp)<<32, np.abs(hmc_int_lsw_diff_temp))
            hmc_int_time_diff.append(hmc_int_time_diff_temp)
            print("Diff: FHost{0} - FHost{1} is:{2}".format(r, (r+n+1), hmc_int_time_diff_temp))


    print('Tag Reorder Out:')
    proc_time_diff = []

    for r in range(len(hmc_out_msw)):
        # Current Element
        fhost_time_msw = proc_msw[r]
        fhost_time_lsw = proc_lsw[r]

        for n in range(len(proc_msw)-r-1):
            # Next Element
            fhost_time_msw_next = proc_msw[r+n+1]
            fhost_time_lsw_next = proc_lsw[r+n+1]

            proc_msw_diff_temp = fhost_time_msw - fhost_time_msw_next
            proc_lsw_diff_temp = fhost_time_lsw - fhost_time_lsw_next
            proc_time_diff_temp = np.add(np.abs(proc_msw_diff_temp)<<32, np.abs(proc_lsw_diff_temp))
            proc_time_diff.append(proc_time_diff_temp)
            print("Diff: FHost{0} - FHost{1} is:{2}".format(r, (r+n+1), proc_time_diff_temp))

    time.sleep(1)





# Old Code:



    # f1_hmc_in_msw = f1.registers.hmc_ct_sync_time_hmc_in_msw.read()['data']['msw']
    # f1_hmc_in_lsw = f1.registers.hmc_ct_sync_time_hmc_in_lsw.read()['data']['lsw']

    # f1_hmc_out_msw = f1.registers.hmc_ct_sync_time_hmc_out_msw.read()['data']['msw']
    # f1_hmc_out_lsw = f1.registers.hmc_ct_sync_time_hmc_out_lsw.read()['data']['lsw']

    # f1_hmc_int_msw = f1.registers.hmc_ct_obuf_sync_time_hmc_msw.read()['data']['msw']
    # f1_hmc_int_lsw = f1.registers.hmc_ct_obuf_sync_time_hmc_lsw.read()['data']['lsw']

    # f1_proc_msw = f1.registers.hmc_ct_obuf_sync_time_proc_msw.read()['data']['msw']
    # f1_proc_lsw = f1.registers.hmc_ct_obuf_sync_time_proc_lsw.read()['data']['lsw']

    # #-----------------------------------------------------------------------

    # f2_hmc_in_msw = f2.registers.hmc_ct_sync_time_hmc_in_msw.read()['data']['msw']
    # f2_hmc_in_lsw = f2.registers.hmc_ct_sync_time_hmc_in_lsw.read()['data']['lsw']

    # f2_hmc_out_msw = f2.registers.hmc_ct_sync_time_hmc_out_msw.read()['data']['msw']
    # f2_hmc_out_lsw = f2.registers.hmc_ct_sync_time_hmc_out_lsw.read()['data']['lsw']

    # f2_hmc_int_msw = f2.registers.hmc_ct_obuf_sync_time_hmc_msw.read()['data']['msw']
    # f2_hmc_int_lsw = f2.registers.hmc_ct_obuf_sync_time_hmc_lsw.read()['data']['lsw']

    # f2_proc_msw = f2.registers.hmc_ct_obuf_sync_time_proc_msw.read()['data']['msw']
    # f2_proc_lsw = f2.registers.hmc_ct_obuf_sync_time_proc_lsw.read()['data']['lsw']

    # #-----------------------------------------------------------------------

    # f3_hmc_in_msw = f3.registers.hmc_ct_sync_time_hmc_in_msw.read()['data']['msw']
    # f3_hmc_in_lsw = f3.registers.hmc_ct_sync_time_hmc_in_lsw.read()['data']['lsw']

    # f3_hmc_out_msw = f3.registers.hmc_ct_sync_time_hmc_out_msw.read()['data']['msw']
    # f3_hmc_out_lsw = f3.registers.hmc_ct_sync_time_hmc_out_lsw.read()['data']['lsw']

    # f3_hmc_int_msw = f3.registers.hmc_ct_obuf_sync_time_hmc_msw.read()['data']['msw']
    # f3_hmc_int_lsw = f3.registers.hmc_ct_obuf_sync_time_hmc_lsw.read()['data']['lsw']

    # f3_proc_msw = f3.registers.hmc_ct_obuf_sync_time_proc_msw.read()['data']['msw']
    # f3_proc_lsw = f3.registers.hmc_ct_obuf_sync_time_proc_lsw.read()['data']['lsw']


   # for i in range(len(hmc_in_msw)):
    #     print('hmc_in_msw:', hmc_in_msw[i])
    #     print('hmc_in_lsw:',hmc_in_lsw[i])
    #     print(' ')

    # print('HMC Out:')
    # for i in range(len(hmc_out_msw)):
    #     print(hmc_out_msw[i])
    #     print(hmc_out_lsw[i])
    #     print(' ')

    # print('Tag Reorder In:')
    # for i in range(len(hmc_int_msw)):
    #     print(hmc_int_msw[i])
    #     print(hmc_int_lsw[i])
    #     print(' ')

    # print('Tag Reorder Out:')
    # for i in range(len(proc_msw)):
    #     print(proc_msw[i])
    #     print(proc_lsw[i])
    #     print(' ')

    #print('CT HMC In:')
    # # print(f0_hmc_in_msw)
    # # print(f1_hmc_in_msw)
    # # print(f2_hmc_in_msw)
    # # print(f3_hmc_in_msw)
    # # print(f0_hmc_in_lsw)
    # # print(f1_hmc_in_lsw)
    # # print(f2_hmc_in_lsw)
    # # print(f3_hmc_in_lsw)
    # print(' ')
    # print(' ')

    # print('HMC Out:')
    # print(f0_hmc_out_msw)
    # print(f3_hmc_out_msw)
    # print(f1_hmc_out_msw)
    # print(f2_hmc_out_msw)
    # print(f0_hmc_out_lsw)
    # print(f1_hmc_out_lsw)
    # print(f2_hmc_out_lsw)
    # print(f3_hmc_out_lsw)
    # print(' ')
    # print(' ')

    # print('HMC Int:')
    # print(f0_hmc_int_msw)
    # print(f1_hmc_int_msw)
    # print(f2_hmc_int_msw)
    # print(f3_hmc_int_msw)
    # print(f0_hmc_int_lsw)
    # print(f1_hmc_int_lsw)
    # print(f2_hmc_int_lsw)
    # print(f3_hmc_int_lsw)
    # print(' ')
    # print(' ')

    # print('Proc:')
    # print(f0_proc_msw)
    # print(f1_proc_msw)
    # print(f2_proc_msw)
    # print(f3_proc_msw)
    # print(f0_proc_lsw)
    # print(f1_proc_lsw)
    # print(f2_proc_lsw)
    # print(f3_proc_lsw)
    # print(' ')
    # print(' ')

    # Compute Diff: HMC in
    # print('CT HMC In Diff:')
    # print('---------------')
    # hmc_in_diff01_msw = f0_hmc_in_msw - f1_hmc_in_msw
    # hmc_in_diff01_lsw = f0_hmc_in_lsw - f1_hmc_in_lsw
    # time_hmc_in_diff01 = np.add(np.abs(hmc_in_diff01_msw)<<32, np.abs(hmc_in_diff01_lsw))

    # hmc_in_diff02_msw = f0_hmc_in_msw - f2_hmc_in_msw
    # hmc_in_diff02_lsw = f0_hmc_in_lsw - f2_hmc_in_lsw
    # time_hmc_in_diff02 = np.add(np.abs(hmc_in_diff02_msw)<<32, np.abs(hmc_in_diff02_lsw))

    # hmc_in_diff03_msw = f0_hmc_in_msw - f3_hmc_in_msw
    # hmc_in_diff03_lsw = f0_hmc_in_lsw - f3_hmc_in_lsw
    # time_hmc_in_diff03 = np.add(np.abs(hmc_in_diff03_msw)<<32, np.abs(hmc_in_diff03_lsw))

    # hmc_in_diff12_msw = f1_hmc_in_msw - f2_hmc_in_msw
    # hmc_in_diff12_lsw = f1_hmc_in_lsw - f2_hmc_in_lsw
    # time_hmc_in_diff12 = np.add(np.abs(hmc_in_diff12_msw)<<32, np.abs(hmc_in_diff12_lsw))

    # hmc_in_diff13_msw = f1_hmc_in_msw - f3_hmc_in_msw
    # hmc_in_diff13_lsw = f1_hmc_in_lsw - f3_hmc_in_lsw
    # time_hmc_in_diff13 = np.add(np.abs(hmc_in_diff13_msw)<<32, np.abs(hmc_in_diff13_lsw))

    # print('MSW:')
    # print(hmc_in_diff01_msw)
    # print(hmc_in_diff02_msw)
    # print(hmc_in_diff03_msw)
    # print(hmc_in_diff12_msw)
    # print(hmc_in_diff13_msw)
    # print('LSW:')
    # print(hmc_in_diff01_lsw)
    # print(hmc_in_diff02_lsw)
    # print(hmc_in_diff03_lsw)
    # print(hmc_in_diff12_lsw)
    # print(hmc_in_diff13_lsw)
    # print(' ')

    # print('Diff:F0 - F1')
    # print(time_hmc_in_diff01)
    # print('Diff:F0 - F2')
    # print(time_hmc_in_diff02)
    # print('Diff:F0 - F3')
    # print(time_hmc_in_diff03)
    # print('Diff:F1 - F2')
    # print(time_hmc_in_diff12)
    # print('Diff:F1 - F3')
    # print(time_hmc_in_diff13)
    # print(' ')

    # # Compute Diff: HMC Out
    # print('CT HMC Out Diff:')
    # print('----------------')
    # hmc_out_diff01_msw = f0_hmc_out_msw - f1_hmc_out_msw
    # hmc_out_diff01_lsw = f0_hmc_out_lsw - f1_hmc_out_lsw
    # time_hmc_out_diff01 = np.add(np.abs(hmc_out_diff01_msw)<<32, np.abs(hmc_out_diff01_lsw))

    # hmc_out_diff02_msw = f0_hmc_out_msw - f2_hmc_out_msw
    # hmc_out_diff02_lsw = f0_hmc_out_lsw - f2_hmc_out_lsw
    # time_hmc_out_diff02 = np.add(np.abs(hmc_out_diff02_msw)<<32, np.abs(hmc_out_diff02_lsw))

    # hmc_out_diff03_msw = f0_hmc_out_msw - f3_hmc_out_msw
    # hmc_out_diff03_lsw = f0_hmc_out_lsw - f3_hmc_out_lsw
    # time_hmc_out_diff03 = np.add(np.abs(hmc_out_diff03_msw)<<32, np.abs(hmc_out_diff03_lsw))

    # hmc_out_diff12_msw = f1_hmc_out_msw - f2_hmc_out_msw
    # hmc_out_diff12_lsw = f1_hmc_out_lsw - f2_hmc_out_lsw
    # time_hmc_out_diff12 = np.add(np.abs(hmc_out_diff12_msw)<<32, np.abs(hmc_out_diff12_lsw))

    # hmc_out_diff13_msw = f1_hmc_out_msw - f3_hmc_out_msw
    # hmc_out_diff13_lsw = f1_hmc_out_lsw - f3_hmc_out_lsw
    # time_hmc_out_diff13 = np.add(np.abs(hmc_out_diff13_msw)<<32, np.abs(hmc_out_diff13_lsw))

    # print('MSW:')
    # print(hmc_out_diff01_msw)
    # print(hmc_out_diff02_msw)
    # print(hmc_out_diff03_msw)
    # print(hmc_out_diff12_msw)
    # print(hmc_out_diff13_msw)
    # print('LSW:')
    # print(hmc_out_diff01_lsw)
    # print(hmc_out_diff02_lsw)
    # print(hmc_out_diff03_lsw)
    # print(hmc_out_diff12_lsw)
    # print(hmc_out_diff13_lsw)
    # print(' ')

    # print('Diff:F0 - F1')
    # print(time_hmc_out_diff01)
    # print('Diff:F0 - F2')
    # print(time_hmc_out_diff02)
    # print('Diff:F0 - F3')
    # print(time_hmc_out_diff03)
    # print('Diff:F1 - F2')
    # print(time_hmc_out_diff12)
    # print('Diff:F1 - F3')
    # print(time_hmc_out_diff13)
    # print(' ')


    # # Compute Diff: HMC Int
    # print('Tag Re-order In Diff:')
    # print('---------------------')
    # hmc_int_diff01_msw = f0_hmc_int_msw - f1_hmc_int_msw
    # hmc_int_diff01_lsw = f0_hmc_int_lsw - f1_hmc_int_lsw
    # time_hmc_int_diff01 = np.add(np.abs(hmc_int_diff01_msw)<<32, np.abs(hmc_int_diff01_lsw))

    # hmc_int_diff02_msw = f0_hmc_int_msw - f2_hmc_int_msw
    # hmc_int_diff02_lsw = f0_hmc_int_lsw - f2_hmc_int_lsw
    # time_hmc_int_diff02 = np.add(np.abs(hmc_int_diff02_msw)<<32, np.abs(hmc_int_diff02_lsw))

    # hmc_int_diff03_msw = f0_hmc_int_msw - f3_hmc_int_msw
    # hmc_int_diff03_lsw = f0_hmc_int_lsw - f3_hmc_int_lsw
    # time_hmc_int_diff03 = np.add(np.abs(hmc_int_diff03_msw)<<32, np.abs(hmc_int_diff03_lsw))

    # hmc_int_diff12_msw = f1_hmc_int_msw - f2_hmc_int_msw
    # hmc_int_diff12_lsw = f1_hmc_int_lsw - f2_hmc_int_lsw
    # time_hmc_int_diff12 = np.add(np.abs(hmc_int_diff12_msw)<<32, np.abs(hmc_int_diff12_lsw))

    # hmc_int_diff13_msw = f1_hmc_int_msw - f3_hmc_int_msw
    # hmc_int_diff13_lsw = f1_hmc_int_lsw - f3_hmc_int_lsw
    # time_hmc_int_diff13 = np.add(np.abs(hmc_int_diff13_msw)<<32, np.abs(hmc_int_diff13_lsw))

    # print('MSW:')
    # print(hmc_int_diff01_msw)
    # print(hmc_int_diff02_msw)
    # print(hmc_int_diff03_msw)
    # print(hmc_int_diff12_msw)
    # print(hmc_int_diff13_msw)
    # print('LSW:')
    # print(hmc_int_diff01_lsw)
    # print(hmc_int_diff02_lsw)
    # print(hmc_int_diff03_lsw)
    # print(hmc_int_diff12_lsw)
    # print(hmc_int_diff13_lsw)
    # print(' ')

    # print('Diff:F0 - F1')
    # print(time_hmc_int_diff01)
    # print('Diff:F0 - F2')
    # print(time_hmc_int_diff02)
    # print('Diff:F0 - F3')
    # print(time_hmc_int_diff03)
    # print('Diff:F1 - F2')
    # print(time_hmc_int_diff12)
    # print('Diff:F1 - F3')
    # print(time_hmc_int_diff13)
    # print(' ')

    # # Compute Diff: Proc
    # print('Tag Re-order Out Diff:')
    # print('---------------------')
    # proc_diff01_msw = f0_proc_msw - f1_proc_msw
    # proc_diff01_lsw = f0_proc_lsw - f1_proc_lsw
    # time_proc_diff01 = np.add(np.abs(proc_diff01_msw)<<32, np.abs(proc_diff01_lsw))

    # proc_diff02_msw = f0_proc_msw - f2_proc_msw
    # proc_diff02_lsw = f0_proc_lsw - f2_proc_lsw
    # time_proc_diff02 = np.add(np.abs(proc_diff02_msw)<<32, np.abs(proc_diff02_lsw))

    # proc_diff03_msw = f0_proc_msw - f3_proc_msw
    # proc_diff03_lsw = f0_proc_lsw - f3_proc_lsw
    # time_proc_diff03 = np.add(np.abs(proc_diff03_msw)<<32, np.abs(proc_diff03_lsw))

    # proc_diff12_msw = f1_proc_msw - f2_proc_msw
    # proc_diff12_lsw = f1_proc_lsw - f2_proc_lsw
    # time_proc_diff12 = np.add(np.abs(proc_diff12_msw)<<32, np.abs(proc_diff12_lsw))

    # proc_diff13_msw = f1_proc_msw - f3_proc_msw
    # proc_diff13_lsw = f1_proc_lsw - f3_proc_lsw
    # time_proc_diff13 = np.add(np.abs(proc_diff13_msw)<<32, np.abs(proc_diff13_lsw))

    # print('MSW:')
    # print(proc_diff01_msw)
    # print(proc_diff02_msw)
    # print(proc_diff03_msw)
    # print(proc_diff12_msw)
    # print(proc_diff13_msw)
    # print('LSW:')
    # print(proc_diff01_lsw)
    # print(proc_diff02_lsw)
    # print(proc_diff03_lsw)
    # print(proc_diff12_lsw)
    # print(proc_diff13_lsw)
    # print(' ')

    # print('Diff:F0 - F1')
    # print(time_proc_diff01)
    # print('Diff:F0 - F2')
    # print(time_proc_diff02)
    # print('Diff:F0 - F3')
    # print(time_proc_diff03)
    # print('Diff:F1 - F2')
    # print(time_proc_diff12)
    # print('Diff:F1 - F3')
    # print(time_proc_diff13)
    # print(' ')


    # print(f0.registers.hmc_ct_status0.read())
    # print(f1.registers.hmc_ct_status0.read())
    # print(f2.registers.hmc_ct_status0.read())
    # print(f3.registers.hmc_ct_status0.read())
    # print("--------------------------------")

    # print(f0.registers.hmc_ct_status1.read())
    # print(f1.registers.hmc_ct_status1.read())
    # print(f2.registers.hmc_ct_status1.read())
    # print(f3.registers.hmc_ct_status1.read())
    # print("--------------------------------")

    # print(f0.registers.hmc_ct_status2.read())
    # print(f1.registers.hmc_ct_status2.read())
    # print(f2.registers.hmc_ct_status2.read())
    # print(f3.registers.hmc_ct_status2.read())
    # print("--------------------------------")




# print(f0.registers.hmc_ct_status0.read())
# print(f1.registers.hmc_ct_status0.read())
# print(f2.registers.hmc_ct_status0.read())
# print(f3.registers.hmc_ct_status0.read())
# print("--------------------------------")

# print(f0.registers.hmc_ct_status1.read())
# print(f1.registers.hmc_ct_status1.read())
# print(f2.registers.hmc_ct_status1.read())
# print(f3.registers.hmc_ct_status1.read())
# print("--------------------------------")

# print(f0.registers.hmc_ct_status2.read())
# print(f1.registers.hmc_ct_status2.read())
# print(f2.registers.hmc_ct_status2.read())
# print(f3.registers.hmc_ct_status2.read())
# print("--------------------------------")