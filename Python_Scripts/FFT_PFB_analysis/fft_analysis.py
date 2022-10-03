# Use: Casper FFT  
# No PFB
# python fft_analysis.py --cw 0.85 --cw_freq 26.776123e6 --wgn 0.105 --acc 1024 --eq 15 --fft_shift 65535 --plot --program
# python fft_analysis.py --cw 0.85 --cw_freq 26.776123e6 --wgn 0.08 --acc 1024 --eq 80 --fft_shift 65535 --plot

# Use: Xilinx FFT
# python fft_analysis.py --cw 0.99 --cw_freq 267.76123e6 --wgn 0.07 --acc 1024 --eq 100 --mix_freq 267.76123e6 --fft_shift 21845 --program
# python fft_analysis.py --cw 0.99 --cw_freq 267.76123e6 --wgn 0.07 --acc 1024 --eq 100 --mix_freq 267.76123e6 --fft_shift 21845 

# Shift Analysis
# python fft_analysis.py --cw 0.5 --cw_freq 267.76123e6 --wgn 0.0 --acc 1 --eq 10 --mix_freq 267.76123e6 --plot --xil_shift_analysis --program

import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import argparse
from IPython import embed
import fft_plotting
import set_registers
import snapshots
import matplotlib.pyplot as plt

host = 'skarab02080A-01'

# WB: CASPER FFT
# prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_fft_wb_2022-08-25_0922.fpg"
# prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_fft_only_wb_2022-08-10_0052.fpg"
# prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_pfb_wb_2022-08-25_1300.fpg"

# NB: Xilinx FFT
# prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_fft_nb_2022-08-19_1634.fpg"
prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_fft_nb_2022-09-30_1400.fpg"
# prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_pfb_nb_2022-08-22_1052.fpg"

#==============================================================================
#   Classes and methods
#==============================================================================
     
def program_fpga(f, args, prog_file):
	if args.program:
		print 'Programming FPGA:', prog_file
		f.upload_to_ram_and_program(prog_file)
		f.get_system_information(prog_file)
	else:
		print 'Getting system information using', prog_file
		f.get_system_information(prog_file)

def system_reset(f):
	print 'Issue sync'
	f.registers.control.write(sys_rst='pulse')

def manual_sync(f):
	print 'Issue sync'
	f.registers.man_sync.write(sync='pulse')

def data_analysis(data):
	print 'Max value: ',np.max(data)
	print 'Max value position: ',np.argmax(data)
	fft_plotting.plot_vacc_data(data)

def db_power(x):
    # np.maximum just to prevent errors about log(0)
	return 10 * np.log10(np.maximum(1e-3, x))

def change_setup(f, args, cw_scale, shift):
	set_registers.set_cw_generator(f, scale=cw_scale, freq=args.cw_freq)
	set_registers.set_mixer_freq(f, mix_freq=args.mix_freq)
	set_registers.set_fft_shift(f, shift=shift)

	# Arm snapshots
	snapshots.arm_adc_snapshots(f)
	snapshots.arm_ddc_snapshots(f)
	snapshots.arm_fft_nb_snapshots(f)

def setup_with_args(f,args):
	# # Is this the FFT or PFB version?
	if prog_file.find('pfb') >= 0:
		print 'PFB in design'
		pfb = True
	else:
		print 'Only FFT in design'
		pfb = False

	# Is this the CASPER FFT or Xilinx FFT version?
	if prog_file.find('wb') >= 0:
		print 'Wideband design under test'
		wideband = True

	else: # NB (Xilinx FFT)
		print 'Narrowband design under test'
		wideband = False
		set_registers.set_mixer_freq(f, mix_freq=args.mix_freq)

	# Set parameters
	if wideband:
		set_registers.set_mixer_freq(f, mix_freq=args.mix_freq)
	
	set_registers.set_fft_shift(f, shift=args.fft_shift)
	set_registers.set_eq(f, eq=args.eq)
	set_registers.set_wng_generator(f, scale=args.wgn)
	set_registers.set_cw_generator(f, scale=args.cw, freq=args.cw_freq)
	set_registers.set_vacc(f, acc_len=args.acc)
	f.registers.control.write(cnt_rst='pulse')

	# Arm snapshots
	snapshots.arm_adc_snapshots(f)
	snapshots.arm_ddc_snapshots(f)

	if pfb:
		if wideband:
			snapshots.arm_pfb_wb_snapshots(f)
		else:			
			snapshots.arm_pfb_nb_snapshots(f)
	else:
		if wideband:
			snapshots.arm_fft_wb_snapshots(f)
		else:
			snapshots.arm_fft_nb_snapshots(f)

	snapshots.arm_quant_snapshots(f)
	# snapshots.arm_vacc_in_snapshots(f)
	snapshots.arm_vacc_snapshots(f)
	return wideband, pfb

