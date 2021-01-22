import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed


host = 'skarab020307-01'

filename = '/home/avanderbyl/fpgs/s_c107m32k_ctdbg_2021-01-21_1300.fpg'

start_correlator = True
halt_test_on_fail = False

num_xengs = 4
number_of_runs = 100

#==============================================================================
#   Classes and methods
#==============================================================================

class skarab_debug: 
        
    def program_fpga(self, f):
        print 'Programming FPGA' 
        f.upload_to_ram_and_program(filename)
        f.get_system_information(filename)        
        
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
    xeng_indexs = []
    Fchan_to_xeng = []

    # Grab all indexs associated to each distinct XEng
    for x in range(num_xengs):
        xeng_indexs.append(list_duplicates(x_idx,x))

    for x in range(len(xeng_indexs)):
        print 'Grabbing all channels associated to Xeng', x 
        ch_list_temp = []
        for idx in xeng_indexs[x]:
            ch_list_temp.append(ct2_freq_id[idx])
        Fchan_to_xeng.append(ch_list_temp)  
    
    return Fchan_to_xeng

def write_xeng_channels_to_file(channel_per_X):
    for x in range(num_xengs):
        print 'Writing to file for XEng:%d' % x
        f= open("X"+str(x)+".txt","w+")
        for i in range(len(channel_per_X[x])):
            f.write("%d\r\n" % channel_per_X[x][i])
        f.close()

def write_test_results_to_file(results):
    print 'Writing to file'

    #embed()
    
    f= open("Test_results.txt","w+")
    for i in range(len(results)):
        #print results[i]
        f.write("%s\r\n" % str(results[i]))
    f.close()

def read_in_xeng_ref_file(num_xengs):

    xeng_ref_data = []

    for xeng in range(num_xengs):
        with open ("X"+str(xeng)+"_4A_ref.txt", "r") as myfile:
            temp_lst = []
            data = myfile.readlines()
            for line in data:
                tmp = line.rstrip()
                temp_lst.append(int(tmp))

            xeng_ref_data.append(temp_lst)
            #print "xeng_ref_data len is:%d" % len(xeng_ref_data)
            #print "temp_lst len is:%d" % len(temp_lst)

    return xeng_ref_data

def compare_xeng_data_with_ref_xeng(xeng_ref_data, fchannel_per_X):
    print 'Comparing XEng data'

    # check list lengths are the same
    if len(xeng_ref_data) != len(fchannel_per_X):
        raise Exception('Number of XEngs do not match. Aborting.')
    else:
        errors =  []
        for xeng in range(len(xeng_ref_data)):
            # Check list length matches in each XEng
            if len(xeng_ref_data[xeng]) != len(fchannel_per_X[xeng]):
                raise Exception('Number of channels in XEngs do not match. Aborting.')

            match = True
            err_tmp = []
            for i in range(len(xeng_ref_data[xeng])):
                if xeng_ref_data[xeng][i] != fchannel_per_X[xeng][i]:
                    match = False
                    mismatch_str = 'Mismatch in Xeng:', xeng, 'Found Channel:', fchannel_per_X[xeng][i], 'Should be Channel:', xeng_ref_data[xeng][i]
                    print mismatch_str
                    err_tmp.append(mismatch_str)
            

            if match:
                print 'No errors in Xeng:%d' % xeng 
            else:
                errors.append(err_tmp)
                print 'Found', len(errors),'error(s) in XEng', xeng  
    return errors


#==============================================================================
# Start Correlator
#==============================================================================

full_test_results = []

