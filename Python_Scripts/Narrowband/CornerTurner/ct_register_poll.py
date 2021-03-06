import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed
from os import system

dash = '-' * 250
number_of_polls = 7000

print(' *** Register Poll ***')
print('----------------------')
print(' ')

c=corr2.fxcorrelator.FxCorrelator('bob',config_source='/etc/corr/avdbyl_nb_107_32k.ini')
c.initialise(program=False,configure=False,require_epoch=False)

def printSyncStatus():
    print('Sync Status:')      
    for fhost in range(len(c.fhosts)):
        print(sync_status[fhost])
    print(dash)
    print(' ')

def printSyncCount():
    for fhost in range(len(c.fhosts)):
        print('FHost{}:CD Sync Count {:<5}  FHost{}:DDC In Sync Count {:<5}     FHost{}:DDC Out Sync Count {:<5}     FHost{}:FFT Sync Count {:<5}   FHost{}:PFB Sync Count {:<5}    FHost{}:Quant Sync Count {:<5}  FHost{}:CT Sync Count {:< 5}'.format(\
        fhost,cd_sync_count[fhost],\
        fhost, ddc_in_sync_count[fhost],\
        fhost,ddc_out_sync_count[fhost],\
        fhost,fft_sync_count[fhost],\
        fhost,pfb_sync_count[fhost],\
        fhost,quant_sync_count[fhost],\
        fhost,ct_sync_count[fhost]))

    print(dash)
    print(' ')

def printSyncLatency():
    # Print out Sync Latencies (DV Enabled)
    
    print('DV Counter')
    print('----------')
    for fhost in range(len(c.fhosts)):
        print('FHost{}:TLCD Sync Lat {:<5}  FHost{}:CD Raw Sync Lat {:<5}    FHost{}:CD Sync Lat {:<5}  FHost{}:TLBS Sync Lat {:<5}  FHost{}:BS Sync Lat {:<5}     FHost{}:TG DDS Sync Lat {:<5}   FHost{}:DDS Sync Lat {:<5}   FHost{}:Mix Sync Lat {:<5}     FHost{}:DecFIR Sync Lat {:<5}'.format(\
        fhost,sync_lat_tlcd[fhost],\
        fhost,sync_lat_raw_cd_hmc[fhost],\
        fhost,sync_lat_cd_hmc[fhost],\
        fhost,sync_lat_tlbs[fhost],\
        fhost,sync_lat_bs[fhost],\
        fhost,sync_lat_tgdds[fhost],\
        fhost,sync_lat_dds[fhost],\
        fhost,sync_lat_mix[fhost],\
        fhost,sync_lat_decfir[fhost]))
    
    print(' ')
    print(' ')
    for fhost in range(len(c.fhosts)):
        print('FHost{}:DDC Sync Lat {:<5}   FHost{}:FFT Sync Lat {:<5}      FHost{}:FFT ReOrder Sync Lat {:<5}      FHost{}:PFB Sync Lat {:<5}      FHost{}:TLFD Sync Lat {:<5}         FHost{}:FD_NB Sync Lat {:<5}         FHost{}:FD Demux Sync Lat {:<5}    FHost{}:Quant Sync Lat {:<5}'.format(\
        fhost,sync_lat_ddc[fhost],\
        fhost,sync_lat_fft[fhost],\
        fhost,sync_lat_fft_reorder[fhost],\
        fhost,sync_lat_pfb[fhost],\
        fhost,sync_lat_tlfd[fhost],\
        fhost,sync_lat_fd_nb[fhost],\
        fhost,sync_lat_fd_demux[fhost],\
        fhost,sync_lat_quant[fhost]))
        if sync_lat_tlfd[fhost]!=3:
            print('Aha')
            print('FHost{}:FFT Sync Align {:<5}     FHost{}:Sync Align {:<5}'.format(\
            fhost,fft_sync_align[fhost],\
            fhost,sync_align[fhost]))
            print('FHost{}:TLFD Sync Lat {:<5}'.format(\
            fhost,sync_lat_tlfd[fhost]))


    print(' ')
    print(' ')
    for fhost in range(len(c.fhosts)):
        print('FHost{}:CT Sync Lat {:<5}      FHost{}:CT In Sync Lat {:<5}    FHost{}:HMC AddGen Sync Lat {:<5}    FHost{}:HMC Reord Sync Lat {:<5}     FHost{}:HMC Sync Lat {:<5}    FHost{}:Pack Sync Lat {:<5}'.format(\
        fhost,sync_lat_ct[fhost],\
        fhost,sync_lat_ct_in[fhost],\
        fhost,sync_lat_hmc_addgen[fhost],\
        fhost,sync_lat_hmc_reord[fhost],\
        fhost,sync_lat_hmc[fhost],\
        fhost,sync_lat_pack[fhost]))

    print(' ')    
    print(' ')

    print(dash)
    print(' ')

