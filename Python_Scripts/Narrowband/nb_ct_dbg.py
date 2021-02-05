import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

# Dbelab06
config_file = '/etc/corr/avdbyl_nb_107_32k.ini'
# config_file = '/etc/corr/avdbyl_nb_107_32k.ini'

# CMC2
#config_file = '/etc/corr/array0-bc128n107M32k_qual'
#host = 'skarab020c10-01' #skarab02090b-01,skarab020a09-01

#filename = '/tmp/s_c107m32k_ctdbg_2021-01-21_1300.fpg'

# Control Parameters
f_debug = True
x_debug = True
start_correlator = False

halt_test_on_fail = False
create_fref = False
create_xref = False

dbg_verbose = False
tvg_enable = True

num_channels = 32768
num_fengs = 4
num_xengs_boards = 1   #4A = 1; 64A = 8
num_cores_per_x = 4 
number_of_runs = 50

#==============================================================================
#   Classes and methods
#==============================================================================

# class skarab_debug: 
        
#     def program_fpga(self, f):
#         print 'Programming FPGA' 
#         f.upload_to_ram_and_program(filename)
#         f.get_system_information(filename)        
        
def list_duplicates(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def extract_Fchannel_per_Xeng(x_idx):
    Fchan_to_xeng = []

    # Grab all indexs associated to each distinct XEng
    for x_board in range(num_xengs_boards):

        for core_number in range(num_cores_per_x):
            xeng_indexs = []
            overall_xcore = x_board * num_cores_per_x + core_number
            xeng_indexs.append(list_duplicates(x_idx,overall_xcore))

            print 'Grabbing all channels associated to Xeng Core', overall_xcore 
            ch_list_temp = []

            for idx in xeng_indexs[0]:
                ch_list_temp.append(ct2_freq_id[idx])
            Fchan_to_xeng.append(ch_list_temp)  

            # for x in range(len(xeng_indexs)):
            #     print 'Grabbing all channels associated to Xeng', x 
            #     ch_list_temp = []
            #     for idx in xeng_indexs[x]:
            #         ch_list_temp.append(ct2_freq_id[idx])
            #     Fchan_to_xeng.append(ch_list_temp)  
    
    return Fchan_to_xeng

def write_fxeng_channels_to_file(data):
    feng = data[0]
    channel_per_X = data[1]

    for core_number in range(len(channel_per_X)):
        # Note: 
        # core_number represents the local core number for which an FEng will send to a particular XEng
        # overall_xcore represents the unique core number for the XEng(Overall)
               
        print 'Writing to file for FEng:', feng,'and XEng Core:', core_number
        f= open("F"+str(feng)+"X"+str(core_number)+"_ref"+".txt","w+")
        for i in range(len(channel_per_X[core_number])):
            f.write("%d\r\n" % channel_per_X[core_number][i])
        f.close()

def write_fx_test_results_to_file(results):
    print 'Writing to file'

    f= open("FX_results.txt","a+")
    for i in range(len(results)):
        #print results[i]
        f.write("%s\r\n" % str(time.ctime()))
        f.write("%s\r\n" % str(results[i]))

    f.write(" \r\n")    
    f.write(" \r\n")
    f.close()

def read_in_fxeng_ref_file(total_xcores, num_fengs):

    fxeng_ref_data = []

    for feng in range(num_fengs):
        for core_number in range(total_xcores):
            with open ("F"+str(feng)+"X"+str(core_number)+"_ref.txt", "r") as myfile:
                temp_lst = []
                data = myfile.readlines()
                for line in data:
                    tmp = line.rstrip()
                    temp_lst.append(int(tmp))
            fxeng_ref_data.append(temp_lst)

    return fxeng_ref_data

def compare_fxeng_data_with_ref_fxeng(feng, fxeng_ref_data, fchannel_per_X):
    print '####################'
    print 'Comparing FXEng data'
    print '####################'
    print ' '
    
    # Compute the sum of all xcores for all fengs
    total_fx_cores = num_fengs*num_cores_per_x*num_xengs_boards

    # check number of fengs match
    if len(fxeng_ref_data) != total_fx_cores:
        raise Exception('Number of fx cores do not match. Aborting.')
    else:
        errors =  []

        # We know the Feng under test. Now check each fxcore of the current with the fxcore of the reference
        for curr_cores in range(len(fchannel_per_X)):

            # Compute which core to look at in the reference.
            ref_core = (num_cores_per_x*num_xengs_boards)*feng + curr_cores
            print 'Current Core is:', curr_cores
            print 'Ref Core is:', ref_core


            if len(fxeng_ref_data[ref_core]) != len(fchannel_per_X[curr_cores]):
                raise Exception('Number of channels in XEngs do not match. Aborting.')
            
            match = True
            err_tmp = []

            for i in range(len(fxeng_ref_data[ref_core])):
                if dbg_verbose:
                    print 'Checking Ref Core:', ref_core, 'where freq is:', fxeng_ref_data[ref_core][i], 'and Current Core is:', curr_cores,'with freq:',fchannel_per_X[curr_cores][i]
                if fxeng_ref_data[ref_core][i] != fchannel_per_X[curr_cores][i]:
                    match = False
                    mismatch_str = 'Mismatch in FXCore:', ref_core, 'Found Channel:', fchannel_per_X[curr_cores][i], 'Should be Channel:', fxeng_ref_data[ref_core][i]
                    print mismatch_str
                    err_tmp.append(mismatch_str)

            if match:
                print 'No errors in FXCore:%d' % ref_core 
            else:
                errors.append(err_tmp)
                print 'Found', len(errors),'error(s) in FXCore', ref_core 
    return errors

def check_xeng_core_data(xeng, core, fengid, freq, data, valid):
    print ' '
    print 'Checking XEng core data Xeng:', xeng, 'and core:', core
    print '---------------------------------------------- '
    print ' '

    # Setup runtime parameters
    xcore = []
    passed = True

    # Compute the legitimate channel range for this xcore
    channels_per_core = num_channels/(num_xengs_boards*num_cores_per_x)
    print 'channels_per_core:', channels_per_core

    core_range_start = core * channels_per_core
    core_range_end = core_range_start + (channels_per_core - 1)
    print 'core_range_start:', core_range_start
    print 'core_range_end:', core_range_end

    # embed()

    for idx in range(len(data)):
        
        # Test 1: Does the channel number injected in the data field match the freq channel reported by the XEng core?
        if (freq[idx] == data[idx]) & valid[idx]:
            xcore.append((fengid[idx],freq[idx],data[idx],valid[idx]))
        else:
            print 'Feng',fengid[idx] ,'Match error in channel:', freq[idx], 'and', data[idx]
            passed = False

        # Test 2: Is the channel in the correct core?
        if (freq[idx] < core_range_start) | (freq[idx] > core_range_end):
            passed = False
            print 'Freq Channel under test out of range. Channel is:', freq[idx]

        # Test 3: Is the (injected) channel in the correct core?
        if (data[idx] < core_range_start) | (data[idx] > core_range_end):
            passed = False
            print 'Channel (inject) under test out of range. Channel is:', data[idx]

    # for f in range(num_fengs):
    #     for idx in range(len(fengid)):
    #         if fengid[idx] == f:
    #             if (freq[idx] == data[idx]) & valid[idx]:
    #                 # print 'fengid[idx] is:', fengid[idx], 'and f is:', f
    #                 xcore.append((fengid[idx],freq[idx],data[idx],valid[idx]))
    #             else:
    #                 print 'Feng',fengid[idx] ,'Match error in channel:', freq[idx], 'and', data[idx]
    #                 passed = False
    
    if passed:
        print 'Xeng:', xeng, 'with core:', core, 'Passed'
    else:
        print 'Xeng:', xeng, 'with core:', core, 'Falied'

    return (xcore, passed )

#==============================================================================
# Start Correlator
#==============================================================================

feng_full_test_results = []
xeng_full_test_results = []
core0_error_count = 0
core1_error_count = 0
core2_error_count = 0
core3_error_count = 0

if create_fref == False:
    # Read in reference XEng channel allocations
    print 'Reading in Reference files'
    total_xcores = num_xengs_boards * num_cores_per_x
    fxeng_ref_data = read_in_fxeng_ref_file(total_xcores,num_fengs)

#while True:
for run_number in range(number_of_runs):
    print ' '
    print 'Run Number:', run_number
    print '-----------'
    print 'core0_error_count:', core0_error_count
    print 'core1_error_count:', core1_error_count
    print 'core2_error_count:', core2_error_count
    print 'core3_error_count:', core3_error_count
    time.sleep(1)

    if start_correlator:
        c=corr2.fxcorrelator.FxCorrelator('bob',config_source=config_file)
        c.initialise(program=True,configure=True,require_epoch=False)

    else:    
        c=corr2.fxcorrelator.FxCorrelator('bob',config_source=config_file)
        c.initialise(program=False,configure=False,require_epoch=False)

    if f_debug:
        print("Setting Up FEngs")
        for feng in range(num_fengs):
            f = c.fhosts[feng]
            print("FEng:",feng)

            #==============================================================================
            #  Register Setup
            #==============================================================================
            # FFT
            f.registers.nb_pfb_fft_trig_sel.write(sel=1)
            f.registers.nb_pfb_fft_trig_thresh.write(threshold=4096*4)
            print(f.registers.nb_pfb_fft_trig_thresh.read())

            # CT
            f.registers.hmc_ct_ct_trig_sel.write(sel=0)
            f.registers.hmc_ct_xidx_trig_thresh.write(threshold=0)
            f.registers.hmc_ct_freq_trig_thresh.write(threshold=0)

            f.registers.hmc_ct_ct2_dv_sel.write(sel=0)

            # VACC
            # print 'Setting Acc Length'
            # f0.registers.acc_len1.write(reg=np.power(2,16))
            # f0.registers.acc_scale.write(reg=0.9)

            # CT TVG
            if tvg_enable:
                f.registers.ct_control0.write(tvg_en2=1)

            #==============================================================================
            #  ARM Snapshots
            #==============================================================================
            #f0.snapshots.snap_acc_ss.arm(man_trig=False, man_valid=False)
            f.snapshots.nb_pfb_snap_fft_ss.arm(man_trig=False, man_valid=False)
            f.snapshots.hmc_ct_ss_ct1_ss.arm(man_trig=False, man_valid=False)
            f.snapshots.hmc_ct_ss_ct2_ss.arm(man_trig=False, man_valid=False)

    if x_debug:
        print("Setting Up XEngs")
        for xeng in range(num_xengs_boards):
            x = c.xhosts[xeng]
            print("XEng:",xeng)

            x.registers.hmc_pkt_reord_dv_sel.write(sel=0)
            x.registers.rx_unpack_dv_sel.write(sel=3)
            x.registers.tvg_control.write(snap_hmc_pkt_reord_we_sel=4)

            x.registers.fengid_match.write(sel=3)

            # Inside Cores
            x.registers.sys0_snap_reord_dv_sel.write(sel=0)
            x.registers.sys1_snap_reord_dv_sel.write(sel=0)
            x.registers.sys2_snap_reord_dv_sel.write(sel=0)
            x.registers.sys3_snap_reord_dv_sel.write(sel=0)


            #==============================================================================
            #  ARM Snapshots
            #==============================================================================
            x.snapshots.snap_rx_unpack0_ss.arm(man_trig=False, man_valid=False)
            x.snapshots.snap_hmc_pkt_reord_ss.arm(man_trig=False, man_valid=False)
            x.snapshots.sys0_snap_reord_ss.arm(man_trig=False, man_valid=False)
            x.snapshots.sys1_snap_reord_ss.arm(man_trig=False, man_valid=False)
            x.snapshots.sys2_snap_reord_ss.arm(man_trig=False, man_valid=False)
            x.snapshots.sys3_snap_reord_ss.arm(man_trig=False, man_valid=False)



    #==============================================================================
    #  Reset
    #==============================================================================
    print 'Issuing Reset'      
    c.fops.sys_reset()
    print ' ' 
    print 'Reset Done'      

    if f_debug:
        print '##################'
        print 'Checking FEng Data'
        print '##################'
        for feng in range(num_fengs):
            f = c.fhosts[feng]

            print ' '
            print 'Checking CT Data in FEng:',feng
            print '---------------------------'
            #==============================================================================
            #  FFT Debug
            #==============================================================================
            #fft_snap = f.snapshots.nb_pfb_snap_fft_ss.read(arm=False)['data'] 
            #fft_re = fft_snap['fft_re']
            #fft_im = fft_snap['fft_im']
            #fft_ch = fft_snap['ch']
            #fft_of = fft_snap['of']
            #fft_dv = fft_snap['dv']
            #fft_sync = fft_snap['sync']
            #fft_cnt_sync = fft_snap['cnt_sync']

            #nb_pfb = np.abs(np.power((fft_re + np.multiply(fft_im, 1j)),2))
            #plt.figure(1)
            #plt.plot(nb_pfb)
            #plt.semilogy(nb_pfb)

            #==============================================================================
            #  CT Debug
            #==============================================================================
            # print('Reading CT1')
            # ct1_snap = f.snapshots.hmc_ct_ss_ct1_ss.read(arm=False)['data']

            # ct1_f0_re = ct1_snap['f0_re']
            # ct1_f1_re = ct1_snap['f1_re']
            # ct1_f2_re = ct1_snap['f2_re']
            # ct1_f3_re = ct1_snap['f3_re']
            # ct1_f4_re = ct1_snap['f4_re']
            # ct1_f5_re = ct1_snap['f5_re']
            # ct1_f6_re = ct1_snap['f6_re']
            # ct1_f7_re = ct1_snap['f7_re']
            # ct1_freq_id = ct1_snap['freq_id']
            # ct1_x_idx = ct1_snap['x_idx']
            # ct1_x_pkt = ct1_snap['x_pkt']
            # ct1_pkt_start = ct1_snap['pkt_start']
            # ct1_dv = ct1_snap['dv']
            # ct1_sync = ct1_snap['sync']

            # print('Reading CT2')
            ct2_snap = f.snapshots.hmc_ct_ss_ct2_ss.read(arm=False)['data']

            # ct2_f0_re = ct2_snap['f0_re']
            # ct2_f1_re = ct2_snap['f1_re']
            ct2_data = ct2_snap['data0']
            ct2_freq_id = ct2_snap['freq_id']
            ct2_x_idx = ct2_snap['x_idx']
            ct2_x_pkt = ct2_snap['x_pkt']
            ct2_pkt_start = ct2_snap['pkt_start']
            ct2_dv = ct2_snap['dv']
            ct2_trig = ct2_snap['trig']

            # Get all the channels sent to each XEngine
            fchannel_per_X = extract_Fchannel_per_Xeng(ct2_x_idx)

            # Check if the data is non-zero
            # for idx in range(len(ct2_data)):
            #     if ct2_data[idx] != ct2_freq_id[idx]:
            #         print 'FEng freq error mismatch in channel:',ct2_data[idx],'should be:', ct2_freq_id[idx]

            if create_fref:
                # Write the results to file per X-Eng
                write_fxeng_channels_to_file((feng,fchannel_per_X))
            else:
                # Compare current Xeng data with reference Xeng data
                results = compare_fxeng_data_with_ref_fxeng(feng, fxeng_ref_data, fchannel_per_X)
            
                # Check if the test passed.
                if len(results) != 0:
                    # Create a tuple with run_number and results
                    feng_full_test_results.append(('FEng:'+str(feng),'Run:'+str(run_number),results))

                    write_fx_test_results_to_file(feng_full_test_results) 
                    
                    # Halt at this point
                    if halt_test_on_fail:
                        embed()
        
           

    if x_debug:
        print ' '
        print '##################'
        print 'Checking XEng Data'
        print '##################'
        xeng_cores = []
        for xeng in range(num_xengs_boards):
            x = c.xhosts[xeng]

            #==============================================================================
            #  XEng SPEAD and HMC flags
            #==============================================================================
            header_err_cnt= x.registers.spead_status0.read()['data']['header_err_cnt']
            magic_err_cnt = x.registers.spead_status0.read()['data']['magic_err_cnt']
            pad_err_cnt = x.registers.spead_status0.read()['data']['pad_err_cnt']
            pkt_len_err_cnt = x.registers.spead_status0.read()['data']['pkt_len_err_cnt']
            time_err_cnt = x.registers.spead_status0.read()['data']['time_err_cnt']
            
            if ((header_err_cnt>0) | (magic_err_cnt>0) | (pad_err_cnt>0) | (pkt_len_err_cnt>0) | (time_err_cnt>0)):
                print 'SPEAD Flag Error(s)'
                print 'header_err_cnt:', header_err_cnt
                print 'magic_err_cnt:', magic_err_cnt
                print 'pad_err_cnt:', pad_err_cnt
                print 'pkt_len_err_cnt:', pkt_len_err_cnt
                print 'time_err_cnt:', time_err_cnt
                print ' '
            
            hmc_err_cnt= x.registers.hmc_pkt_reord_status0.read()['data']['hmc_err_cnt']
            dest_err_cnt= x.registers.hmc_pkt_reord_status0.read()['data']['dest_err_cnt']
            
            lnk2_nrdy_err_cnt = x.registers.hmc_pkt_reord_status1.read()['data']['lnk2_nrdy_err_cnt']
            lnk3_nrdy_err_cnt = x.registers.hmc_pkt_reord_status1.read()['data']['lnk3_nrdy_err_cnt']

            miss_err_cnt = x.registers.hmc_pkt_reord_status2.read()['data']['miss_err_cnt']
            ts_err_cnt = x.registers.hmc_pkt_reord_status2.read()['data']['ts_err_cnt']

            discard_cnt = x.registers.hmc_pkt_reord_status3.read()['data']['discard_cnt']
            mcnt_timeout_cnt = x.registers.hmc_pkt_reord_status3.read()['data']['mcnt_timeout_cnt']

            if ((hmc_err_cnt>0) | (dest_err_cnt>0) | (lnk2_nrdy_err_cnt>0) | (lnk3_nrdy_err_cnt>0) | (miss_err_cnt>0) | (ts_err_cnt>0) | (discard_cnt>0) | (mcnt_timeout_cnt>0)):
                print 'HMC Flag Error(s)'
                print 'hmc_err_cnt:', hmc_err_cnt
                print 'dest_err_cnt:', dest_err_cnt
                print 'lnk2_nrdy_err_cnt:', lnk2_nrdy_err_cnt
                print 'lnk3_nrdy_err_cnt:', lnk3_nrdy_err_cnt
                print 'miss_err_cnt:', miss_err_cnt
                print 'ts_err_cnt:', ts_err_cnt
                print 'discard_cnt:', discard_cnt
                print 'mcnt_timeout_cnt:', mcnt_timeout_cnt
                print ' '

            #==============================================================================
            #  XEng Core Data
            #==============================================================================
            print("Checking CT Data in XEng:",xeng)

            #==============================================================================
            #  XEng Unpack
            #==============================================================================
            # print('Reading RX Unpack')
            # rx_unpack_snap = x.snapshots.snap_rx_unpack0_ss.read(arm=False)['data']

            # rx_unp_valid = rx_unpack_snap['valid']
            # rx_unp_eof = rx_unpack_snap['eof']
            # rx_unp_fengid = rx_unpack_snap['fengid']
            # rx_unp_freq_this_eng = rx_unpack_snap['freq_this_eng']
            # rx_unp_xeng_id = rx_unpack_snap['xeng_id']


            #==============================================================================
            #  XEng HMC Reorder
            #==============================================================================
            # hmc_pkt_reord_snap = x.snapshots.snap_hmc_pkt_reord_ss.read(arm=False)['data']

            # hmc_reord_data = hmc_pkt_reord_snap['data']
            # hmc_reord_valid = hmc_pkt_reord_snap['valid']
            # hmc_reord_pkt_idx = hmc_pkt_reord_snap['pkt_idx']
            # hmc_reord_timestamp = hmc_pkt_reord_snap['timestamp']
            # hmc_reord_fengid = hmc_pkt_reord_snap['fengid']
            # hmc_reord_freq = hmc_pkt_reord_snap['freq']
            # hmc_reord_xeng = hmc_pkt_reord_snap['xeng']
            # hmc_reord_err = hmc_pkt_reord_snap['err']
            # hmc_reord_dv = hmc_pkt_reord_snap['dv']

            #==============================================================================
            #  XEng Cores
            #==============================================================================
            # temp_sys0 = x.snapshots.sys0_snap_reord_ss.read()
            # sys0_reord_snap = temp_sys0['data']

            sys0_reord_snap = x.snapshots.sys0_snap_reord_ss.read()['data']

            sys0_reord_fengid = sys0_reord_snap['fengid']
            sys0_reord_valid = sys0_reord_snap['valid']
            sys0_reord_freq = sys0_reord_snap['freq']
            sys0_reord_data = sys0_reord_snap['data']
            sys0_reord_dv = sys0_reord_snap['dv']

            # Create tuple with all sys0 snapshot data
            # sys0_reord = (xeng, core, sys0_reord_fengid, sys0_reord_freq, sys0_reord_data, sys0_reord_valid, sys0_reord_dv)
            # -------------------

            sys1_reord_snap = x.snapshots.sys1_snap_reord_ss.read()['data']

            sys1_reord_fengid = sys1_reord_snap['fengid']
            sys1_reord_valid = sys1_reord_snap['valid']
            sys1_reord_freq = sys1_reord_snap['freq']
            sys1_reord_data = sys1_reord_snap['data']
            sys1_reord_dv = sys1_reord_snap['dv']
            # -------------------

            sys2_reord_snap = x.snapshots.sys2_snap_reord_ss.read()['data']

            sys2_reord_fengid = sys2_reord_snap['fengid']
            sys2_reord_valid = sys2_reord_snap['valid']
            sys2_reord_freq = sys2_reord_snap['freq']
            sys2_reord_data = sys2_reord_snap['data']
            sys2_reord_dv = sys2_reord_snap['dv']
            # -------------------

            sys3_reord_snap = x.snapshots.sys3_snap_reord_ss.read()['data']

            sys3_reord_fengid = sys3_reord_snap['fengid']
            sys3_reord_valid = sys3_reord_snap['valid']
            sys3_reord_freq = sys3_reord_snap['freq']
            sys3_reord_data = sys3_reord_snap['data']
            sys3_reord_dv = sys3_reord_snap['dv']

            #==============================================================================
            #  Check XEng Core Data
            #==============================================================================
            core = 0
            xcore0 = check_xeng_core_data(xeng, core, sys0_reord_fengid, sys0_reord_freq, sys0_reord_data, sys0_reord_valid)
            core = 1
            xcore1 = check_xeng_core_data(xeng, core, sys1_reord_fengid, sys1_reord_freq, sys1_reord_data, sys1_reord_valid)
            core = 2
            xcore2 = check_xeng_core_data(xeng, core, sys2_reord_fengid, sys2_reord_freq, sys2_reord_data, sys2_reord_valid)
            core = 3
            xcore3 = check_xeng_core_data(xeng, core, sys3_reord_fengid, sys3_reord_freq, sys3_reord_data, sys3_reord_valid)
            
            if xcore0[1] == False:
                xeng_full_test_results.append(('XEng:'+str(xeng),'Run:'+str(run_number),xcore0))
                core0_error_count = core0_error_count + 1

            if xcore1[1] == False:
                xeng_full_test_results.append(('XEng:'+str(xeng),'Run:'+str(run_number),xcore1))
                core1_error_count = core1_error_count + 1

            if xcore2[1] == False:
                xeng_full_test_results.append(('XEng:'+str(xeng),'Run:'+str(run_number),xcore2))
                core2_error_count = core2_error_count + 1

            if xcore3[1] == False:
                xeng_full_test_results.append(('XEng:'+str(xeng),'Run:'+str(run_number),xcore3))
                core3_error_count = core3_error_count + 1

            # if ((xcore0[1] | xcore1[1] | xcore2[1] | xcore3[1]) == False):
            #     xeng_error_count = xeng_error_count + 1
            #     print 'xeng_error_count:', xeng_error_count
            #     embed()

            # embed()
            # if create_xref:
            #     # Write the results to file per X-Eng
            #     write_fxeng_channels_to_file((feng,fchannel_per_X))
            # else:
                # Compare current Xeng data with reference Xeng data
                # results = compare_fxeng_data_with_ref_fxeng(feng, fxeng_ref_data, fchannel_per_X)
            
                # # Check if the test passed.
                # if len(results) != 0:
                #     # Create a tuple with run_number and results
                #     feng_full_test_results.append(('FEng:'+str(feng),'Run:'+str(run_number),results))

                #     write_fx_test_results_to_file(feng_full_test_results) 
                    
                #     # Halt at this point
                #     if halt_test_on_fail:
                #         embed()
            # embed()

    plt.show()

print ' '
print '##################################################'
print ' '
print 'Feng Results:', feng_full_test_results
print ' '
print 'Xeng Results:', xeng_full_test_results
print ' '
print '##################################################'
print ' '
print 'Core Error(s)'
print '-------------'
print 'core0_error_count:', core0_error_count
print 'core1_error_count:', core1_error_count
print 'core2_error_count:', core2_error_count
print 'core3_error_count:', core3_error_count
print ' '
print 'SPEAD Flag Error(s)'
print '-------------------'
print 'header_err_cnt:', header_err_cnt
print 'magic_err_cnt:', magic_err_cnt
print 'pad_err_cnt:', pad_err_cnt
print 'pkt_len_err_cnt:', pkt_len_err_cnt
print 'time_err_cnt:', time_err_cnt
print ' '
print 'HMC Flag Error(s)'
print '-----------------'
print 'hmc_err_cnt:', hmc_err_cnt
print 'dest_err_cnt:', dest_err_cnt
print 'lnk2_nrdy_err_cnt:', lnk2_nrdy_err_cnt
print 'lnk3_nrdy_err_cnt:', lnk3_nrdy_err_cnt
print 'miss_err_cnt:', miss_err_cnt
print 'ts_err_cnt:', ts_err_cnt
print 'discard_cnt:', discard_cnt
print 'mcnt_timeout_cnt:', mcnt_timeout_cnt
print ' '
embed()