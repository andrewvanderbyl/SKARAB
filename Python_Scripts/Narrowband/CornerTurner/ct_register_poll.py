import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed
from os import system

dash = '-' * 40

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
        print("CD Sync Count: FHost{0}:{1}".format(fhost,cd_sync_count[fhost]))
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("DDC In Sync Count: FHost{0}:{1}".format(fhost,ddc_in_sync_count[fhost]))
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("DDC Out Sync Count: FHost{0}:{1}".format(fhost,ddc_out_sync_count[fhost]))
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("FFT Out Sync Count: FHost{0}:{1}".format(fhost,fft_sync_count[fhost]))
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("PFB Sync Count: FHost{0}:{1}".format(fhost,pfb_sync_count[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("Quant Sync Count: FHost{0}:{1}".format(fhost,quant_sync_count[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CT Sync Count: FHost{0}:{1}".format(fhost,ct_sync_count[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print('FHost{}:CD Sync Count {:<5}FHost{}:DDC In Sync Count {:<5} FHost{}:DDC Out Sync Count {:<5} FHost{}:FFT Sync Count {:<5} FHost{}:PFB Sync Count {:<5} FHost{}:Quant Sync Count {:<5} FHost{}:CT Sync Count {:< 5}'.format(fhost,cd_sync_count[fhost],\
        fhost, ddc_in_sync_count[fhost],\
        fhost,ddc_out_sync_count[fhost],\
        fhost,fft_sync_count[fhost],\
        fhost,pfb_sync_count[fhost],\
        fhost,quant_sync_count[fhost],\
        fhost,ct_sync_count[fhost]))

    print(dash)
    print(' ')

def printSyncLatency():
    # Print out Sync Latencies
    for fhost in range(len(c.fhosts)):
        print("TLCD Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_tlcd[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CD Raw Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_raw_cd_hmc[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CD Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_cd_hmc[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("TLBS Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_tlbs[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("BS Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_bs[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("TG DDS Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_tgdds[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("DDS Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_dds[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("Mix Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_mix[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("DecFIR Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_decfir[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("DDC Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_ddc[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("FFT Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_fft[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("FFT ReOrder Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_fft_reorder[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("PFB Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_pfb[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("FD Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_fd[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("Quant Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_quant[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CT Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_ct[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CT In Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_ct_in[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("HMC AddGen Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_hmc_addgen[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("Pack Sync Latency: FHost{0}:{1}".format(fhost,sync_lat_pack[fhost])) 
    print(' ')

    print('-----------------------------------------------------------------------')
    print(' ')

def printSyncLatencyFreeRunning():

    # Print out Sync Latencies (Free Running)
    for fhost in range(len(c.fhosts)):
        print("TLCD Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_tlcd_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CD Raw Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_raw_cd_hmc_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CD Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_cd_hmc_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("TLBS Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_tlbs_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("BS Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_bs_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("TG DDS Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_tgdds_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("DDS Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_dds_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("Mix Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_mix_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("DecFIR Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_decfir_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("DDC Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_ddc_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("FFT Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_fft_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("FFT ReOrder Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_fft_reorder_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("PFB Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_pfb_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("FD Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_fd_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("Quant Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_quant_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CT Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_ct_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CT In Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_ct_in_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("HMC AddGen Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_hmc_addgen_free[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("Pack Sync Latency(Free): FHost{0}:{1}".format(fhost,sync_lat_pack_free[fhost])) 
    print(' ')

    print(dash)
    print(' ')

def printSyncDataLatch():
    # Print out Sync Data Latch
    for fhost in range(len(c.fhosts)):
        print("TLCD Data Latch: FHost{0}:{1}".format(fhost,sync_latch_tlcd[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CD Raw Data Latch: FHost{0}:{1}".format(fhost,sync_latch_raw_cd_hmc[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CD Data Latch: FHost{0}:{1}".format(fhost,sync_latch_cd_hmc[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("TLBS Data Latch: FHost{0}:{1}".format(fhost,sync_latch_tlbs[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("BS Data Latch: FHost{0}:{1}".format(fhost,sync_latch_bs[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("TG DDS Data Latch: FHost{0}:{1}".format(fhost,sync_latch_tgdds[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("DDS Data Latch: FHost{0}:{1}".format(fhost,sync_latch_dds[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("Mix Data Latch: FHost{0}:{1}".format(fhost,sync_latch_mix[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("DecFIR Data Latch: FHost{0}:{1}".format(fhost,sync_latch_decfir[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("DDC Data Latch: FHost{0}:{1}".format(fhost,sync_latch_ddc[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("FFT Data Latch: FHost{0}:{1}".format(fhost,sync_latch_fft[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("FFT ReOrder Data Latch: FHost{0}:{1}".format(fhost,sync_latch_fft_reorder[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("PFB Data Latch: FHost{0}:{1}".format(fhost,sync_latch_pfb[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("FD Data Latch: FHost{0}:{1}".format(fhost,sync_latch_fd[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("Quant Data Latch: FHost{0}:{1}".format(fhost,sync_latch_quant[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CT Data Latch: FHost{0}:{1}".format(fhost,sync_latch_ct[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CT In Data Latch: FHost{0}:{1}".format(fhost,sync_latch_ct_in[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("CT HMC AddGen Data Latch: FHost{0}:{1}".format(fhost,sync_latch_hmc_addgen[fhost])) 
    print(' ')

    for fhost in range(len(c.fhosts)):
        print("Pack Data Latch: FHost{0}:{1}".format(fhost,sync_latch_pack[fhost])) 
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


for fhost in range(len(c.fhosts)):
    # Reset Counters
    c.fhosts[fhost].registers.control.write(cnt_rst='pulse')
    # Disable Auto Reset
    c.fhosts[fhost].registers.control.write(auto_rst_enable=0)
    

for i in range(2):
   
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
    sync_lat_fd = []
    sync_lat_quant = []
    sync_lat_ct = []
    sync_lat_ct_in = []
    sync_lat_hmc_addgen = []
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
    sync_lat_fd_free = []
    sync_lat_quant_free = []
    sync_lat_ct_free = []
    sync_lat_ct_in_free = []
    sync_lat_hmc_addgen_free = []    
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
    sync_latch_fd = []
    sync_latch_quant = []
    sync_latch_ct = []
    sync_latch_ct_in = []
    sync_latch_hmc_addgen = []      
    sync_latch_pack = []

    cd_sync_count = []
    ddc_in_sync_count = []
    ddc_out_sync_count = []
    fft_sync_count = []
    pfb_sync_count = []
    quant_sync_count = []
    ct_sync_count = []

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
        sync_lat_tlcd.append(c.fhosts[fhost].registers.sync_lat_tlcd.read()['data'])
        sync_lat_cd_hmc.append(c.fhosts[fhost].registers.sync_lat_cd_hmc.read()['data'])
        sync_lat_raw_cd_hmc.append(c.fhosts[fhost].registers.sync_lat_raw_cd_hmc.read()['data'])
        sync_lat_tlbs.append(c.fhosts[fhost].registers.sync_lat_tlbs.read()['data'])
        sync_lat_bs.append(c.fhosts[fhost].registers.sync_lat_bs.read()['data'])
        sync_lat_tgdds.append(c.fhosts[fhost].registers.sync_lat_tgdds.read()['data'])
        sync_lat_dds.append(c.fhosts[fhost].registers.sync_lat_dds.read()['data'])
        sync_lat_mix.append(c.fhosts[fhost].registers.DDC_sync_lat_mix.read()['data'])
        sync_lat_decfir.append(c.fhosts[fhost].registers.DDC_sync_lat_decfir.read()['data'])   
        sync_lat_ddc.append(c.fhosts[fhost].registers.sync_lat_ddc.read()['data'])
        sync_lat_fft.append(c.fhosts[fhost].registers.nb_pfb_sync_lat_fft.read()['data'])   
        sync_lat_fft_reorder.append(c.fhosts[fhost].registers.nb_pfb_sync_lat_fft_reorder.read()['data'])              
        sync_lat_pfb.append(c.fhosts[fhost].registers.sync_lat_pfb.read()['data'])
        sync_lat_fd.append(c.fhosts[fhost].registers.sync_lat_fd.read()['data'])
        sync_lat_quant.append(c.fhosts[fhost].registers.sync_lat_quant.read()['data'])
        sync_lat_ct.append(c.fhosts[fhost].registers.sync_lat_ct.read()['data'])
        sync_lat_ct_in.append(c.fhosts[fhost].registers.hmc_ct_sync_lat_ct_in.read()['data'])
        sync_lat_hmc_addgen.append(c.fhosts[fhost].registers.hmc_ct_sync_lat_hmc_addgen.read()['data'])
        sync_lat_pack.append(c.fhosts[fhost].registers.sync_lat_pack.read()['data'])
        
        # Grab Sync Latency Free Running
        sync_lat_tlcd_free.append(c.fhosts[fhost].registers.sync_lat_tlcd_free.read()['data'])
        sync_lat_cd_hmc_free.append(c.fhosts[fhost].registers.sync_lat_cd_hmc_free.read()['data'])
        sync_lat_raw_cd_hmc_free.append(c.fhosts[fhost].registers.sync_lat_raw_cd_hmc_free.read()['data'])
        sync_lat_tlbs_free.append(c.fhosts[fhost].registers.sync_lat_tlbs_free.read()['data'])
        sync_lat_bs_free.append(c.fhosts[fhost].registers.sync_lat_bs_free.read()['data'])
        sync_lat_tgdds_free.append(c.fhosts[fhost].registers.sync_lat_tgdds_free.read()['data'])
        sync_lat_dds_free.append(c.fhosts[fhost].registers.sync_lat_dds_free.read()['data'])
        sync_lat_mix_free.append(c.fhosts[fhost].registers.DDC_sync_lat_mix_free.read()['data'])   
        sync_lat_decfir_free.append(c.fhosts[fhost].registers.DDC_sync_lat_decfir_free.read()['data'])   
        sync_lat_ddc_free.append(c.fhosts[fhost].registers.sync_lat_ddc_free.read()['data'])
        sync_lat_fft_free.append(c.fhosts[fhost].registers.nb_pfb_sync_lat_fft_free.read()['data'])
        sync_lat_fft_reorder_free.append(c.fhosts[fhost].registers.nb_pfb_sync_lat_fft_reorder_free.read()['data'])              
        sync_lat_pfb_free.append(c.fhosts[fhost].registers.sync_lat_pfb_free.read()['data'])
        sync_lat_fd_free.append(c.fhosts[fhost].registers.sync_lat_fd_free.read()['data'])
        sync_lat_quant_free.append(c.fhosts[fhost].registers.sync_lat_quant_free.read()['data'])
        sync_lat_ct_free.append(c.fhosts[fhost].registers.sync_lat_ct_free.read()['data'])
        sync_lat_ct_in_free.append(c.fhosts[fhost].registers.hmc_ct_sync_lat_ct_in_free.read()['data'])
        sync_lat_hmc_addgen_free.append(c.fhosts[fhost].registers.hmc_ct_sync_lat_hmc_addgen_free.read()['data'])        
        sync_lat_pack_free.append(c.fhosts[fhost].registers.sync_lat_pack_free.read()['data'])


        # Grab Sync Data Latch
        sync_latch_tlcd.append(c.fhosts[fhost].registers.sync_latch_tlcd.read()['data'])
        sync_latch_cd_hmc.append(c.fhosts[fhost].registers.sync_latch_cd_hmc.read()['data'])
        sync_latch_raw_cd_hmc.append(c.fhosts[fhost].registers.sync_latch_raw_cd_hmc.read()['data'])
        sync_latch_tlbs.append(c.fhosts[fhost].registers.sync_latch_tlbs.read()['data'])
        sync_latch_bs.append(c.fhosts[fhost].registers.sync_latch_bs.read()['data'])
        sync_latch_tgdds.append(c.fhosts[fhost].registers.sync_latch_tgdds.read()['data'])
        sync_latch_dds.append(c.fhosts[fhost].registers.sync_latch_dds.read()['data'])
        sync_latch_mix.append(c.fhosts[fhost].registers.DDC_sync_latch_mix.read()['data'])
        sync_latch_decfir.append(c.fhosts[fhost].registers.DDC_sync_latch_decfir.read()['data'])
        sync_latch_ddc.append(c.fhosts[fhost].registers.sync_latch_ddc.read()['data'])
        sync_latch_fft.append(c.fhosts[fhost].registers.nb_pfb_sync_latch_fft.read()['data'])
        sync_latch_fft_reorder.append(c.fhosts[fhost].registers.nb_pfb_sync_latch_fft_reorder.read()['data'])           
        sync_latch_pfb.append(c.fhosts[fhost].registers.sync_latch_pfb.read()['data'])
        sync_latch_fd.append(c.fhosts[fhost].registers.sync_latch_fd.read()['data'])
        sync_latch_quant.append(c.fhosts[fhost].registers.sync_latch_quant.read()['data'])
        sync_latch_ct.append(c.fhosts[fhost].registers.sync_latch_ct.read()['data'])
        sync_latch_ct_in.append(c.fhosts[fhost].registers.hmc_ct_sync_latch_ct_in.read()['data'])
        sync_latch_hmc_addgen.append(c.fhosts[fhost].registers.hmc_ct_sync_latch_hmc_addgen.read()['data'])              
        sync_latch_pack.append(c.fhosts[fhost].registers.sync_latch_pack.read()['data'])


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
    printSyncStatus()
    printSyncCount()
    #printSyncLatency()
    #printSyncLatencyFreeRunning()
    #printSyncDataLatch()


    time.sleep(1)