def printSyncLatencyFreeRunning():
    # Print out Sync Latencies (Free Running)

    print('Free Running Counter')
    print('--------------------')
    for fhost in range(len(c.fhosts)):
        print('FHost{}:TLCD Sync Lat {:<5}  FHost{}:CD Raw Sync Lat {:<5}    FHost{}:CD Sync Lat {:<5}  FHost{}:TLBS Sync Lat {:<5}  FHost{}:BS Sync Lat {:<5}     FHost{}:TG DDS Sync Lat {:<5}   FHost{}:DDS Sync Lat {:<5}   FHost{}:Mix Sync Lat {:<5}     FHost{}:DecFIR Sync Lat {:<5}'.format(\
        fhost,sync_lat_tlcd_free[fhost],\
        fhost,sync_lat_raw_cd_hmc_free[fhost],\
        fhost,sync_lat_cd_hmc_free[fhost],\
        fhost,sync_lat_tlbs_free[fhost],\
        fhost,sync_lat_bs_free[fhost],\
        fhost,sync_lat_tgdds_free[fhost],\
        fhost,sync_lat_dds_free[fhost],\
        fhost,sync_lat_mix_free[fhost],\
        fhost,sync_lat_decfir_free[fhost]))
    
    print(' ')
    print(' ')
    for fhost in range(len(c.fhosts)):
        print('FHost{}:DDC Sync Lat {:<5}   FHost{}:FFT Sync Lat {:<5}      FHost{}:FFT ReOrder Sync Lat {:<5}      FHost{}:PFB Sync Lat {:<5}      FHost{}:TLFD Sync Lat {:<5}         FHost{}:FD_NB Sync Lat {:<5}         FHost{}:FD Demux Sync Lat {:<5}    FHost{}:Quant Sync Lat {:<5}'.format(\
        fhost,sync_lat_ddc_free[fhost],\
        fhost,sync_lat_fft_free[fhost],\
        fhost,sync_lat_fft_reorder_free[fhost],\
        fhost,sync_lat_pfb_free[fhost],\
        fhost,sync_lat_tlfd_free[fhost],\
        fhost,sync_lat_fd_nb_free[fhost],\
        fhost,sync_lat_fd_demux_free[fhost],\
        fhost,sync_lat_quant_free[fhost]))
    print(' ')    
    print(' ')

    for fhost in range(len(c.fhosts)):
        print('FHost{}:CT Sync Lat {:<5}      FHost{}:CT In Sync Lat {:<5}    FHost{}:HMC AddGen Sync Lat {:<5}    FHost{}:HMC Reord Sync Lat {:<5}     FHost{}:HMC Sync Lat {:<5}    FHost{}:Pack Sync Lat {:<5}'.format(\
        fhost,sync_lat_ct_free[fhost],\
        fhost,sync_lat_ct_in_free[fhost],\
        fhost,sync_lat_hmc_addgen_free[fhost],\
        fhost,sync_lat_hmc_reord_free[fhost],\
        fhost,sync_lat_hmc_free[fhost],\
        fhost,sync_lat_pack_free[fhost]))

    print(' ')    
    print(' ')

    for fhost in range(len(c.fhosts)):
        print('FHost{}:FFT Sync Align {:<5}     FHost{}:FFT Sync Align {:<5}'.format(\
        fhost,fft_sync_align[fhost],\
        fhost,sync_align[fhost]))
    
    print(' ')    
    print(' ')

    for fhost in range(len(c.fhosts)):
        print('FHost{}:DDS TS (msw) {:<5}     FHost{}:DDS TS (lsw) {:<5}'.format(\
        fhost,dds_msw[fhost],\
        fhost,dds_lsw[fhost]))

    print(' ')    
    print(' ')

    for fhost in range(len(c.fhosts)):
        print('FHost{}:DDC TS (msw) {:<5}     FHost{}:DDC TS (lsw) {:<5}'.format(\
        fhost,ddc_msw[fhost],\
        fhost,ddc_lsw[fhost]))

    print(' ')    
    print(' ')

    for fhost in range(len(c.fhosts)):
        print('FHost{}:PFB TS (msw) {:<5}     FHost{}:PFB TS (lsw) {:<5}'.format(\
        fhost,pfb_msw[fhost],\
        fhost,pfb_lsw[fhost]))

    print(' ')    
    print(' ')

    for fhost in range(len(c.fhosts)):
        print('FHost{}:TG CD (msw) {:<5}     FHost{}:TG CD (lsw) {:<5}'.format(\
        fhost,tg_cd_msw[fhost],\
        fhost,tg_cd_lsw[fhost]))

    print(' ')    
    print(' ')

    print(dash)
    print(' ')

