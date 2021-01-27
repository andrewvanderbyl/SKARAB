import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

# Dbelab06
config_file = '/etc/corr/avdbyl_nb_107_32k.ini'

# CMC2
#config_file = '/etc/corr/array0-bc128n107M32k_qual'
#host = 'skarab020c10-01' #skarab02090b-01,skarab020a09-01

#filename = '/tmp/s_c107m32k_ctdbg_2021-01-21_1300.fpg'

# Control Parameters
f_debug = True
x_debug = False
start_correlator = False
halt_test_on_fail = False
create_ref = False
dbg_verbose = False

num_fengs = 4
num_xengs_boards = 1   #4A = 1; 64A = 8
num_cores_per_x = 4 
number_of_runs = 1

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

def write_xeng_channels_to_file(data):
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

def read_in_xeng_ref_file(total_xcores, num_fengs):

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

def compare_xeng_data_with_ref_xeng(feng, fxeng_ref_data, fchannel_per_X):
    print 'Comparing FXEng data'
    
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
            ref_core = num_fengs*feng + curr_cores
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


#==============================================================================
# Start Correlator
#==============================================================================

feng_full_test_results = []
xeng_full_test_results = []

if create_ref == False:
    # Read in reference XEng channel allocations
    print 'Reading in Reference files'
    total_xcores = num_xengs_boards * num_cores_per_x
    fxeng_ref_data = read_in_xeng_ref_file(total_xcores,num_fengs)

#while True:
for run_number in range(number_of_runs):
    print 'Run Number:', run_number
    print 'Number of errors:', len(feng_full_test_results)

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

            #==============================================================================
            #  ARM Snapshots
            #==============================================================================
            #f0.snapshots.snap_acc_ss.arm(man_trig=False, man_valid=False)
            f.snapshots.nb_pfb_snap_fft_ss.arm(man_trig=False, man_valid=False)
            f.snapshots.hmc_ct_ss_ct1_ss.arm(man_trig=False, man_valid=False)
            f.snapshots.hmc_ct_ss_ct2_ss.arm(man_trig=False, man_valid=False)

    if x_debug:
        print("Setting Up XEngs")
        for xeng in range(num_xengs):
            x = c.xhosts[xeng]
            print("XEng:",xeng)
            x.snapshots.snap_rx_unpack0_ss.arm(man_trig=False, man_valid=False)





    #==============================================================================
    #  Reset
    #==============================================================================
    print 'Issuing Reset'      
    c.fops.sys_reset()
    print ' ' 
    print 'Reset Done'      

    if f_debug:
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

            ct2_f0_re = ct2_snap['f0_re']
            ct2_f1_re = ct2_snap['f1_re']
            ct2_freq_id = ct2_snap['freq_id']
            ct2_x_idx = ct2_snap['x_idx']
            ct2_x_pkt = ct2_snap['x_pkt']
            ct2_pkt_start = ct2_snap['pkt_start']
            ct2_dv = ct2_snap['dv']
            ct2_trig = ct2_snap['trig']

            # Get all the channels sent to each XEngine
            fchannel_per_X = extract_Fchannel_per_Xeng(ct2_x_idx)

            if create_ref:
                # Write the results to file per X-Eng
                write_xeng_channels_to_file((feng,fchannel_per_X))
            else:
                # Compare current Xeng data with reference Xeng data
                results = compare_xeng_data_with_ref_xeng(feng, fxeng_ref_data, fchannel_per_X)
            
                # Check if the test passed.
                if len(results) != 0:
                    # Create a tuple with run_number and results
                    feng_full_test_results.append(('FEng:'+str(feng),'Run:'+str(run_number),results))

                    write_fx_test_results_to_file(feng_full_test_results) 
                    
                    # Halt at this point
                    if halt_test_on_fail:
                        embed()
        
           

    if x_debug:
        for xeng in range(num_xengs):
            x = c.xhosts[xeng]
            print("Checking CT Data in XEng:",xeng)

            #==============================================================================
            #  XEng Unpack
            #==============================================================================
            # print('Reading RX Unpack')
            rx_unpack_snap = x.snapshots.snap_rx_unpack0_ss.read(arm=False)['data']

            rx_unp_valid = rx_unpack_snap['valid']
            rx_unp_eof = rx_unpack_snap['eof']
            rx_unp_fengid = rx_unpack_snap['fengid']
            rx_unp_freq_this_eng = rx_unpack_snap['freq_this_eng']
            rx_unp_xeng_id = rx_unpack_snap['xeng_id']

            print x.snapshots.snap_rx_unpack0_ss.pri

    plt.show()

print ' '
print '##################################################'
print ' '
print 'Feng Results:', feng_full_test_results
print ' '
print 'Xeng Results:', xeng_full_test_results
print ' '
print '##################################################'