def DecimalToBinary(num):
	return (bin(num)[2:])

def NumStages(binary):
	stages = 0
	for b in binary:
		if int(b) == 1:
			stages += 1
	return stages

def calc_shift():
	# shift_pairs = ['01','10','10','01','10','10','01','10'] # Default 26006
	# shift_pairs = ['01','10','10','10','10','10','10','10']  # Full shift
	sp_1 = ['01','10','10','10','10','10','10','10']  # 27306 (21846)
	sp_2 = ['01','10','10','10','10','10','01','10']  # 27302 (25942)
	sp_3 = ['01','10','10','10','10','01','10','10']  # 27290 (22870)
	sp_4 = ['01','10','10','10','01','10','10','10']  # 27242 (22102)
	sp_5 = ['01','10','10','01','10','10','10','10']  # 27050 (21910)
	sp_6 = ['01','10','01','10','10','10','10','10']  # 26282 (21862)
	sp_7 = ['01','01','10','10','10','10','10','10']  # 23210 (21850)
	sp_8 = ['01','10','10','01','10','10','01','10']  # 27046 (26006)
	sp_9 = ['01','10','10','01','10','01','01','10']  # 27030 (27030)
	# shift_pairs = [sp_1, sp_2, sp_3, sp_4, sp_5, sp_6, sp_7, sp_8, sp_9]
	shift_pairs = [sp_1, sp_2, sp_8, sp_9]

	# shift_bin = ''
	shifts = []
	for pair in shift_pairs:
		shift_bin = ''
		num_stages = 0
		for sp in pair:
			num_stages += int(sp,2)
			shift_bin+=sp
		shift_rev = shift_bin[::-1]
		shift_int = int(shift_rev,2)
		shifts.append([num_stages, shift_int, shift_bin])
		print 'Desired', int(shift_bin,2), 'which is flipped and input to reg:',shift_int
	return shifts

def run_xil_fft_shift_analysis(f, args):
	print ''
	print 'FFT Shift Analysis'
	print '------------------'

	# Generate shift values
	shifts = calc_shift()
	cw_scales = [0.5]

	analysis_data = []
	for cw_scale in cw_scales:
		for stages, shift, shift_bin in shifts:
			overflow = 0
			# set_registers.set_cw_generator(f, scale=cw, freq=args.cw_freq)
			# set_registers.set_mixer_freq(f, mix_freq=args.mix_freq)
			# set_registers.set_fft_shift(f, shift=shift)

			change_setup(f, args, cw_scale, shift)

			# Sleep
			time.sleep(0.01)

			# Issue manual sync
			manual_sync(f)

			# Read Snapshot data
			adc_data = snapshots.read_adc_snapshots(f)
			ddc_data = snapshots.read_ddc_snapshots(f)

			print ' '
			print '---CW Data---'
			print 'Requested CW amplitude:', cw_scale
			print 'CW peak(max):', np.max(adc_data)
			print 'CW peak(min):', np.min(adc_data)
			cw_pwr = np.sum(np.square(np.abs(adc_data)))/len(adc_data)
			print 'CW power:', cw_pwr
			print 'CW mean:', np.sum(adc_data)/len(adc_data)
			print ' '
				
			print ' '
			print '---DDC Data---'
			# print 'DDC peak(max)', np.max(ddc_data)
			# print 'DDC peak(min)', np.min(ddc_data)

			fft_ddc = np.fft.fftn(ddc_data)
			fft_peak = np.max(np.abs(fft_ddc))
			# fft_peak_pwr = db_power(np.square(fft_peak))

			fft_peak_channel = np.argmax(np.abs(fft_ddc))
			# fft_pwr_spectrum = np.sum(np.square(np.abs(fft_ddc)))
			
			print 'fft_peak:', fft_peak
			# print fft_peak_abs
			# print 'fft_peak_pwr (dB):', fft_peak_pwr
			# print fft_peak_channel
			# print fft_pwr_spectrum
		
			# ddc_pwr_db = db(np.sum(np.square(np.abs(ddc_data)))/len(ddc_data))

			# print 'DDC power (dB)', ddc_pwr_db
			print 'DDC mean', np.sum(ddc_data)/len(ddc_data)
			print ' '

			data = []
			name = 'Xil FFT w/o PFB'
			data.append((snapshots.read_fft_nb_snapshots(f), name))

			overflow_count = f.registers.pfb_of_cnt.read()['data']['cnt']
			if overflow_count > 0:
				print 'FFT Overflow (counter): (***OVERFLOW***)', overflow_count
				overflow = 1
			else:
				print 'FFT Overflow (counter):', overflow_count
				overflow = 0
			print ' '

			for i, (spectrum, name) in enumerate(data):
				xil_peak = np.max(np.abs(spectrum))
				xil_peak_pwr = db_power(np.square(xil_peak))
				xil_peak_channel = np.argmax(np.abs(spectrum))
				xil_pwr_spectrum = np.sum(np.square(np.abs(spectrum)))
				
				print '--Xil Channel Data---'
				print 'Xil Peak channel:', xil_peak_channel
				print 'Xil Peak channel value (cmplx):', spectrum[xil_peak_channel]
				print 'Xil Peak value:', xil_peak
				print 'Xil Peak Pwr (dB):', xil_peak_pwr
				# print 'Xil Pwr Spec:', xil_pwr_spectrum
				print ' '

				print '---Shift---'
				expected_input_output_ratio = np.power(2,stages)
				actual_input_output_ratio = fft_peak/xil_peak

				print 'Requested Shift:', shift
				print 'Shift (Bin)', shift_bin 
				print 'Expected stages shifted:', stages
				print 'Expected Input/Output ratio:', expected_input_output_ratio
				print 'Actual Input/Output ratio :', actual_input_output_ratio
				print ' '
				analysis_data.append([cw_scale, stages, shift, overflow, expected_input_output_ratio, actual_input_output_ratio])


			print '***---***---***---***---***---***'
			print ' '
	
	fft_plotting.plot_fft_analysis_results(analysis_data)