def printSyncDataLatch():
    # Print out Sync Data Latch

    print('Data Latch')
    print('--------------------')
    for fhost in range(len(c.fhosts)):
        print('FHost{}:TLCD {:<5}   FHost{}:CD Raw {:<5}    FHost{}:CD {:<5}    FHost{}:TLBS {:<5}  FHost{}:BS {:<5}    FHost{}:TG DDS {:<5}        FHost{}:DDS {:<5}       FHost{}:Mix {:<5}     FHost{}:DecFIR {:<5}      FHost{}:DDC {:<5}   FHost{}:FFT {:<5}   FHost{}:FFT ReOrder {:<5}'.format(\
        fhost,sync_latch_tlcd[fhost],\
        fhost,sync_latch_raw_cd_hmc[fhost],\
        fhost,sync_latch_cd_hmc[fhost],\
        fhost,sync_latch_tlbs[fhost],\
        fhost,sync_latch_bs[fhost],\
        fhost,sync_latch_tgdds[fhost],\
        fhost,sync_latch_dds[fhost],\
        fhost,sync_latch_mix[fhost],\
        fhost,sync_latch_decfir[fhost],\
        fhost,sync_latch_ddc[fhost],\
        fhost,sync_latch_fft[fhost],\
        fhost,sync_latch_fft_reorder[fhost]))
    
    print(' ')
    print(' ')

    for fhost in range(len(c.fhosts)):
        print('FHost{}:PFB {:<5}     FHost{}:TLFD {:<5}     FHost{}:FDNB {:<5}       FHost{}:FD Demux {:<5}    FHost{}:Quant {:<5}    FHost{}:CT In{:<5}     FHost{}:HMC AddGen {:<5}  FHost{}:HMC Tag {:<5} FHost{}:HMC Wradd {:<5}  FHost{}:HMC RdAdd {:<5}   FHost{}:HMC ReOrd {:<5}     FHost{}:HMC {:<5}   FHost{}:CT {:<5}       FHost{}:Pack {:<5}'.format(\
        fhost,sync_latch_pfb[fhost],\
        fhost,sync_latch_tlfd[fhost],\
        fhost,sync_latch_fd_nb[fhost],\
        fhost,sync_latch_fd_demux[fhost],\
        fhost,sync_latch_quant[fhost],\
        fhost,sync_latch_ct_in[fhost],\
        fhost,sync_latch_hmc_addgen[fhost],\
        fhost,sync_latch_hmc_tag[fhost],\
        fhost,sync_latch_hmc_wradd[fhost],\
        fhost,sync_latch_hmc_rdadd[fhost],\
        fhost,sync_latch_hmc_reord[fhost],\
        fhost,sync_latch_hmc[fhost],\
        fhost,sync_latch_ct[fhost],\
        fhost,sync_latch_pack[fhost]))

    print(' ')    
    print(' ')

    print(dash)
    print(' ')