#while True:
for run_number in range(number_of_runs):
    print 'Run Number:', run_number
    print 'Number of errors:', len(full_test_results)

    if start_correlator:
        c=corr2.fxcorrelator.FxCorrelator('bob',config_source='/etc/corr/avdbyl_nb_107_32k.ini')
        c.initialise(program=True,configure=True,require_epoch=False)

        f0 = c.fhosts[0]
    else:    
        f0 = casperfpga.CasperFpga(host)
        f0.get_system_information(filename)

    # Read in reference XEng channel allocations
    xeng_ref_data = read_in_xeng_ref_file(num_xengs)


    #==============================================================================
    #  Register Setup
    #==============================================================================
    # FFT
    f0.registers.nb_pfb_fft_trig_sel.write(sel=1)
    f0.registers.nb_pfb_fft_trig_thresh.write(threshold=4096*4)
    print(f0.registers.nb_pfb_fft_trig_thresh.read())

    # CT
    f0.registers.hmc_ct_ct_trig_sel.write(sel=0)
    f0.registers.hmc_ct_xidx_trig_thresh.write(threshold=0)
    f0.registers.hmc_ct_freq_trig_thresh.write(threshold=0)

    f0.registers.hmc_ct_ct2_dv_sel.write(sel=2)

    # VACC
    # print 'Setting Acc Length'
    # f0.registers.acc_len1.write(reg=np.power(2,16))
    # f0.registers.acc_scale.write(reg=0.9)


    #==============================================================================
    #  ARM Snapshots
    #==============================================================================
    #f0.snapshots.snap_acc_ss.arm(man_trig=False, man_valid=False)
    f0.snapshots.nb_pfb_snap_fft_ss.arm(man_trig=False, man_valid=False)
    f0.snapshots.hmc_ct_ss_ct1_ss.arm(man_trig=True, man_valid=True)
    f0.snapshots.hmc_ct_ss_ct2_ss.arm(man_trig=False, man_valid=False)

    #==============================================================================
    #  Reset
    #==============================================================================
    #print ' ' 
    #print 'Issuing Reset'      

    #f0.registers.cnt_rst.write(reg='pulse')
    f0.registers.control.write(sys_rst='pulse')

    print ' ' 
    print 'Reset Done'      



    #==============================================================================
    #  FFT Debug
    #==============================================================================
    fft_snap = f0.snapshots.nb_pfb_snap_fft_ss.read(arm=False)['data'] 
    fft_re = fft_snap['fft_re']
    fft_im = fft_snap['fft_im']
    fft_ch = fft_snap['ch']
    fft_of = fft_snap['of']
    fft_dv = fft_snap['dv']
    fft_sync = fft_snap['sync']
    fft_cnt_sync = fft_snap['cnt_sync']

    nb_pfb = np.abs(np.power((fft_re + np.multiply(fft_im, 1j)),2))
    # plt.figure(1)
    # plt.plot(nb_pfb)
    # plt.semilogy(nb_pfb)

    #==============================================================================
    #  CT Debug
    #==============================================================================
    ct1_snap = f0.snapshots.hmc_ct_ss_ct1_ss.read(arm=False)['data']

    ct1_f0_re = ct1_snap['f0_re']
    ct1_f1_re = ct1_snap['f1_re']
    ct1_f2_re = ct1_snap['f2_re']
    ct1_f3_re = ct1_snap['f3_re']
    ct1_f4_re = ct1_snap['f4_re']
    ct1_f5_re = ct1_snap['f5_re']
    ct1_f6_re = ct1_snap['f6_re']
    ct1_f7_re = ct1_snap['f7_re']
    ct1_freq_id = ct1_snap['freq_id']
    ct1_x_idx = ct1_snap['x_idx']
    ct1_x_pkt = ct1_snap['x_pkt']
    ct1_pkt_start = ct1_snap['pkt_start']
    ct1_dv = ct1_snap['dv']
    ct1_sync = ct1_snap['sync']

    ct2_snap = f0.snapshots.hmc_ct_ss_ct2_ss.read(arm=False)['data']

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

    # Write the results to file per X-Eng
    # write_xeng_channels_to_file(fchannel_per_X)

    # Compare current Xeng data with reference Xeng data
    results = compare_xeng_data_with_ref_xeng(xeng_ref_data, fchannel_per_X)
    
    # Check if the test passed.
    if len(results) != 0:
        # Create a tuple with run_number and results
        full_test_results.append((run_number,results))
        
        write_test_results_to_file(full_test_results)

        # Halt at this point
        if halt_test_on_fail:
            embed()

    #==============================================================================
    #  VACC
    #==============================================================================
    # Grab SS Data for all skarabs

    #pfb_snap = f0.snapshots.snap_pfb_ss.read(arm=False)['data'] 
    #pfb_snap1 = f0.snapshots.snap_pfb1_ss.read(arm=False)['data'] 

    #pfb_real0 = pfb_snap['real0']
    #pfb_imag0 = pfb_snap['imag0']
    #pfb_real1 = pfb_snap['real1']
    #pfb_imag1 = pfb_snap['imag1']
    #pfb_real2 = pfb_snap1['real2']
    #pfb_imag2 = pfb_snap1['imag2']
    #pfb_real3 = pfb_snap1['real3']
    #pfb_imag3 = pfb_snap1['imag3']
    #
    #pfb_real = []
    #            
    #for x in range(0, len(pfb_real0)):
    #    pfb_real.extend(
    #        [pfb_real0[x], pfb_real1[x], pfb_real2[x], pfb_real3[x]])
    #
    #pfb_imag = []
    #            
    #for x in range(0, len(pfb_imag0)):
    #    pfb_imag.extend(
    #        [pfb_imag0[x], pfb_imag1[x], pfb_imag2[x], pfb_imag3[x]])
    #
    #pfb_complx = pfb_real + np.multiply(pfb_imag, 1j)

    #==============================================================================
    #print ' ' 
    #print 'Grabbing Vacc'  
    #snap_vacc = f0.snapshots.snap_acc_ss.read(arm=False)['data'] 
    #vacc = snap_vacc['acc']

    #==============================================================================




    # #plt.figure(3)
    # #plt.clf()
    # #plt.plot(vacc)

    plt.show()

print full_test_results