def run(f, args):
	# Setup and return modes
	wideband, pfb = setup_with_args(f,args)

	# Sleep
	time.sleep(0.01)

	# Issue manual sync
	manual_sync(f)

	# List to hold results
	data = []

	# Read Snapshot data
	adc_data = snapshots.read_adc_snapshots(f)
	# data.append((snapshots.read_adc_snapshots(f), 'adc'))

	# Read FFT/PFB Snapshots and plot
	if pfb:
		if wideband:
			name = 'CASPER FFT with PFB'
			data.append((snapshots.read_pfb_wb_snapshots(f), name))
		else:
			name = 'Xil FFT with PFB'
			data.append((snapshots.read_pfb_nb_snapshots(f), name))
	else:
		if wideband:
			name = 'CASPER FFT without PFB'
			data.append((snapshots.read_fft_wb_snapshots(f), name))
		else:
			name = 'Xil FFT w/o PFB'
			data.append((snapshots.read_fft_nb_snapshots(f), name))

	# data.append((snapshots.read_quant_snapshots(f), name + ' ' + '(Quant)'))
	# data.append((snapshots.read_vacc_in_snapshots(f), name + ' ' + '(VACC In)'))

	# data.append((snapshots.read_vacc_snapshots(f), name + ' ' + '(Acc:'+str(args.acc)+')'))

	if args.xil_shift_analysis:
		run_xil_fft_shift_analysis(f, args)
	
	if args.plot:
		fft_plotting.plot_results_separate(data, args)

	if args.embed:
		embed()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--skarab", type=str, default=host, help="Specify SKARAB host")
	parser.add_argument("--program", action="store_true", help="Program FPGA")
	parser.add_argument("--acc", type=int, default=64, help="Number of accumulations")
	parser.add_argument("--cw", type=float, default=0.75, help="CW scale")
	parser.add_argument("--cw_freq", type=float, default=53.5e6, help="CW frequency")
	parser.add_argument("--wgn", type=float, default=2**(-10), help="WGN scale")
	parser.add_argument("--eq", type=int, default=1, help="EQ scale")
	parser.add_argument("--fft_shift", type=int, default=32767, help="FFT shift")
	parser.add_argument("--mix_freq", type=float, default=100e6, help="DDS Mixer frequency")
	parser.add_argument("--embed", action="store_true", default=False, help="Enable Ipython embed")
	parser.add_argument("--plot", action="store_true", default=False, help="Enable plotting")
	parser.add_argument("--xil_shift_analysis", action="store_true", default=False, help="Cycle through a range of FFT shift and CW levels")
	args = parser.parse_args()
	print 'Using SKARAB:', args.skarab

	f = casperfpga.CasperFpga(args.skarab)
	program_fpga(f, args, prog_file)

	run(f,args)

if __name__ == '__main__':
	main()