def printTimeStamps():
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
    print(' ')
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

    print(' ')
    print('Tag Reorder In:')
    hmc_int_time_diff = []

    for r in range(len(hmc_int_msw)):
        # Current Element
        fhost_time_msw = hmc_int_msw[r]
        fhost_time_lsw = hmc_int_lsw[r]

        for n in range(len(hmc_int_msw)-r-1):
            # Next Element
            fhost_time_msw_next = hmc_int_msw[r+n+1]
            fhost_time_lsw_next = hmc_int_lsw[r+n+1]

            hmc_int_msw_diff_temp = fhost_time_msw - fhost_time_msw_next
            hmc_int_lsw_diff_temp = fhost_time_lsw - fhost_time_lsw_next
            hmc_int_time_diff_temp = np.add(np.abs(hmc_int_msw_diff_temp)<<32, np.abs(hmc_int_lsw_diff_temp))
            hmc_int_time_diff.append(hmc_int_time_diff_temp)
            print("Diff: FHost{0} - FHost{1} is:{2}".format(r, (r+n+1), hmc_int_time_diff_temp))

    print(' ')
    print('Tag Reorder Out:')
    proc_time_diff = []

    for r in range(len(proc_msw)):
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
    print(' ')
    print('DDS Timestamps:')
    dds_time_diff = []

    for r in range(len(dds_msw)):
        # Current Element
        fhost_time_msw = dds_msw[r]
        fhost_time_lsw = dds_lsw[r]

        for n in range(len(ddc_msw)-r-1):
            # Next Element
            fhost_time_msw_next = dds_msw[r+n+1]
            fhost_time_lsw_next = dds_lsw[r+n+1]

            dds_msw_diff_temp = fhost_time_msw - fhost_time_msw_next
            dds_lsw_diff_temp = fhost_time_lsw - fhost_time_lsw_next
            dds_time_diff_temp = np.add(np.abs(dds_msw_diff_temp)<<32, np.abs(dds_lsw_diff_temp))
            dds_time_diff.append(dds_time_diff_temp)
            print("Diff: FHost{0} - FHost{1} is:{2}".format(r, (r+n+1), dds_time_diff_temp))

    print(' ')
    print('DDC Timestamps:')
    ddc_time_diff = []

    for r in range(len(ddc_msw)):
        # Current Element
        fhost_time_msw = ddc_msw[r]
        fhost_time_lsw = ddc_lsw[r]

        for n in range(len(ddc_msw)-r-1):
            # Next Element
            fhost_time_msw_next = ddc_msw[r+n+1]
            fhost_time_lsw_next = ddc_lsw[r+n+1]

            ddc_msw_diff_temp = fhost_time_msw - fhost_time_msw_next
            ddc_lsw_diff_temp = fhost_time_lsw - fhost_time_lsw_next
            ddc_time_diff_temp = np.add(np.abs(ddc_msw_diff_temp)<<32, np.abs(ddc_lsw_diff_temp))
            ddc_time_diff.append(ddc_time_diff_temp)
            print("Diff: FHost{0} - FHost{1} is:{2}".format(r, (r+n+1), ddc_time_diff_temp))

    print('PFB Timestamps:')
    pfb_time_diff = []

    for r in range(len(pfb_msw)):
        # Current Element
        fhost_time_msw = pfb_msw[r]
        fhost_time_lsw = pfb_lsw[r]

        for n in range(len(pfb_msw)-r-1):
            # Next Element
            fhost_time_msw_next = pfb_msw[r+n+1]
            fhost_time_lsw_next = pfb_lsw[r+n+1]

            pfb_msw_diff_temp = fhost_time_msw - fhost_time_msw_next
            pfb_lsw_diff_temp = fhost_time_lsw - fhost_time_lsw_next
            pfb_time_diff_temp = np.add(np.abs(pfb_msw_diff_temp)<<32, np.abs(pfb_lsw_diff_temp))
            pfb_time_diff.append(pfb_time_diff_temp)
            print("Diff: FHost{0} - FHost{1} is:{2}".format(r, (r+n+1), pfb_time_diff_temp))

for fhost in range(len(c.fhosts)):
    # Reset Counters
    c.fhosts[fhost].registers.control.write(cnt_rst='pulse')
    # Disable Auto Reset
    c.fhosts[fhost].registers.control.write(auto_rst_enable=0)
    

for i in range(number_of_polls):
   
    c.fops.sys_reset()
    time.sleep(3)
    
    _ = system('clear')

    hmc_in_msw = []
    hmc_in_lsw = []
    hmc_out_msw = []
    hmc_out_lsw = []
    hmc_int_msw = []
    hmc_int_lsw = []
    proc_msw = []
    proc_lsw = []
    dds_msw = []
    dds_lsw = []
    ddc_msw = []
    ddc_lsw = []
    pfb_msw = []
    pfb_lsw = []
    tg_cd_msw = []
    tg_cd_lsw = []

    sync_status = []

    sync_lat_tlcd = []
    sync_lat_cd_hmc = []
    sync_lat_raw_cd_hmc = []
    sync_lat_tlbs = []
    sync_lat_bs = []
    sync_lat_tgdds = []
    sync_lat_dds = []
    sync_lat_mix = []
    sync_lat_decfir = []
    sync_lat_ddc = []
    sync_lat_fft = []
    sync_lat_fft_reorder = []
    sync_lat_pfb = []
    sync_lat_tlfd = []    
    sync_lat_fd_nb = []    
    sync_lat_fd_demux = []
    sync_lat_quant = []
    sync_lat_ct_in = []
    sync_lat_hmc_addgen = []
    sync_lat_hmc_reord = []
    sync_lat_hmc = []
    sync_lat_ct = []
    sync_lat_pack = []

    sync_lat_tlcd_free = []
    sync_lat_cd_hmc_free = []
    sync_lat_raw_cd_hmc_free = []
    sync_lat_tlbs_free = []
    sync_lat_bs_free = []
    sync_lat_tgdds_free = []
    sync_lat_dds_free = []
    sync_lat_mix_free = []
    sync_lat_decfir_free = []   
    sync_lat_ddc_free = []
    sync_lat_fft_free = []
    sync_lat_fft_reorder_free = []    
    sync_lat_pfb_free = []
    sync_lat_tlfd_free = []    
    sync_lat_fd_nb_free = []    
    sync_lat_fd_demux_free = []
    sync_lat_quant_free = []
    sync_lat_ct_in_free = []
    sync_lat_hmc_addgen_free = []
    sync_lat_hmc_reord_free = []
    sync_lat_hmc_free = []
    sync_lat_ct_free = []
    sync_lat_pack_free = []

    sync_latch_tlcd = []
    sync_latch_cd_hmc = []
    sync_latch_raw_cd_hmc = []
    sync_latch_tlbs = []
    sync_latch_bs = []
    sync_latch_tgdds = []
    sync_latch_dds = []
    sync_latch_mix = []
    sync_latch_decfir = []
    sync_latch_ddc = []
    sync_latch_fft = []
    sync_latch_fft_reorder = []      
    sync_latch_pfb = []
    sync_latch_tlfd = []    
    sync_latch_fd_nb = []    
    sync_latch_fd_demux = []
    sync_latch_quant = []
    sync_latch_ct_in = []
    sync_latch_hmc_tag = []
    sync_latch_hmc_wradd = []
    sync_latch_hmc_rdadd = []
    sync_latch_hmc_addgen = []
    sync_latch_hmc_reord = []
    sync_latch_hmc = []
    sync_latch_ct = []
    sync_latch_pack = []

    cd_sync_count = []
    ddc_in_sync_count = []
    ddc_out_sync_count = []
    fft_sync_count = []
    pfb_sync_count = []
    quant_sync_count = []
    ct_sync_count = []

    fft_sync_align = []
    sync_align = []

    for fhost in range(len(c.fhosts)):
        # Grab Sync Status
        sync_status.append(c.fhosts[fhost].registers.sync_status0.read()['data'])

        # Grab Sync Count
        cd_sync_count.append(c.fhosts[fhost].registers.cd_sync_cnt.read()['data']['reg']) 
        ddc_in_sync_count.append(c.fhosts[fhost].registers.DDC_ddc_in_sync_cnt.read()['data']['reg'])
        ddc_out_sync_count.append(c.fhosts[fhost].registers.DDC_ddc_out_sync_cnt.read()['data']['reg'])
        fft_sync_count.append(c.fhosts[fhost].registers.nb_pfb_fft_sync_cnt.read()['data']['reg'])        
        pfb_sync_count.append(c.fhosts[fhost].registers.pfb_sync_cnt.read()['data']['reg']) 
        quant_sync_count.append(c.fhosts[fhost].registers.quant_sync_cnt.read()['data']['reg']) 
        ct_sync_count.append(c.fhosts[fhost].registers.ct_sync_cnt.read()['data']['sync_out']) 

        # Grab Sync Latency
        sync_lat_tlcd.append(c.fhosts[fhost].registers.sync_lat_tlcd.read()['data']['count'])
        sync_lat_cd_hmc.append(c.fhosts[fhost].registers.sync_lat_cd_hmc.read()['data']['count'])
        sync_lat_raw_cd_hmc.append(c.fhosts[fhost].registers.sync_lat_raw_cd_hmc.read()['data']['count'])
        sync_lat_tlbs.append(c.fhosts[fhost].registers.sync_lat_tlbs.read()['data']['count'])
        sync_lat_bs.append(c.fhosts[fhost].registers.sync_lat_bs.read()['data']['count'])
        sync_lat_tgdds.append(c.fhosts[fhost].registers.sync_lat_tgdds.read()['data']['count'])
        sync_lat_dds.append(c.fhosts[fhost].registers.sync_lat_dds.read()['data']['count'])
        sync_lat_mix.append(c.fhosts[fhost].registers.DDC_sync_lat_mix.read()['data']['count'])
        sync_lat_decfir.append(c.fhosts[fhost].registers.DDC_sync_lat_decfir.read()['data']['count'])   
        sync_lat_ddc.append(c.fhosts[fhost].registers.sync_lat_ddc.read()['data']['count'])
        sync_lat_fft.append(c.fhosts[fhost].registers.nb_pfb_sync_lat_fft.read()['data']['count'])   
        sync_lat_fft_reorder.append(c.fhosts[fhost].registers.nb_pfb_sync_lat_fft_reorder.read()['data']['count'])              
        sync_lat_pfb.append(c.fhosts[fhost].registers.sync_lat_pfb.read()['data']['count'])
        sync_lat_tlfd.append(c.fhosts[fhost].registers.sync_lat_tlfd.read()['data']['count'])
        sync_lat_fd_nb.append(c.fhosts[fhost].registers.sync_lat_fd_nb.read()['data']['count'])
        sync_lat_fd_demux.append(c.fhosts[fhost].registers.sync_lat_fd_demux.read()['data']['count'])
        sync_lat_quant.append(c.fhosts[fhost].registers.sync_lat_quant.read()['data']['count'])
        sync_lat_ct_in.append(c.fhosts[fhost].registers.hmc_ct_sync_lat_ct_in.read()['data']['count'])
        sync_lat_hmc_addgen.append(c.fhosts[fhost].registers.hmc_ct_sync_lat_hmc_addgen.read()['data']['count'])
        sync_lat_hmc_reord.append(c.fhosts[fhost].registers.hmc_ct_sync_lat_hmc_reord.read()['data']['count'])
        sync_lat_hmc.append(c.fhosts[fhost].registers.hmc_ct_sync_lat_hmc.read()['data']['count'])
        sync_lat_ct.append(c.fhosts[fhost].registers.sync_lat_ct.read()['data']['count'])
        sync_lat_pack.append(c.fhosts[fhost].registers.sync_lat_pack.read()['data']['count'])
        
        # Grab Sync Latency Free Running
        sync_lat_tlcd_free.append(c.fhosts[fhost].registers.sync_lat_tlcd_free.read()['data']['count'])
        sync_lat_cd_hmc_free.append(c.fhosts[fhost].registers.sync_lat_cd_hmc_free.read()['data']['count'])
        sync_lat_raw_cd_hmc_free.append(c.fhosts[fhost].registers.sync_lat_raw_cd_hmc_free.read()['data']['count'])
        sync_lat_tlbs_free.append(c.fhosts[fhost].registers.sync_lat_tlbs_free.read()['data']['count'])
        sync_lat_bs_free.append(c.fhosts[fhost].registers.sync_lat_bs_free.read()['data']['count'])
        sync_lat_tgdds_free.append(c.fhosts[fhost].registers.sync_lat_tgdds_free.read()['data']['count'])
        sync_lat_dds_free.append(c.fhosts[fhost].registers.sync_lat_dds_free.read()['data']['count'])
        sync_lat_mix_free.append(c.fhosts[fhost].registers.DDC_sync_lat_mix_free.read()['data']['count'])   
        sync_lat_decfir_free.append(c.fhosts[fhost].registers.DDC_sync_lat_decfir_free.read()['data']['count'])   
        sync_lat_ddc_free.append(c.fhosts[fhost].registers.sync_lat_ddc_free.read()['data']['count'])
        sync_lat_fft_free.append(c.fhosts[fhost].registers.nb_pfb_sync_lat_fft_free.read()['data']['count'])
        sync_lat_fft_reorder_free.append(c.fhosts[fhost].registers.nb_pfb_sync_lat_fft_reorder_free.read()['data']['count'])              
        sync_lat_pfb_free.append(c.fhosts[fhost].registers.sync_lat_pfb_free.read()['data']['count'])
        sync_lat_tlfd_free.append(c.fhosts[fhost].registers.sync_lat_tlfd_free.read()['data']['count'])
        sync_lat_fd_nb_free.append(c.fhosts[fhost].registers.sync_lat_fd_nb_free.read()['data']['count'])
        sync_lat_fd_demux_free.append(c.fhosts[fhost].registers.sync_lat_fd_demux_free.read()['data']['count'])
        sync_lat_quant_free.append(c.fhosts[fhost].registers.sync_lat_quant_free.read()['data']['count'])
        sync_lat_ct_in_free.append(c.fhosts[fhost].registers.hmc_ct_sync_lat_ct_in_free.read()['data']['count'])
        sync_lat_hmc_addgen_free.append(c.fhosts[fhost].registers.hmc_ct_sync_lat_hmc_addgen_free.read()['data']['count'])
        sync_lat_hmc_reord_free.append(c.fhosts[fhost].registers.hmc_ct_sync_lat_hmc_reord_free.read()['data']['count'])
        sync_lat_hmc_free.append(c.fhosts[fhost].registers.hmc_ct_sync_lat_hmc_free.read()['data']['count'])
        sync_lat_ct_free.append(c.fhosts[fhost].registers.sync_lat_ct_free.read()['data']['count'])
        sync_lat_pack_free.append(c.fhosts[fhost].registers.sync_lat_pack_free.read()['data']['count'])


        # Grab Sync Data Latch
        sync_latch_tlcd.append(c.fhosts[fhost].registers.sync_latch_tlcd.read()['data']['count'])
        sync_latch_cd_hmc.append(c.fhosts[fhost].registers.sync_latch_cd_hmc.read()['data']['count'])
        sync_latch_raw_cd_hmc.append(c.fhosts[fhost].registers.sync_latch_raw_cd_hmc.read()['data']['count'])
        sync_latch_tlbs.append(c.fhosts[fhost].registers.sync_latch_tlbs.read()['data']['count'])
        sync_latch_bs.append(c.fhosts[fhost].registers.sync_latch_bs.read()['data']['count'])
        sync_latch_tgdds.append(c.fhosts[fhost].registers.sync_latch_tgdds.read()['data']['count'])
        sync_latch_dds.append(c.fhosts[fhost].registers.sync_latch_dds.read()['data']['count'])
        sync_latch_mix.append(c.fhosts[fhost].registers.DDC_sync_latch_mix.read()['data']['count'])
        sync_latch_decfir.append(c.fhosts[fhost].registers.DDC_sync_latch_decfir.read()['data']['count'])
        sync_latch_ddc.append(c.fhosts[fhost].registers.sync_latch_ddc.read()['data']['count'])
        sync_latch_fft.append(c.fhosts[fhost].registers.nb_pfb_sync_latch_fft.read()['data']['count'])
        sync_latch_fft_reorder.append(c.fhosts[fhost].registers.nb_pfb_sync_latch_fft_reorder.read()['data']['count'])           
        sync_latch_pfb.append(c.fhosts[fhost].registers.sync_latch_pfb.read()['data']['count'])
        sync_latch_tlfd.append(c.fhosts[fhost].registers.sync_latch_tlfd.read()['data']['count'])
        sync_latch_fd_nb.append(c.fhosts[fhost].registers.sync_latch_fd_nb.read()['data']['count'])
        sync_latch_fd_demux.append(c.fhosts[fhost].registers.sync_latch_fd_demux.read()['data']['count'])
        sync_latch_quant.append(c.fhosts[fhost].registers.sync_latch_quant.read()['data']['count'])
        sync_latch_ct_in.append(c.fhosts[fhost].registers.hmc_ct_sync_latch_ct_in.read()['data']['count'])
        sync_latch_hmc_addgen.append(c.fhosts[fhost].registers.hmc_ct_sync_latch_hmc_addgen.read()['data']['count'])
        sync_latch_hmc_reord.append(c.fhosts[fhost].registers.hmc_ct_sync_latch_hmc_reord.read()['data']['count'])

        sync_latch_hmc_tag.append(c.fhosts[fhost].registers.hmc_ct_sync_latch_hmc_tag.read()['data']['count'])   
        sync_latch_hmc_wradd.append(c.fhosts[fhost].registers.hmc_ct_sync_latch_hmc_wradd.read()['data']['count'])
        sync_latch_hmc_rdadd.append(c.fhosts[fhost].registers.hmc_ct_sync_latch_hmc_rdadd.read()['data']['count'])

        sync_latch_hmc.append(c.fhosts[fhost].registers.hmc_ct_sync_latch_hmc.read()['data']['count'])
        sync_latch_ct.append(c.fhosts[fhost].registers.sync_latch_ct.read()['data']['count'])
        sync_latch_pack.append(c.fhosts[fhost].registers.sync_latch_pack.read()['data']['count'])

        fft_sync_align.append(c.fhosts[fhost].registers.nb_pfb_fft_sync_align.read()['data']['reg'])
        sync_align.append(c.fhosts[fhost].registers.nb_pfb_sync_gen_sync_align.read()['data']['reg'])
        
        # Grab Sync Time Gen
        hmc_in_msw.append(c.fhosts[fhost].registers.hmc_ct_sync_time_hmc_in_msw.read()['data']['msw'])
        hmc_in_lsw.append(c.fhosts[fhost].registers.hmc_ct_sync_time_hmc_in_lsw.read()['data']['lsw'])

        hmc_out_msw.append(c.fhosts[fhost].registers.hmc_ct_sync_time_hmc_out_msw.read()['data']['msw'])
        hmc_out_lsw.append(c.fhosts[fhost].registers.hmc_ct_sync_time_hmc_out_lsw.read()['data']['lsw'])

        hmc_int_msw.append(c.fhosts[fhost].registers.hmc_ct_obuf_sync_time_hmc_msw.read()['data']['msw'])
        hmc_int_lsw.append(c.fhosts[fhost].registers.hmc_ct_obuf_sync_time_hmc_lsw.read()['data']['lsw'])

        proc_msw.append(c.fhosts[fhost].registers.hmc_ct_obuf_sync_time_proc_msw.read()['data']['msw'])
        proc_lsw.append(c.fhosts[fhost].registers.hmc_ct_obuf_sync_time_proc_lsw.read()['data']['lsw'])

        dds_msw.append(c.fhosts[fhost].registers.sync_time_gen_dds_msw.read()['data']['msw'])
        dds_lsw.append(c.fhosts[fhost].registers.sync_time_gen_dds_lsw.read()['data']['lsw'])

        ddc_msw.append(c.fhosts[fhost].registers.sync_time_ddc_msw.read()['data']['msw'])
        ddc_lsw.append(c.fhosts[fhost].registers.sync_time_ddc_lsw.read()['data']['lsw'])

        pfb_msw.append(c.fhosts[fhost].registers.sync_time_pfb_msw.read()['data']['msw'])
        pfb_lsw.append(c.fhosts[fhost].registers.sync_time_pfb_lsw.read()['data']['lsw'])

        tg_cd_msw.append(c.fhosts[fhost].registers.sync_time_gen_cd_msw.read()['data']['msw'])
        tg_cd_lsw.append(c.fhosts[fhost].registers.sync_time_gen_cd_lsw.read()['data']['lsw'])

    #-----------------------------------------------------------------------
    printSyncStatus()
    printSyncCount()
    printSyncLatency()
    printSyncLatencyFreeRunning()
    printSyncDataLatch()
    printTimeStamps()


    time.sleep(1)
